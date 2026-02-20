import psutil
import time
from datetime import datetime, timezone
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# ---------------- AUTH ----------------
def authenticate():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


# ---------------- METRICS ----------------
def get_metrics(prev_disk=None, prev_net=None):

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_per_core = str(psutil.cpu_percent(interval=0, percpu=True))

    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_used_gb = round(ram.used / (1024 ** 3), 2)

    swap_percent = psutil.swap_memory().percent

    disk_percent = psutil.disk_usage('/').percent
    disk_io = psutil.disk_io_counters()

    if prev_disk:
        disk_read = (disk_io.read_bytes - prev_disk.read_bytes) / 15
        disk_write = (disk_io.write_bytes - prev_disk.write_bytes) / 15
    else:
        disk_read = 0
        disk_write = 0

    net_io = psutil.net_io_counters()

    if prev_net:
        net_sent = (net_io.bytes_sent - prev_net.bytes_sent) / 15
        net_recv = (net_io.bytes_recv - prev_net.bytes_recv) / 15
    else:
        net_sent = 0
        net_recv = 0

    row = [
        timestamp,
        cpu_percent,
        cpu_per_core,
        ram_percent,
        ram_used_gb,
        swap_percent,
        disk_percent,
        round(disk_read / 1024, 2),
        round(disk_write / 1024, 2),
        round(net_sent / 1024, 2),
        round(net_recv / 1024, 2)
    ]

    return row, disk_io, net_io


# ---------------- MAIN ----------------
def main():
    creds = authenticate()
    client = gspread.authorize(creds)

    try:
        sheet = client.open("PIPLINE")
    except:
        sheet = client.create("PIPLINE")

    headers = [
        "Timestamp", "CPU%", "CPU per Core", "RAM%", "RAM Used GB",
        "Swap%", "Disk%", "Disk Read KB/s",
        "Disk Write KB/s", "Net Sent KB/s", "Net Recv KB/s"
    ]

    # -------- TimeSeries --------
    try:
        ts_sheet = sheet.worksheet("TimeSeries")
    except:
        ts_sheet = sheet.add_worksheet(title="TimeSeries", rows=2000, cols=20)
        ts_sheet.append_row(headers)

    # -------- LastOnly (same structure) --------
    try:
        last_sheet = sheet.worksheet("LastOnly")
    except:
        last_sheet = sheet.add_worksheet(title="LastOnly", rows=5, cols=20)
        last_sheet.append_row(headers)

    prev_disk = None
    prev_net = None

    while True:
        row, prev_disk, prev_net = get_metrics(prev_disk, prev_net)

        # Historical append
        ts_sheet.append_row(row)

        # Update ONLY row 2 in LastOnly
        last_sheet.update("A2", [row])

        print("Data sent:", row)

        time.sleep(15)


if __name__ == "__main__":
    main()