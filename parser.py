import pdfplumber
import re
import csv
STATE_PATTERN = re.compile(
    r"^(.*?)\s+"
    r"(-?\d+\.?\d*)\s+"
    r"(-?\d+\.?\d*)\s+"
    r"(-?\d+)\s+"
    r"([A-Z]+)\s+"
    r"(-?\d+\.?\d*)\s+"
    r"(-?\d+\.?\d*)\s+"
    r"(-?\d+)\s+"
    r"([A-Z]+)$"
)

DISTRICT_PATTERN = re.compile(
    r'^(\d+)\s+'                  # District number
    r'(.+?)\s+'                   # District name
    r'(-?\d+(?:\.\d+)?)\s+'       # Daily Actual
    r'(-?\d+(?:\.\d+)?)\s+'       # Daily Normal
    r'(-?\d+)\s+'                 # Daily Departure
    r'([A-Z]+)\s+'                # Daily Category
    r'(-?\d+(?:\.\d+)?)\s+'       # Season Actual
    r'(-?\d+(?:\.\d+)?)\s+'       # Season Normal
    r'(-?\d+)\s+'                 # Season Departure
    r'([A-Z]+)$'                  # Season Category
)

# ==========================================================
# Read First Page
# ==========================================================

def read_first_page(pdf_path):

    with pdfplumber.open(pdf_path) as pdf:

        return pdf.pages[0].extract_text()


# ==========================================================
# Read Complete PDF
# ==========================================================

def read_complete_pdf(pdf_path):

    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:

        print()
        print("Total Pages in PDF :", len(pdf.pages))
        print()

        for i, page in enumerate(pdf.pages):

            print(f"Reading Page {i+1}")

            text = page.extract_text()

            if text:
                full_text += text + "\n"

    print()
    print("Total Characters Extracted :", len(full_text))
    print()

    return full_text
# ==========================================================
# Extract Report Date
# ==========================================================

def extract_report_date(text):

    pattern = r"DAY:\s*(\d{2}-\d{2}-\d{4})"

    match = re.search(pattern, text)

    if match:

        return match.group(1)

    return "Unknown"


# ==========================================================
# Split text into lines
# ==========================================================

def split_lines(text):

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:

            lines.append(line)

    return lines
# ==========================================================
# Show First Few Lines
# ==========================================================

def show_sample_lines(text):

    lines = text.split("\n")

    print()
    print("=" * 60)
    print("FIRST 50 LINES")
    print("=" * 60)

    for i, line in enumerate(lines[:50], start=1):

        print(f"{i:02d} : {line}")

    return lines

import re

def classify_line(line):

    line = line.strip()

    if not line:
        return "EMPTY"

    if line.startswith("India Meteorological"):
        return "HEADER"

    if line.startswith("Hydromet"):
        return "HEADER"

    if line.startswith("DISTRICT RAINFALL"):
        return "HEADER"

    if line.startswith("DAY:"):
        return "HEADER"

    if line.startswith("S.No"):
        return "HEADER"

    if line.startswith("LEGEND"):
        return "LEGEND"

    # District rows always begin with a serial number
    if re.match(r"^\d+\s", line):
        return "DISTRICT"

    # Everything else is treated as a state summary
    return "STATE"

def inspect_lines(lines):

    print()
    print("=" * 60)
    print("LINE CLASSIFICATION")
    print("=" * 60)

    for line in lines[:40]:

        line_type = classify_line(line)

        print(f"{line_type:10} -> {line}")

# ==========================================================
# Extract District Records
# ==========================================================

# ==========================================================
# Extract District Records
# ==========================================================
def extract_district_records(lines):

    
    current_state = ""

    records = []
    state_count = 0
    district_count = 0

    for line in lines:

        line = line.strip()

        # --------------------------------------------------
        # Skip unwanted lines
        # --------------------------------------------------
        if not line:
            continue

        if line.startswith("DAY:"):
            continue

        if line.startswith("S.No"):
            continue

        if line.startswith("LEGEND"):
            break

        if "India Meteorological" in line:
            continue

        if "Hydromet Division" in line:
            continue

        if "DISTRICT RAINFALL DISTRIBUTION" in line:
            continue

        # --------------------------------------------------
        # Detect STATE summary line
        # --------------------------------------------------
        if not line[0].isdigit():

            match = STATE_PATTERN.match(line)

            if match:

                current_state = match.group(1).strip()

                state_record = {

                    "record_type": "STATE",

                    "state": current_state,

                    "daily_actual": float(match.group(2)),
                    "daily_normal": float(match.group(3)),
                    "daily_departure": int(match.group(4)),
                    "daily_category": match.group(5),

                    "season_actual": float(match.group(6)),
                    "season_normal": float(match.group(7)),
                    "season_departure": int(match.group(8)),
                    "season_category": match.group(9)

                }

                records.append(state_record)
                state_count += 1

               
            continue

        # --------------------------------------------------
        # Detect DISTRICT line
        # --------------------------------------------------
        if line[0].isdigit():

            match = DISTRICT_PATTERN.match(line)

            if not match:
                print("Unable to parse district:", line)
                continue

            district_record = {

                "record_type": "DISTRICT",

                "state": current_state,

                "district_no": int(match.group(1)),

                "district": match.group(2).strip(),

                "daily_actual": float(match.group(3)),
                "daily_normal": float(match.group(4)),
                "daily_departure": int(match.group(5)),
                "daily_category": match.group(6),

                "season_actual": float(match.group(7)),
                "season_normal": float(match.group(8)),
                "season_departure": int(match.group(9)),
                "season_category": match.group(10)

            }

            records.append(district_record)
            district_count += 1

            

    print()

    print("=" * 60)
    print("PARSING SUMMARY")
    print("=" * 60)

    print(f"States Parsed     : {state_count}")
    print(f"Districts Parsed  : {district_count}")
    print(f"Total Records     : {len(records)}")

    print()

    return records

import csv

# ==========================================================
# Save Records to CSV
# ==========================================================
def save_records_csv(records, csv_path):

    if not records:
        print("No records to save.")
        return

    fieldnames = [
        "record_type",
        "state",
        "district_no",
        "district",
        "daily_actual",
        "daily_normal",
        "daily_departure",
        "daily_category",
        "season_actual",
        "season_normal",
        "season_departure",
        "season_category"
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        writer.writeheader()

        for record in records:

            # Fill missing keys (STATE records don't have district info)
            row = {}

            for field in fieldnames:
                row[field] = record.get(field, "")

            writer.writerow(row)

    print()
    print("=" * 60)
    print("CSV CREATED SUCCESSFULLY")
    print("=" * 60)
    print(csv_path)