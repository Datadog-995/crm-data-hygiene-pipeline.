import pandas as pd
import re
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def clean_email(email):
    """Trims whitespace, converts to lowercase, and validates email syntax."""
    if pd.isna(email):
        return None
    email = str(email).strip().lower()
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return email if re.match(email_regex, email) else None

def format_phone(phone):
    """Strips non-numeric characters and formats valid 10-digit US phone numbers."""
    if pd.isna(phone):
        return None
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith("1"):
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return None

def clean_crm_data(df):
    """Executes full hygiene pipeline on incoming raw CRM dataset."""
    logging.info("Starting CRM Data Hygiene Pipeline...")
    initial_rows = len(df)
    
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()
    
    if 'first_name' in df.columns:
        df['first_name'] = df['first_name'].str.title()
    if 'last_name' in df.columns:
        df['last_name'] = df['last_name'].str.title()
        
    if 'email' in df.columns:
        df['email_clean'] = df['email'].apply(clean_email)
        
    if 'phone' in df.columns:
        df['phone_clean'] = df['phone'].apply(format_phone)
        
    df = df.drop_duplicates(subset=['email_clean'], keep='first')
    
    logging.info(f"Pipeline complete. Removed {initial_rows - len(df)} duplicate/invalid records.")
    return df

if __name__ == "__main__":
    logging.info("CRM Cleaner script initialized.")
