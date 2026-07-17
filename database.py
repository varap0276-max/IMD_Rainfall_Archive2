"""
=========================================================
Database Functions
=========================================================
"""

import os
import csv

from config import LOG_FILE


def create_database():

    if os.path.exists(LOG_FILE):

        return

    with open(LOG_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Download_Date",
            "Report_Date",
            "Filename",
            "Status"
        ])


def add_log(download_date,
            report_date,
            filename,
            status):

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            download_date,
            report_date,
            filename,
            status
        ])

# ==========================================================
# Get Last Archived Report
# ==========================================================

def get_last_report_date():

    if not os.path.exists(LOG_FILE):
        return None

    with open(LOG_FILE, "r", encoding="utf-8") as file:

        rows = file.readlines()

    if len(rows) <= 1:
        return None

    last_row = rows[-1].strip().split(",")

    return last_row[1]