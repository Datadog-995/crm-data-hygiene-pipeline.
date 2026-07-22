import unittest
import pandas as pd
from pos_reconciler import process_pos_summary

class TestPOSReconciler(unittest.TestCase):

    def setUp(self):
        """Set up dummy POS sales data for testing."""
        data = {
            'transaction_id': ['TXN-1', 'TXN-2'],
            'payment_method': ['Credit Card', 'Cash'],
            'gross_sales': [100.0, 50.0],
            'discounts': [10.0, 0.0],
            'tax_collected': [8.0, 4.0],
            'tips': [15.0, 5.0],
            'processing_fee': [3.20, 0.0],
            'net_amount': [112.80, 59.0]
        }
        self.df_raw = pd.DataFrame(data)

    def test_journal_entry_balance(self):
        """Verify that Total Debits equal Total Credits in the generated Journal Entry."""
        df_je = process_pos_summary(self.df_raw)
        total_debits = round(df_je['Debit'].sum(), 2)
        total_credits = round(df_je['Credit'].sum(), 2)
        self.assertEqual(total_debits, total_credits)

    def test_fee_deduction(self):
        """Verify merchant processing fee is tracked in debits."""
        df_je = process_pos_summary(self.df_raw)
        fee_row = df_je[df_je['GL_Account'].str.contains('Processing Fees')]
        self.assertEqual(fee_row.iloc[0]['Debit'], 3.20)

if __name__ == "__main__":
    unittest.main()
