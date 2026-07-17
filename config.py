"""
=========================================================
IMD Rainfall Archive Project
Configuration File
=========================================================
"""

import os

# -------------------------------------------------------

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

# ==========================================================
# IMD Rainfall Statistics Page
# ==========================================================

IMD_PAGE_URL = "https://mausam.imd.gov.in/responsive/rainfall_statistics.php?PAGE=4"