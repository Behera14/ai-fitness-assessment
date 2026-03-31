import pandas as pd
import os

# -------------------------------
# 📁 Dynamic Path (PRO)
# -------------------------------
base_path = os.path.dirname(os.path.dirname(__file__))
file_path = os.path.join(base_path, "final_output.csv")

df = pd.read_csv(file_path)

# -------------------------------
# 🧪 Test Cases
# -------------------------------

# Test 1: File should not be empty
assert not df.empty, "❌ Output file is empty"

# Test 2: At least one issue should exist
assert (df["issue"] != "Matched").any(), "❌ No issues detected"

# Test 3: Missing settlement exists
assert "Missing Settlement" in df["issue"].values, "❌ Missing Settlement not detected"

# Test 4: Duplicate detected
assert "Duplicate Entry" in df["issue"].values, "❌ Duplicate not detected"

# Test 5: Rounding issue detected
assert "Rounding Issue" in df["issue"].values, "❌ Rounding issue not detected"

# Test 6: Columns check
expected_cols = {"id", "amount_txn", "amount_bank", "issue"}
assert set(df.columns) == expected_cols, "❌ Columns mismatch"

print("✅ All test cases passed successfully!")