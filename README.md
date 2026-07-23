# E-Commerce & Retail Data Operations Suite

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Datadog-995/crm-data-hygiene-pipeline./blob/main/notebooks/data_operations_demo.ipynb)

An automated Python data engineering suite featuring specialized pipelines for CRM lead hygiene and POS-to-Accounting financial reconciliation.

---

## 1. CRM Data Hygiene Pipeline

Cleans, standardizes, and audits raw customer/lead exports from CRM platforms (Salesforce, HubSpot, Zoho).

* **Features:** Email syntax validation, phone number formatting, string trimming, proper title casing, and contact deduplication.
* **Script:** `crm_cleaner.py`
* **Sample Data:** `sample_dirty_crm_data.csv`
* **Tests:** `test_crm_cleaner.py`

```python
import pandas as pd
from crm_cleaner import clean_crm_data

df_raw = pd.read_csv('sample_dirty_crm_data.csv')
df_cleaned = clean_crm_data(df_raw)
df_cleaned.to_csv('cleaned_crm_leads.csv', index=False)
```

---

## 2. POS-to-Accounting General Ledger Pipeline

Aggregates raw daily Point-of-Sale transaction logs into balanced double-entry General Ledger journal entries ready for accounting software (QuickBooks, Xero).

* **Features:** Calculates gross revenue, sales tax payable, tip liabilities, and merchant processing fees; verifies $0.00 out-of-balance reconciliation.
* **Script:** `pos_reconciler.py`
* **Sample Data:** `sample_pos_sales.csv`
* **Tests:** `test_pos_reconciler.py`

```python
import pandas as pd
from pos_reconciler import process_pos_summary

df_sales = pd.read_csv('sample_pos_sales.csv')
df_journal_entry = process_pos_summary(df_sales)
df_journal_entry.to_csv('daily_journal_entry.csv', index=False)
```

---

## Running Automated Tests & CI/CD
Run all unit tests locally:
```bash
python -m unittest discover -p "test_*.py"
```
All commits are automatically validated via GitHub Actions CI/CD (`.github/workflows/data_pipeline.yml`).
---

## 🖥️ Recommended Workstation & Hardware Setup
* **Workstation Laptop:** [Apple MacBook Air (M-Series)](https://www.amazon.com/dp/B0CX23AC11/?tag=qualitydata07-20) – Primary development and data pipeline processing machine.
* **External Display:** [4K UHD External Desktop Monitor](https://www.amazon.com/dp/B07YGZL8XF/?tag=qualitydata07-20) – High-resolution workspace for multi-window data auditing.
* **Local Storage & Backups:** [SanDisk 2TB Extreme Portable SSD](https://www.amazon.com/dp/B08GV4YYV7/?tag=qualitydata07-20) – Fast local backup drive for large dataset snapshots and Time Machine.
* **Connectivity:** [Anker USB-C Multi-Port Hub / Dock](https://www.amazon.com/dp/B07ZVKTP53/?tag=qualitydata07-20) – Port expansion for external monitors, power delivery, and drives.
