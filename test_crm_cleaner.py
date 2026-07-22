import unittest
import pandas as pd
from crm_cleaner import clean_email, format_phone, clean_crm_data

class TestCRMCleaner(unittest.TestCase):

    def test_clean_email_valid(self):
        """Test valid email cleaning and lowercasing."""
        self.assertEqual(clean_email("  USER@EXAMPLE.COM "), "user@example.com")

    def test_clean_email_invalid(self):
        """Test malformed email rejection."""
        self.assertIsNone(clean_email("invalid-email-address"))
        self.assertIsNone(clean_email("user@domain"))

    def test_format_phone_ten_digits(self):
        """Test 10-digit US phone formatting."""
        self.assertEqual(format_phone("5550192831"), "(555) 019-2831")
        self.assertEqual(format_phone("555-019-2831"), "(555) 019-2831")

    def test_format_phone_eleven_digits(self):
        """Test 11-digit US phone formatting with country code."""
        self.assertEqual(format_phone("15550192831"), "(555) 019-2831")

    def test_clean_crm_data_pipeline(self):
        """Test full dataframe cleaning pipeline and deduplication."""
        raw_data = {
            "first_name": [" john ", "john "],
            "last_name": ["doe", "doe"],
            "email": ["JOHN@EXAMPLE.COM", "john@example.com"],
            "phone": ["5550192831", "555-019-2831"]
        }
        df_raw = pd.DataFrame(raw_data)
        df_cleaned = clean_crm_data(df_raw)
        
        # Pipeline should deduplicate and keep 1 record
        self.assertEqual(len(df_cleaned), 1)
        self.assertEqual(df_cleaned.iloc[0]["first_name"], "John")

if __name__ == "__main__":
    unittest.main()
