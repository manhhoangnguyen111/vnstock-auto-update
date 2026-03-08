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

```
df = stock.quote.history(
    start=today,
    end=today,
    interval="1D"
)
```

except
