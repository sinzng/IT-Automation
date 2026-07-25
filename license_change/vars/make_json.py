import os
import json
import re
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

# ───────────────────────────────────────
# 환경변수 읽기
# ───────────────────────────────────────
host_ip = os.environ.get("host_ip", "")
jeus_id = os.environ.get("jeus_id", "")
device_name = os.environ.get("device_name", "")
port = os.environ.get("port", "")
web_check = os.environ.get("web_check", "")
json_path = os.environ.get("json_path", "")
output_path = os.environ.get("output_path", "")
file_name = os.environ.get("file_name", "")

# ───────────────────────────────────────
# 값 파싱
# ───────────────────────────────────────
host_name = ""
due_day = ""

lines = web_check.strip().splitlines()
dates = []

for line in lines:
    if "HOST-NAME" in line:
        host_name = line.split(":")[-1].strip()
    elif "DUE-DAY" in line:
        raw_date = line.split(":")[-1].strip().replace("/", "-")
        try:
            dates.append(datetime.strptime(raw_date, "%Y-%m-%d"))
        except ValueError:
            pass

if dates:
    due_day = max(dates).strftime("%Y-%m-%d")
    if len(dates) >= 2 and dates[1] > dates[0]:
        status = "변경완료"
    else:
        status = "변경실패"
# ───────────────────────────────────────
# JSON 개별 파일로 저장
# ───────────────────────────────────────
os.makedirs(json_path, exist_ok=True)

host_id = host_ip or device_name or "unknown"
json_file = os.path.join(json_path, f"{host_id}.json")

with open(json_file, "w", encoding="utf-8") as f:
    json.dump({
        "host": host_ip,
        "device": device_name,
        "port": port,
        "jeus_id": jeus_id,
        "host_name": host_name,
        "due_day": due_day,
        "status": status
    }, f, indent=2, ensure_ascii=False)
