#!/usr/bin/env python3
"""Run A-share OpenCLI source health checks and emit diagnostic events."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class SourceSpec:
    source_name: str
    source_tier: str
    command: list[str]
    entity: str
    requested_fields: list[str]
    failure_repairs: dict[str, list[str]]
    retry_variants: list[tuple[str, list[str]]] | None = None
    fallback: "SourceSpec | None" = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def extract_json(output: str) -> Any | None:
    decoder = json.JSONDecoder()
    for index, char in enumerate(output):
        if char not in "[{":
            continue
        try:
            value, _ = decoder.raw_decode(output[index:])
            return value
        except json.JSONDecodeError:
            continue
    return None


def run_command(command: list[str], timeout: int) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            command,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        return completed.returncode, completed.stdout or "", completed.stderr or ""
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        return 124, stdout, stderr or f"Command timed out after {timeout}s"
    except FileNotFoundError as exc:
        return 127, "", str(exc)


def resolve_opencli() -> list[str] | None:
    for candidate in ("opencli", "opencli.cmd", "opencli.exe", "opencli.ps1"):
        path = shutil.which(candidate)
        if not path:
            continue
        if path.lower().endswith(".ps1"):
            powershell = shutil.which("powershell") or shutil.which("pwsh")
            if powershell:
                return [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path]
            return None
        return [path]
    return None


def detect_failure_reason(returncode: int, stdout: str, stderr: str, data: Any | None) -> str:
    combined = f"{stdout}\n{stderr}".lower()
    if returncode == 124:
        return "timeout"
    if "not recognized" in combined or "not found" in combined:
        return "adapter_error"
    if "api_key" in combined or "token" in combined or "credential" in combined:
        return "missing_credentials"
    if "rate" in combined and "limit" in combined:
        return "rate_limit"
    if "schema" in combined or "missing expected" in combined:
        return "schema_drift"
    if "no data" in combined or data == [] or data is None:
        return "no_data"
    if returncode != 0:
        return "adapter_error"
    return "none"


def validate_rows(data: Any, expected_fields: list[str]) -> tuple[str, str]:
    if not isinstance(data, list) or not data:
        return "fail", "no rows"
    first = data[0]
    if not isinstance(first, dict):
        return "suspicious", "first row is not an object"
    missing = [field for field in expected_fields if field not in first]
    if missing:
        return "suspicious", f"missing expected fields: {', '.join(missing)}"
    non_null = [field for field in expected_fields if first.get(field) not in (None, "", [])]
    if not non_null:
        return "partial", "expected fields are present but empty"
    return "pass", "ok"


def infer_timestamp(data: Any) -> str | None:
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        return None
    row = data[0]
    for field in ("REPORT_DATE", "reportDate", "publishDate", "noticeDate", "announceDate", "time", "date"):
        if row.get(field):
            return str(row[field])
    return None


def repairs_for(spec: SourceSpec, reason: str) -> list[str]:
    return spec.failure_repairs.get(reason) or spec.failure_repairs.get("default", [])


def check_source(spec: SourceSpec, timeout: int) -> tuple[dict[str, Any], Any | None]:
    returncode, stdout, stderr = run_command(spec.command, timeout)
    data = extract_json(stdout)
    status, validation_note = validate_rows(data, spec.requested_fields)
    reason = detect_failure_reason(returncode, stdout, stderr, data)

    if returncode != 0:
        status = "fail"
    elif status != "pass" and reason == "none":
        if "missing expected" in validation_note:
            reason = "schema_drift"
        elif "expected fields are present but empty" in validation_note:
            reason = "empty_rows"
        else:
            reason = "no_data"

    event = {
        "source_name": spec.source_name,
        "source_tier": spec.source_tier,
        "command_or_access_path": " ".join(spec.command),
        "entity": spec.entity,
        "requested_fields": spec.requested_fields,
        "status": status,
        "observed_at": utc_now(),
        "data_timestamp": infer_timestamp(data),
        "failure_reason": reason if status != "pass" else "none",
        "fallback_used": "none",
        "user_message": "",
        "repair_candidates": [] if status == "pass" else repairs_for(spec, reason),
        "validation_note": validation_note,
        "retry_attempts": [],
    }

    if status == "pass":
        event["user_message"] = f"{spec.source_name} returned usable data for {spec.entity}."
    else:
        event["user_message"] = (
            f"{spec.source_name} returned {status} for {spec.entity}: "
            f"{event['failure_reason']}. Treat related conclusions as incomplete unless fallback data is used."
        )
    return event, data


def retry_failed_source(event: dict[str, Any], spec: SourceSpec, timeout: int) -> None:
    if event["status"] == "pass" or not spec.retry_variants:
        return
    for label, command in spec.retry_variants:
        returncode, stdout, stderr = run_command(command, timeout)
        data = extract_json(stdout)
        status, validation_note = validate_rows(data, spec.requested_fields)
        reason = detect_failure_reason(returncode, stdout, stderr, data)
        if returncode != 0:
            status = "fail"
        elif status != "pass" and reason == "none":
            if "missing expected" in validation_note:
                reason = "schema_drift"
            elif "expected fields are present but empty" in validation_note:
                reason = "empty_rows"
            else:
                reason = "no_data"

        event["retry_attempts"].append(
            {
                "label": label,
                "command_or_access_path": " ".join(command),
                "status": status,
                "failure_reason": reason if status != "pass" else "none",
                "data_timestamp": infer_timestamp(data),
                "validation_note": validation_note,
            }
        )
        if status == "pass":
            event["status"] = "recovered"
            event["fallback_used"] = label
            event["failure_reason"] = "none"
            event["repair_candidates"] = []
            event["data_timestamp"] = infer_timestamp(data)
            event["user_message"] += f" Retry succeeded: {label}."
            return


def summarize(events: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [event["source_name"] for event in events if event["status"] not in ("pass", "recovered")]
    fallbacks = [event["fallback_used"] for event in events if event.get("fallback_used") not in (None, "none")]
    status = "pass" if not failed else "partial"
    return {
        "status": status,
        "failed_sources": failed,
        "fallback_sources": fallbacks,
        "user_warning": (
            "All checked A-share sources returned usable data."
            if status == "pass"
            else "Some A-share sources failed or returned incomplete data; inspect diagnostic_events before relying on conclusions."
        ),
        "repair_candidates": sorted(
            {
                repair
                for event in events
                for repair in event.get("repair_candidates", [])
            }
        ),
    }


def build_specs(opencli_cmd: list[str], symbol: str, market: str, limit: int) -> list[SourceSpec]:
    end_date = datetime.now(timezone.utc).strftime("%Y%m%d")
    start_date = f"{int(end_date[:4]) - 1}0101"
    common_repairs = {
        "adapter_error": ["run the same command with --trace retain-on-failure", "inspect opencli adapter help"],
        "timeout": ["retry once", "reduce result limit", "try fallback source"],
        "schema_drift": ["inspect returned fields", "update adapter field mapping", "try alternative command"],
        "empty_rows": ["treat adapter output as schema drift", "run command with --trace retain-on-failure", "file upstream adapter issue with sample output"],
        "no_data": ["widen date window or limit", "try fallback source", "ask user for a more specific category"],
        "default": ["try fallback source", "surface source limitation to user"],
    }
    announcement_fallback = SourceSpec(
        source_name="Eastmoney announcement",
        source_tier="Tier-3",
        command=[*opencli_cmd, "eastmoney", "announcement", "--code", symbol, "--limit", str(limit), "-f", "json"],
        entity=symbol,
        requested_fields=["title", "url"],
        failure_repairs=common_repairs,
    )
    return [
        SourceSpec(
            source_name="Eastmoney stock quote",
            source_tier="Tier-3",
            command=[*opencli_cmd, "eastmoney", "stock-quote", "--code", symbol, "--market", market, "-f", "json"],
            entity=symbol,
            requested_fields=["code", "name", "price", "changeRate", "amount"],
            failure_repairs=common_repairs,
        ),
        SourceSpec(
            source_name="Eastmoney financial summary",
            source_tier="Tier-3",
            command=[*opencli_cmd, "eastmoney", "bbsj-summary", "--code", symbol, "--limit", str(limit), "-f", "json"],
            entity=symbol,
            requested_fields=["REPORT_DATE", "TOTAL_OPERATE_INCOME", "PARENT_NETPROFIT", "BASIC_EPS"],
            failure_repairs=common_repairs,
        ),
        SourceSpec(
            source_name="Eastmoney broker research",
            source_tier="Tier-3",
            command=[*opencli_cmd, "eastmoney", "research", "--code", symbol, "--type", "stock", "--limit", str(limit), "-f", "json"],
            entity=symbol,
            requested_fields=["publishDate", "orgName", "rating", "title", "pdfUrl"],
            failure_repairs=common_repairs,
        ),
        SourceSpec(
            source_name="CNInfo disclosure",
            source_tier="Tier-3",
            command=[*opencli_cmd, "cninfo", "disclosure", "--symbol", symbol, "--limit", str(limit), "-f", "json"],
            entity=symbol,
            requested_fields=["announceDate", "title", "category"],
            failure_repairs={
                **common_repairs,
                "no_data": ["retry with wider date window", "try Eastmoney announcement fallback", "ask user for disclosure category", "inspect CNInfo adapter query parameters"],
                "empty_rows": ["treat CNInfo result as adapter/schema anomaly", "run CNInfo command with --trace retain-on-failure", "file upstream adapter issue with sample output", "try Eastmoney announcement fallback"],
            },
            retry_variants=[
                (
                    "CNInfo disclosure wide date retry",
                    [
                        *opencli_cmd,
                        "cninfo",
                        "disclosure",
                        "--symbol",
                        symbol,
                        "--startDate",
                        start_date,
                        "--endDate",
                        end_date,
                        "--limit",
                        str(limit),
                        "-f",
                        "json",
                    ],
                )
            ],
            fallback=announcement_fallback,
        ),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run A-share source health checks.")
    parser.add_argument("--symbol", default="600519", help="A-share stock code, e.g. 600519")
    parser.add_argument("--market", default="sh", help="Eastmoney market code: sh or sz")
    parser.add_argument("--limit", type=int, default=3, help="Rows to request for list-like sources")
    parser.add_argument("--timeout", type=int, default=25, help="Command timeout in seconds")
    args = parser.parse_args()

    opencli_cmd = resolve_opencli()
    if opencli_cmd is None:
        result = {
            "source_health": {
                "status": "fail",
                "failed_sources": ["opencli"],
                "fallback_sources": [],
                "user_warning": "opencli is not available on PATH.",
                "repair_candidates": ["install opencli", "add opencli to PATH"],
            },
            "diagnostic_events": [],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    events: list[dict[str, Any]] = []
    for spec in build_specs(opencli_cmd, args.symbol, args.market, args.limit):
        event, _ = check_source(spec, args.timeout)
        retry_failed_source(event, spec, args.timeout)
        if event["status"] not in ("pass", "recovered") and spec.fallback is not None:
            fallback_event, _ = check_source(spec.fallback, args.timeout)
            events.append(fallback_event)
            if fallback_event["status"] == "pass":
                event["fallback_used"] = spec.fallback.source_name
                event["user_message"] += f" Fallback succeeded: {spec.fallback.source_name}."
        events.append(event)

    result = {
        "source_health": summarize(events),
        "diagnostic_events": events,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["source_health"]["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
