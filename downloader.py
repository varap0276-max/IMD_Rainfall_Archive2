import os
import requests

from datetime import datetime

from config import *

from parser import (
    read_complete_pdf,
    extract_report_date,
    split_lines,
    inspect_lines,
    extract_district_records,
    save_records_csv
)
from database import create_database
from database import add_log


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
# Download PDF
# ==========================================================

def download_pdf():

    print("\nConnecting to IMD...")

    response = requests.get(PDF_URL, timeout=60)

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
# Main
# ==========================================================

def main():

    print()
    print("=" * 60)
    print("IMD DAILY RAINFALL ARCHIVER")
    print("=" * 60)

    # ------------------------------------------------------
    # Create Project Folders
    # ------------------------------------------------------
    create_project_folders()

    # ------------------------------------------------------
    # Create Database
    # ------------------------------------------------------
    create_database()

    # ------------------------------------------------------
    # Download Today's PDF
    # ------------------------------------------------------
    pdf_path = download_pdf()

    # ------------------------------------------------------
    # Read Complete PDF
    # ------------------------------------------------------
    print()
    print("Reading PDF...")

    text = read_complete_pdf(pdf_path)

    # ------------------------------------------------------
    # Extract Report Date
    # ------------------------------------------------------
    report_date = extract_report_date(text)

    print()
    print("Report Date :", report_date)

    # ------------------------------------------------------
    # Save Raw Text
    # ------------------------------------------------------
    txt_filename = report_date + ".txt"

    txt_path = os.path.join(TEMP_FOLDER, txt_filename)

    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(text)

    print()
    print("Raw text saved at:")
    print(txt_path)

    # ------------------------------------------------------
    # Split into Lines
    # ------------------------------------------------------
    lines = split_lines(text)

    print()
    print("Total Lines :", len(lines))

    # ------------------------------------------------------
    # Debug Line Classification
    # ------------------------------------------------------
    inspect_lines(lines)

    # ------------------------------------------------------
    # Extract Structured Records
    # ------------------------------------------------------
    records = extract_district_records(lines)

    print()
    print("Total Records Extracted :", len(records))

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
    # Update Download Log
    # ------------------------------------------------------
    add_log(
        download_date=datetime.now().strftime("%Y-%m-%d"),
        report_date=report_date,
        filename=os.path.basename(pdf_path),
        status="Downloaded"
    )

    print()
    print("Database Updated.")

    print()
    print("=" * 60)
    print("PROGRAM COMPLETED SUCCESSFULLY")
    print("=" * 60)


# ==========================================================
# Program Entry
# ==========================================================

if __name__ == "__main__":
    main()