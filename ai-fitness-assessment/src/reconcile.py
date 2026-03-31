import pandas as pd
import os

# -------------------------------
# 📁 Dynamic Path Setup (PRO)
# -------------------------------
base_path = os.path.dirname(os.path.dirname(__file__))

transactions_path = os.path.join(base_path, "data", "transactions.csv")
settlements_path = os.path.join(base_path, "data", "settlements.csv")

# -------------------------------
# 📊 Load Data
# -------------------------------
transactions = pd.read_csv(transactions_path)
settlements = pd.read_csv(settlements_path)

# Convert dates
transactions["date"] = pd.to_datetime(transactions["date"])
settlements["date"] = pd.to_datetime(settlements["date"])

# -------------------------------
# 🔗 Merge Data
# -------------------------------
df = pd.merge(
    transactions,
    settlements,
    on="id",
    how="outer",
    suffixes=("_txn", "_bank")
)

# -------------------------------
# ⚙️ Issue Detection Logic
# -------------------------------
df["issue"] = "Matched"

# Missing transaction
df.loc[df["amount_txn"].isna(), "issue"] = "Missing Transaction"

# Missing settlement
df.loc[df["amount_bank"].isna(), "issue"] = "Missing Settlement"

# Amount mismatch
df.loc[
    (df["amount_txn"].notna()) &
    (df["amount_bank"].notna()) &
    (df["amount_txn"] != df["amount_bank"]),
    "issue"
] = "Amount Mismatch"

# Rounding issue
df.loc[
    (df["amount_txn"].notna()) &
    (df["amount_bank"].notna()) &
    (abs(df["amount_txn"] - df["amount_bank"]) < 0.01),
    "issue"
] = "Rounding Issue"

# Settlement delay (next month)
df.loc[
    (df["date_txn"].notna()) &
    (df["date_bank"].notna()) &
    (df["date_txn"].dt.month != df["date_bank"].dt.month),
    "issue"
] = "Settlement Delay"

# Duplicate entries in bank
duplicates = settlements[settlements.duplicated(subset=["id"], keep=False)]
duplicate_ids = duplicates["id"].unique()
df.loc[df["id"].isin(duplicate_ids), "issue"] = "Duplicate Entry"

# -------------------------------
# 📊 Clean Final Report
# -------------------------------
final_df = df[["id", "amount_txn", "amount_bank", "issue"]]

print("\n🔍 Reconciliation Report:\n")
print(final_df)

# -------------------------------
# 📈 Summary
# -------------------------------
print("\n📊 Issue Summary:\n")
print(final_df["issue"].value_counts())

# -------------------------------
# 💾 Save Output
# -------------------------------
output_path = os.path.join(base_path, "final_output.csv")
final_df.to_csv(output_path, index=False)

print(f"\n✅ Final output saved at: {output_path}")