from vnstock import Vnstock
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import os

# =========================

# CONFIG

# =========================

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

SPREADSHEET_ID = "1o4OoH78lGVln6Alm15_uh97PPu4eAdr74JN0LEp3u90"

# =========================

# GOOGLE SHEETS CONNECT

# =========================

scope = [
"https://spreadsheets.google.com/feeds",
"https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
"google_credentials.json", scope
)

client = gspread.authorize(creds)

sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# =========================

# GET TODAY DATA

# =========================

today = datetime.today().strftime("%Y-%m-%d")

print("Fetching data for:", today)

try:
stock = Vnstock().stock(symbol="VN30", source="VCI")
df = stock.quote.history(
start=today,
end=today,
interval="1D"
)
except Exception as e:
print("VNStock error:", e)
exit()

if df.empty:
print("No new data today")
exit()

# =========================

# CHECK LAST ROW

# =========================

existing = sheet.get_all_values()

new_date = pd.to_datetime(df.iloc[-1]["time"]).strftime("%Y-%m-%d")

if len(existing) > 1:
last_date = existing[-1][0]

```
if new_date == last_date:
    print("Already updated today")
    exit()
```

# =========================

# PREPARE DATA

# =========================

row_data = df.iloc[-1]

row = [
new_date,
row_data["open"],
row_data["high"],
row_data["low"],
row_data["close"],
row_data["volume"]
]

# =========================

# APPEND TO SHEET

# =========================

try:
sheet.append_row(row)
print("New row added:", row)
except Exception as e:
print("Google Sheets error:", e)
