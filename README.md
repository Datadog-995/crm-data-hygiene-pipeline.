# CRM Data Hygiene & Lead Audit Pipeline

An automated Python data engineering pipeline designed to clean, standardize, and audit messy e-commerce and CRM sales lead datasets.

## Key Features
* **Email Hygiene & Syntax Validation:** Trims whitespace, standardizes casing, and validates proper email syntax using regular expressions.
* **Phone Number Standardization:** Strips non-numeric characters and converts valid US phone numbers into clean standard formats `(XXX) XXX-XXXX`.
* **Text Field Normalization:** Trims trailing/leading spaces and standardizes name casing across lead fields.
* **Deduplication:** Identifies and removes duplicate records based on primary key fields to maintain data integrity.

## Tech Stack & Requirements
* **Language:** Python 3.x
* **Libraries:** `pandas`
* **Workflow Automation:** GitHub Actions CI/CD

## Usage & Script Execution

```python
import pandas as pd
from crm_cleaner import clean_crm_data

# Load messy CRM dataset
df_raw = pd.read_csv('sample_dirty_crm_data.csv')

# Execute data hygiene pipeline
df_cleaned = clean_crm_data(df_raw)

# Export cleaned results
df_cleaned.to_csv('cleaned_crm_leads.csv', index=False)
```

## Running Unit Tests
To run automated unit tests across email validation and phone formatting logic:
```bash
python -m unittest test_crm_cleaner.py
```
