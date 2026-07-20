import os
import requests
from git_utils import git_update
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import *

from parser import (
    read_complete_pdf,
    extract_report_date,
    split_lines,
    inspect_lines,
    extract_district_records,
    save_records_csv
)
from database import (
    create_database,
    add_log,
    get_last_report_date
)


# ==========================================================
# Create folders
# ==========================================================

def create_project_folders():

    os.makedirs(PDF_FOLDER, exist_ok=True)

    os.makedirs(CSV_FOLDER, exist_ok=True)

    os.makedirs(LOG_FOLDER, exist_ok=True)

    os.makedirs(TEMP_FOLDER, exist_ok=True)


# ==========================================================
# Validate PDF
# ==========================================================

def validate_pdf(response):

    content_type = response.headers.get("Content-Type", "")

    if "application/pdf" not in content_type.lower():

        raise Exception("Downloaded file is not a PDF.")

    if not response.content.startswith(b"%PDF"):

        raise Exception("Invalid PDF file.")
    
# ==========================================================
# Get Latest PDF URL from IMD Website
# ==========================================================

def get_latest_pdf_url():

    print()
    print("=" * 60)
    print("LOCATING LATEST PDF")
    print("=" * 60)

    response = requests.get(IMD_PAGE_URL)

    if response.status_code != 200:
        raise Exception("Unable to open IMD webpage.")

    soup = BeautifulSoup(response.text, "html.parser")

    pdf_button = soup.find("a", id="default-block-btn")

    if pdf_button is None:
        raise Exception("Download button not found.")

    pdf_href = pdf_button.get("href")

    pdf_url = urljoin(IMD_PAGE_URL, pdf_href)

    print("Latest PDF URL Found:")
    print(pdf_url)

    return pdf_url


# ==========================================================
# Download PDF
# ==========================================================

def download_pdf():

    print("\nConnecting to IMD...")

    pdf_url = get_latest_pdf_url()

    response = requests.get(pdf_url)

    response.raise_for_status()

    validate_pdf(response)

    print("Connection Successful.")

    today = datetime.now().strftime("%Y-%m-%d")

    pdf_name = f"{today}.pdf"

    pdf_path = os.path.join(PDF_FOLDER, pdf_name)

    if os.path.exists(pdf_path):

        print("\nToday's PDF already exists.")

        return pdf_path

    print("\nDownloading PDF...")

    with open(pdf_path, "wb") as file:

        file.write(response.content)

    print("Download Complete.")

    return pdf_path


# ==========================================================
# ==========================================================
# Main
# ==========================================================
# Main
# ==========================================================

def main():

    print()
    print("=" * 60)
    print("IMD DAILY RAINFALL ARCHIVER")
    print("=" * 60)

    # ------------------------------------------------------
    # Create folders and database
    # ------------------------------------------------------

    create_project_folders()

    create_database()

    # ------------------------------------------------------
    # Download latest PDF
    # ------------------------------------------------------

    pdf_path = download_pdf()

    # ------------------------------------------------------
    # Read PDF
    # ------------------------------------------------------

    print()
    print("Reading PDF...")

    text = read_complete_pdf(pdf_path)

    # ------------------------------------------------------
    # Extract Report Date
    # ------------------------------------------------------

    report_date = extract_report_date(text)

    print()
    print("=" * 60)
    print("REPORT INFORMATION")
    print("=" * 60)
    print("Current Report Date :", report_date)

    # ------------------------------------------------------
    # Check last archived report
    # ------------------------------------------------------

    last_report = get_last_report_date()

    print("Last Archived Report :", last_report)

    if last_report is not None and last_report == report_date:

        print()
        print("=" * 60)
        print("REPORT ALREADY ARCHIVED")
        print("=" * 60)
        print("No new report available.")
        print("Program terminated.")

        return

    print()
    print("New report detected.")
    print("Continuing processing...")

    # ------------------------------------------------------
    # Save raw text
    # ------------------------------------------------------

    txt_filename = report_date + ".txt"

    txt_path = os.path.join(TEMP_FOLDER, txt_filename)

    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(text)

    print()
    print("Raw text saved at:")
    print(txt_path)

    # ------------------------------------------------------
    # Split into lines
    # ------------------------------------------------------

    lines = split_lines(text)

    print()
    print("Total Lines :", len(lines))

    # ------------------------------------------------------
    # Inspect PDF (Debug)
    # ------------------------------------------------------

    inspect_lines(lines)

    # ------------------------------------------------------
    # Parse all records
    # ------------------------------------------------------

    records = extract_district_records(lines)

    # ------------------------------------------------------
    # Save CSV
    # ------------------------------------------------------

    csv_filename = report_date + ".csv"

    csv_path = os.path.join(CSV_FOLDER, csv_filename)

    save_records_csv(records, csv_path)

    print()
    print("CSV Saved At:")
    print(csv_path)

    # ------------------------------------------------------
    # Update database
    # ------------------------------------------------------

    add_log(
        download_date=datetime.now().strftime("%Y-%m-%d"),
        report_date=report_date,
        filename=os.path.basename(pdf_path),
        status="Downloaded"
    )

    print()
    print("Database Updated.")

    # ------------------------------------------------------
    # Upload to GitHub
    # ------------------------------------------------------

    git_update(report_date)

    print()
    print("=" * 60)
    print("PROGRAM COMPLETED SUCCESSFULLY")
    print("=" * 60)


# ==========================================================
# Program Entry
# ==========================================================

if __name__ == "__main__":
    main()