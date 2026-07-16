"""
=========================================================
IMD Rainfall Archive Project
Configuration File
=========================================================
"""

import os

# -------------------------------------------------------
# IMD URL
# -------------------------------------------------------

PDF_URL = (
    "https://mausam.imd.gov.in/Rainfall/"
    "DISTRICT_RAINFALL_DISTRIBUTION_COUNTRY_INDIA_cd.pdf"
)

# -------------------------------------------------------
# Project Root
# -------------------------------------------------------

BASE_DIR = os.getcwd()

# -------------------------------------------------------
# Archive Folders
# -------------------------------------------------------

ARCHIVE_FOLDER = os.path.join(BASE_DIR, "archive")

PDF_FOLDER = os.path.join(ARCHIVE_FOLDER, "pdf")

CSV_FOLDER = os.path.join(ARCHIVE_FOLDER, "csv")

LOG_FOLDER = os.path.join(ARCHIVE_FOLDER, "logs")

TEMP_FOLDER = os.path.join(ARCHIVE_FOLDER, "temp")

# -------------------------------------------------------
# Log File
# -------------------------------------------------------

LOG_FILE = os.path.join(LOG_FOLDER, "download_log.csv")

TEMP_FOLDER = os.path.join(BASE_DIR, "archive", "temp")
# ==========================================================
# IMD Rainfall Statistics Page
# ==========================================================

IMD_PAGE_URL = "https://mausam.imd.gov.in/responsive/rainfall_statistics.php?PAGE=4"