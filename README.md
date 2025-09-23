📊 Multi-Step Statement Processor

**A Streamlit web app for automating finance statement reconciliation in three easy steps:**

Merge & Tag – Combine statement and reference files, classify records as matched or unmatched, and apply business enrichment rules.
 PO Check – Cross-check POs against a reference list to flag missing ones.
Remittance Merge – Merge processed statements with remittance data for final reconciliation.

**🚀 Features**

File Uploads: Supports Excel (.xlsx) files.

Smart Merging: Tags records as Matched / Unmatched.

Custom Business Rules: Example calculation (Amount * 10%) + flagging thresholds.

PO Presence Validation: Quickly check if POs exist in reference datasets.

Final Reconciliation: Merge with remittance to prepare final output.

Excel Exports: Download processed outputs at each stage.

Interactive UI: Built using Streamlit

📦 statement-processor
 ┣ 📜 app.py               # Streamlit app
 
 ┣ 📜 requirements.txt     # Dependencies
 
 ┣ 📜 README.md            # Project description
 
 ┣ 📂 sample_data          # Example input files
 
 ┗ 📂 screenshots          # App screenshots

**🛠️ Tech Stack**

Python 3.9+

Streamlit for UI

Pandas for data manipulation

XlsxWriter for Excel exports

**📊 Sample Workflow**

**Step 1 – Merge & Tag**
Upload Statement + Reference → App merges → Tags as Matched/Unmatched → Adds calculated field + flag.

**Step 2 – PO Check**
Upload a file with PO column → App validates and flags POs as Exists or Missing.

**Step 3 – Remittance Merge**
Upload Remittance File → App merges by PO → Creates final reconciled dataset.

