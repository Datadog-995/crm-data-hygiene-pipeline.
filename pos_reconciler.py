import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

GL_ACCOUNT_MAP = {
    'Sales_Revenue': '4000 - Gross Sales Revenue',
    'Discounts': '4100 - Sales Discounts & Returns',
    'Sales_Tax': '2200 - Sales Tax Payable',
    'Tips': '2150 - Employee Tips Payable',
    'Processing_Fees': '6100 - Merchant Processing Fees',
    'Cash_Undeposited': '1010 - Undeposited Funds (Cash)',
    'Card_Clearing': '1020 - Merchant Card Clearing'
}

def process_pos_summary(df):
    """Processes raw daily POS sales transactions and generates a balanced accounting Journal Entry."""
    logging.info("Starting POS-to-Accounting reconciliation pipeline...")
    
    gross_sales = df['gross_sales'].sum()
    discounts = df['discounts'].sum()
    sales_tax = df['tax_collected'].sum()
    tips = df['tips'].sum()
    
    card_sales = df[df['payment_method'] == 'Credit Card']['net_amount'].sum()
    cash_sales = df[df['payment_method'] == 'Cash']['net_amount'].sum()
    processing_fees = df['processing_fee'].sum()
    
    net_card_deposit = card_sales - processing_fees

    journal_entry = [
        {'GL_Account': GL_ACCOUNT_MAP['Card_Clearing'], 'Debit': round(net_card_deposit, 2), 'Credit': 0.0},
        {'GL_Account': GL_ACCOUNT_MAP['Cash_Undeposited'], 'Debit': round(cash_sales, 2), 'Credit': 0.0},
        {'GL_Account': GL_ACCOUNT_MAP['Processing_Fees'], 'Debit': round(processing_fees, 2), 'Credit': 0.0},
        {'GL_Account': GL_ACCOUNT_MAP['Discounts'], 'Debit': round(discounts, 2), 'Credit': 0.0},
        {'GL_Account': GL_ACCOUNT_MAP['Sales_Revenue'], 'Debit': 0.0, 'Credit': round(gross_sales, 2)},
        {'GL_Account': GL_ACCOUNT_MAP['Sales_Tax'], 'Debit': 0.0, 'Credit': round(sales_tax, 2)},
        {'GL_Account': GL_ACCOUNT_MAP['Tips'], 'Debit': 0.0, 'Credit': round(tips, 2)}
    ]
    
    df_je = pd.DataFrame(journal_entry)
    
    total_debits = df_je['Debit'].sum()
    total_credits = df_je['Credit'].sum()
    out_of_balance = round(total_debits - total_credits, 2)
    
    if out_of_balance != 0:
        logging.warning(f"Journal entry out of balance by ${out_of_balance}")
    else:
        logging.info("Journal entry successfully balanced (Debits = Credits).")
        
    return df_je

if __name__ == "__main__":
    logging.info("POS Reconciler initialized.")
