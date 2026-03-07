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

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

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

stock = Vnstock().stock(symbol="VN30", source="VCI")

df = stock.quote.history(
    start=today,
    end=today,
    interval="1D"
)

if df.empty:
    print("No new data today")
    exit()

# =========================
# CHECK LAST ROW
# =========================

existing = sheet.get_all_values()

last_date = existing[-1][0]

new_date = df.iloc[-1]["time"].strftime("%Y-%m-%d")

if new_date == last_date:
    print("Already updated today")
    exit()

# =========================
# APPEND DATA
# =========================

row = df.iloc[-1].tolist()

sheet.append_row(row)

print("New row added")

# =========================
# TELEGRAM NOTIFICATION
# =========================

message = f"✅ VNStock updated {new_date}"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": TELEGRAM_CHAT_ID,
    "text": message
})
