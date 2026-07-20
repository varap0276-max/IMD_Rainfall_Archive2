# 🌧️ IMD Rainfall Archiver

An automated Python application that downloads, parses, archives, and version-controls the daily rainfall distribution reports published by the India Meteorological Department (IMD).

The project automatically detects newly released rainfall reports, extracts district- and state-level rainfall statistics, converts them into structured CSV files, maintains an archive database, and synchronizes the results with GitHub.

---

## Features

- Automatically detects the latest rainfall report from the IMD website
- Downloads the latest PDF report
- Validates downloaded PDF files
- Extracts text from all PDF pages
- Identifies the official report date
- Prevents duplicate downloads using a local archive database
- Parses both State Summary and District Rainfall records
- Converts extracted data into structured CSV format
- Archives PDFs, CSVs, and extracted text files
- Maintains a download history database
- Automatically commits and pushes updates to GitHub
- Supports scheduled execution using GitHub Actions
---

# 🔄 Project Workflow

```text
                 IMD Website
                      │
                      ▼
           Detect Latest PDF Report
                      │
                      ▼
              Download PDF File
                      │
                      ▼
               Validate PDF Format
                      │
                      ▼
             Extract Complete Text
                      │
                      ▼
             Extract Report Date
                      │
                      ▼
        Check Local Archive Database
               │               │
               │               │
         Already Exists     New Report
               │               │
               ▼               ▼
         Stop Program     Parse Rainfall Data
                               │
                               ▼
                       Generate CSV File
                               │
                               ▼
                     Update Archive Database
                               │
                               ▼
                     Git Commit and Push
                               │
                               ▼
                     GitHub Repository Updated
```
---

# 📂 Project Structure

```text
IMD_Rainfall_Project/
│
├── .github/
│   └── workflows/
│       └── daily_download.yml
│
├── archive/
│   ├── csv/
│   ├── pdf/
│   ├── logs/
│   └── temp/
│
├── config.py
├── downloader.py
├── parser.py
├── database.py
├── git_utils.py
├── requirements.txt
├── README.md
└── .gitignore
```
---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/varap0276-max/IMD_Rainfall_Archive2.git
```

Move into the project directory

```bash
cd IMD_Rainfall_Archive2
```

Install the required packages

```bash
pip install -r requirements.txt
```
---

# ▶️ Usage

Run the project using:

```bash
python downloader.py
```

The application will:

1. Connect to the IMD website.
2. Detect the latest rainfall report.
3. Download the latest PDF.
4. Extract rainfall statistics.
5. Generate a CSV archive.
6. Update the local database.
7. Commit and push changes to GitHub automatically.

---

# ⚡ GitHub Actions

This project supports automated execution using **GitHub Actions**.

The workflow is located at:

```text
.github/workflows/daily_download.yml
```

The workflow automatically:

- Sets up Python
- Installs all required dependencies
- Executes the downloader
- Updates the rainfall archive
- Pushes new data to GitHub

The workflow can be triggered manually or scheduled using a cron job.

---

# 🛠️ Technologies Used

- Python 3
- Requests
- BeautifulSoup4
- pdfplumber
- SQLite
- CSV
- Regular Expressions (re)
- Git
- GitHub
- GitHub Actions

---

# 🚀 Future Improvements

- Daily automatic execution using cron scheduling
- Email notification after successful archive updates
- Interactive rainfall dashboard
- Historical rainfall analytics
- REST API for rainfall data access
- Data visualization using Plotly or Dash

---

# 👨‍💻 Author

**L K S V Prasad Sallangi**

M.Tech in Water Resources Engineering

Indian Institute of Technology Hyderabad

GitHub:
https://github.com/varap0276-max