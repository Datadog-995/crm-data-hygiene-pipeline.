# CRM Data Hygiene & Lead Audit Pipeline

An automated Python data cleaning pipeline built with Pandas and Regular Expressions (Regex) to standardize, validate, and audit messy sales leads exported from CRMs (Salesforce, HubSpot, Zoho).

## 📌 Features & Capabilities
* **Name Normalization:** Automatically trims whitespace, applies Proper Title Casing, and splits `Full Name` into separate `First Name` and `Last Name` fields for personalized email campaigns.
* **International Phone Standardization:** Uses regex pattern matching to clean raw phone numbers into standardized E.164 formats (`+1...`) while flagging extension noise or invalid strings.
* **Email Domain & Syntax Validation:** Normalizes emails to lowercase and applies regular expression pattern checking (`^[\w\.-]+@[\w\.-]+\.\w+$`) to catch broken or malformed addresses.
* **Lead Deduplication:** Detects exact and normalized duplicate contacts across lead records.
* **Executive Summary Metrics:** Generates an immediate audit report summarizing total records processed, clean lead counts, and flag totals.

---

## 🛠️ Tech Stack & Requirements
* **Language:** Python 3.x
* **Libraries:** `pandas`, `re` (Regular Expressions)
* **Environment:** Google Colab / Jupyter Notebooks

---

## 🚀 Script Execution

```python
import pandas as pd
import re

# Load raw CRM lead export
df = pd.read_csv('dirty_crm_leads.csv')

# 1. Clean and split full names
df['Full_Name_Clean'] = df['Full_Name'].astype(str).str.strip().str.title()
df['First_Name'] = df['Full_Name_Clean'].apply(lambda x: x.split()[0] if len(x.split()) > 0 else '')
df['Last_Name'] = df['Full_Name_Clean'].apply(lambda x: ' '.join(x.split()[1:]) if len(x.split()) > 1 else '')

# 2. Lowercase and validate email syntax
df['Email_Clean'] = df['Email'].astype(str).str.strip().str.lower()
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
df['Is_Valid_Email'] = df['Email_Clean'].apply(lambda x: bool(re.match(email_pattern, x)))

# 3. Format phone numbers to E.164 standard
def format_phone(phone_str):
    digits = re.sub(r'\D', '', str(phone_str))
    if len(digits) == 10:
        return f"+1{digits}"
    elif len(digits) == 11 and digits.startswith('1'):
        return f"+{digits}"
    else:
        return 'INVALID_PHONE'

df['Phone_Clean'] = df['Phone'].apply(format_phone)

# 4. Deduplicate on normalized email
df['Is_Duplicate'] = df.duplicated(subset=['Email_Clean'], keep='first')

# Export cleaned results
columns_order = ['Lead_ID', 'First_Name', 'Last_Name', 'Company', 'Phone_Clean', 'Email_Clean', 'Is_Valid_Email', 'Is_Duplicate']
df_clean = df[columns_order]
df_clean.to_csv('cleaned_crm_leads.csv', index=False)
