import warnings
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker



RAW = "../dataset_03/Raw data"
STAR = "../power_bi/star_schema"
FIGS = "figures"

os.makedirs(STAR, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)

# print("STAR:", os.path.abspath(STAR))


# print(os.listdir(RAW))

#Load the 6 files
complaints = pd.read_csv(os.path.join(RAW, "complaints_raw.csv"))
customers = pd.read_csv(os.path.join(RAW, "customers_raw.csv"))
loans = pd.read_csv(os.path.join(RAW, "loans_raw.csv"))
applications = pd.read_csv(os.path.join(RAW, "loan_applications_raw.csv"))
repayments = pd.read_csv(os.path.join(RAW, "repayments_raw.csv"))
transactions = pd.read_csv(os.path.join(RAW, "transactions_raw.csv"))
branches= pd.read_csv(os.path.join(RAW , "branches.csv"))
products= pd.read_csv(os.path.join(RAW , "products.csv"))
targets= pd.read_csv(os.path.join(RAW , "monthly_targets.csv"))

# print("All 9 files loaded successfully.")


#Check the number of rows
print("Complaints:", complaints.shape)
print("Customers:", customers.shape)
print("Loans:", loans.shape)
print("Applications:", applications.shape)
print("Repayments:", repayments.shape)
print("Transactions:", transactions.shape)


# Check data types
print("\nCustomers:")
print(customers.dtypes)

print("\nApplications:")
print(applications.dtypes)

print("\nLoans:")
print(loans.dtypes)

print("\nRepayments:")
print(repayments.dtypes)

print("\nTransactions:")
print(transactions.dtypes)

print("\nComplaints:")
print(complaints.dtypes)

#Check missing values
print("\nCustomers missing values:")
print(customers.isna().sum())

print("\nApplications missing values:")
print(applications.isna().sum())

print("\nLoans missing values:")
print(loans.isna().sum())

print("\nRepayments missing values:")
print(repayments.isna().sum())

print("\nTransactions missing values:")
print(transactions.isna().sum())

print("\nComplaints missing values:")
print(complaints.isna().sum())


#duplicate rows
print("Customers duplicates:", customers.duplicated().sum())
print("Applications duplicates:", applications.duplicated().sum())
print("Loans duplicates:", loans.duplicated().sum())
print("Repayments duplicates:", repayments.duplicated().sum())
print("Transactions duplicates:", transactions.duplicated().sum())
print("Complaints duplicates:", complaints.duplicated().sum())


#first 5 rows
print("\nCUSTOMERS:")
print(customers.head())

print("\nAPPLICATIONS:")
print(applications.head())

print("\nLOANS:")
print(loans.head())

print("\nREPAYMENTS:")
print(repayments.head())

print("\nTRANSACTIONS:")
print(transactions.head())

print("\nCOMPLAINTS:")
print(complaints.head())

#loan value
print("Loan status:")
print(loans["loan_status"].value_counts(dropna=False))

print("\nLoan channel:")
print(loans["channel"].value_counts(dropna=False))

print("\nLoan NPA flag:")
print(loans["npa_flag"].value_counts(dropna=False))


#important numeric columns
print("Disbursed amount:")
print(loans["disbursed_amount"].describe())

print("\nOutstanding principal:")
print(loans["outstanding_principal"].describe())

print("\nDPD days:")
print(loans["dpd_days"].describe())

print("\nBureau score:")
print(loans["bureau_score_at_disbursal"].describe())


#invalid/negative values
print("Negative disbursed amounts:",
      (loans["disbursed_amount"] < 0).sum())

print("Negative outstanding principal:",
      (loans["outstanding_principal"] < 0).sum())

print("Negative DPD days:",
      (loans["dpd_days"] < 0).sum())

print("Invalid bureau scores:",
      ((loans["bureau_score_at_disbursal"] < 300) |
       (loans["bureau_score_at_disbursal"] > 900)).sum())



# #date columns
print(loans[["disbursal_date", "first_emi_date"]].head())

print("\nData types:")
print(loans[["disbursal_date", "first_emi_date"]].dtypes)


# the snapshot date
SNAPSHOT_DATE = pd.Timestamp("2026-06-30")
print("Snapshot date:", SNAPSHOT_DATE)

print("Loans after snapshot date:",
      (pd.to_datetime(loans["disbursal_date"], errors="coerce") > SNAPSHOT_DATE).sum())

print("First EMI dates after snapshot:",
      (pd.to_datetime(loans["first_emi_date"], errors="coerce") > SNAPSHOT_DATE).sum())



#Check all six datasets for missing values
datasets = {
    "Customers": customers,
    "Applications": applications,
    "Loans": loans,
    "Repayments": repayments,
    "Transactions": transactions,
    "Complaints": complaints
}

for name, df in datasets.items():
    print(f"\n{name}")
    print("Rows:", len(df))
    print("Missing values:", df.isna().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())

# Check duplicate loan IDs
print("\nDuplicate loan IDs:",
      loans["loan_id"].duplicated().sum())

# Check negative loan amounts
print("Negative disbursed amounts:",
      (loans["disbursed_amount"] < 0).sum())

print("Negative outstanding principal:",
      (loans["outstanding_principal"] < 0).sum())



 #Detailed data-quality checks

for name, df in datasets.items():
    print(f"\n--- {name.upper()} ---")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Missing values:", df.isna().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())


# Loan-specific quality checks

loan_df = loans.copy()

print("\n===== LOAN QUALITY CHECKS =====")

print("Missing loan IDs:",
      loan_df["loan_id"].isna().sum())

print("Duplicate loan IDs:",
      loan_df["loan_id"].duplicated().sum())

print("Missing customer IDs:",
      loan_df["customer_id"].isna().sum())

print("Missing loan status:",
      loan_df["loan_status"].isna().sum())

print("Negative disbursed amounts:",
      (pd.to_numeric(loan_df["disbursed_amount"], errors="coerce") < 0).sum())

print("Negative outstanding principal:",
      (pd.to_numeric(loan_df["outstanding_principal"], errors="coerce") < 0).sum())



#Step 10: Create cleaned copies

raw = {
    "customers": customers,
    "applications": applications,
    "loans": loans,
    "repayments": repayments,
    "transactions": transactions,
    "complaints": complaints
}

clean = {}

for name, df in raw.items():
    clean[name] = df.copy()

    # Remove extra spaces from column names
    clean[name].columns = clean[name].columns.str.strip()

    # Remove extra spaces from text values
    for col in clean[name].select_dtypes(include=["object"]).columns:
        clean[name][col] = clean[name][col].str.strip()

    print(f"{name}: cleaned copy created — {len(clean[name])} rows")

print("\n===== CLEANING VERIFICATION =====")

for name in raw:
    print(
        name,
        "| Raw rows:", len(raw[name]),
        "| Clean rows:", len(clean[name])
    )


# Step 11A: Validate loan data

loan_df = clean["loans"]

SNAPSHOT_DATE = pd.Timestamp("2026-06-30")

# Convert numeric columns safely
numeric_cols = [
    "sanctioned_amount",
    "disbursed_amount",
    "interest_rate",
    "tenure_months",
    "emi_amount",
    "bureau_score_at_disbursal",
    "outstanding_principal",
    "total_amount_paid",
    "dpd_days"
]

for col in numeric_cols:
    loan_df[col] = pd.to_numeric(loan_df[col], errors="coerce")

# print("\n===== LOAN VALIDATION =====")
print("Total loan rows:", len(loan_df))
print("Invalid disbursed amounts:", loan_df["disbursed_amount"].isna().sum())
print("Negative disbursed amounts:", (loan_df["disbursed_amount"] < 0).sum())
print("Negative outstanding principal:", (loan_df["outstanding_principal"] < 0).sum())
print("Negative DPD days:", (loan_df["dpd_days"] < 0).sum())

# Convert dates safely
loan_df["disbursal_date"] = pd.to_datetime(
    loan_df["disbursal_date"], errors="coerce"
)
loan_df["first_emi_date"] = pd.to_datetime(
    loan_df["first_emi_date"], errors="coerce"
)

print("Invalid disbursal dates:", loan_df["disbursal_date"].isna().sum())
print("Loans after snapshot date:",
      (loan_df["disbursal_date"] > SNAPSHOT_DATE).sum())

# Step 12: Validate loan dates and records

loan_df = clean["loans"]

SNAPSHOT_DATE = pd.Timestamp("2026-06-30")

print("\n===== LOAN DATE VALIDATION =====")

print("Missing loan IDs:",
      loan_df["loan_id"].isna().sum())

print("Duplicate loan IDs:",
      loan_df["loan_id"].duplicated().sum())

print("Invalid disbursal dates:",
      loan_df["disbursal_date"].isna().sum())

print("Loans disbursed after snapshot:",
      (loan_df["disbursal_date"] > SNAPSHOT_DATE).sum())

print("First EMI dates before disbursal:",
      (loan_df["first_emi_date"] < loan_df["disbursal_date"]).sum())

print("\nLoan date validation completed.")


# Step 13: Create loan risk categories

loan_df = clean["loans"]

# Categorize loans by Days Past Due (DPD)
loan_df["dpd_bucket"] = np.select(
    [
        loan_df["dpd_days"].isna(),
        loan_df["dpd_days"] <= 0,
        loan_df["dpd_days"] <= 30,
        loan_df["dpd_days"] <= 60,
        loan_df["dpd_days"] <= 90,
        loan_df["dpd_days"] > 90
    ],
    [
        "Unknown",
        "Current",
        "1-30 Days",
        "31-60 Days",
        "61-90 Days",
        "90+ Days"
    ],
    default="Unknown"
)

# Standardize NPA flag
loan_df["npa_flag_clean"] = (
    loan_df["npa_flag"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# # Display results
print("\n===== DPD RISK SUMMARY =====")
print(loan_df["dpd_bucket"].value_counts(dropna=False))

print("\n===== NPA FLAG SUMMARY =====")
print(loan_df["npa_flag_clean"].value_counts(dropna=False))

print("\nTotal loan rows retained:", len(loan_df))


# Step 14: Create loan data-quality flags

loan_df = clean["loans"]

loan_df["dq_missing_loan_id"] = loan_df["loan_id"].isna()

loan_df["dq_duplicate_loan_id"] = loan_df["loan_id"].duplicated(keep="first")

loan_df["dq_negative_disbursed_amount"] = (
    loan_df["disbursed_amount"] < 0
)

loan_df["dq_negative_outstanding"] = (
    loan_df["outstanding_principal"] < 0
)

loan_df["dq_negative_dpd"] = loan_df["dpd_days"] < 0

loan_df["dq_invalid_bureau_score"] = (
    (loan_df["bureau_score_at_disbursal"] < 300) |
    (loan_df["bureau_score_at_disbursal"] > 900)
)

# Count each quality issue
dq_columns = [
    "dq_missing_loan_id",
    "dq_duplicate_loan_id",
    "dq_negative_disbursed_amount",
    "dq_negative_outstanding",
    "dq_negative_dpd",
    "dq_invalid_bureau_score"
]

print("\n===== LOAN DATA QUALITY FLAGS =====")

# for col in dq_columns:
print(f"{col}: {int(loan_df[col].sum())}")

print("\nTotal loan rows retained:", len(loan_df))


# Section 2: Load the raw extracts

raw = {}


FILES = {
    "customers": "customers_raw.csv",
    "applications": "loan_applications_raw.csv",
    "loans": "loans_raw.csv",
    "repayments": "repayments_raw.csv",
    "transactions": "transactions_raw.csv",
    "complaints": "complaints_raw.csv",
    "branches": "branches.csv",
    "products": "products.csv",
    "targets": "monthly_targets.csv"
}


for k, f in FILES.items():
    filepath = os.path.join(RAW, f)

    raw[k] = pd.read_csv(
        filepath,
        dtype=str,
        keep_default_na=False,
        na_values=[""]
    )

    print(
        f"{k:14s} {raw[k].shape[0]:>7,} rows x "
        f"{raw[k].shape[1]:>2} cols"
    )

# Section 2.1: Profile raw datasets

def profile(df, name=""):
    """One row per column: nulls, distinct values, and a sample value."""

    out = pd.DataFrame({
        "column": df.columns,
        "non_null": df.notna().sum().values,
        "null_count": df.isna().sum().values,
        "null_pct": (100 * df.isna().mean().values).round(2),
        "distinct": [df[c].nunique(dropna=True) for c in df.columns],
        "sample": [
            df[c].dropna().iloc[0] if df[c].notna().any() else None
            for c in df.columns
        ],
    })

    out.insert(0, "source", name)
    return out


# Profile the customers dataset
customer_profile = profile(raw["customers"], "customers")
print("\n===== CUSTOMER DATA PROFILE =====")
print(customer_profile.to_string(index=False))

# Section 2.2: Check duplicate business keys

KEYS = {
    "customers": "customer_id",
    "applications": "application_id",
    "loans": "loan_id",
    "repayments": "repayment_id",
    "transactions": "transaction_id",
    "complaints": "complaint_id"
}

dupe_report = pd.DataFrame([
    {
        "source": k,
        "rows": len(raw[k]),
        "distinct_keys": raw[k][v].str.strip().nunique(),
        "duplicate_rows": len(raw[k]) - raw[k][v].str.strip().nunique()
    }
    for k, v in KEYS.items()
])

print("\n===== DUPLICATE BUSINESS KEY REPORT =====")
print(dupe_report.to_string(index=False))

# Section 3: Data-quality assessment

dq = []

def flag(source, column, issue, n, treatment):
    dq.append({
        "source": source,
        "column": column,
        "issue": issue,
        "rows_affected": int(n),
        "treatment": treatment
    })


# Helper: find a column using possible names
def find_col(df, candidates):
    lookup = {c.lower().strip(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    return None


# Helper: safely convert text to numbers
def to_num(series):
    return pd.to_numeric(
        series.astype("string")
        .str.strip()
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace("%", "", regex=False),
        errors="coerce"
    )


# Helper: count duplicate nonblank keys
def duplicate_key_count(series):
    s = series.astype("string").str.strip()
    s = s[s.notna() & s.ne("")]
    return int(s.duplicated().sum())


# --------------------------------------------------
# 1. CUSTOMERS
# --------------------------------------------------

df = raw["customers"]

gender_col = find_col(df, ["gender", "sex"])
if gender_col:
    gender = df[gender_col].astype("string").str.strip().str.lower()
    valid_gender = [
        "m", "f", "male", "female", "other",
        "non-binary", "nonbinary", "unknown", "prefer not to say"
    ]
    invalid = gender.notna() & gender.ne("") & ~gender.isin(valid_gender)

    flag(
        "customers", gender_col, "Unrecognized gender encoding",
        invalid.sum(), "Standardize valid encodings; investigate other values"
    )

date_col = find_col(df, [
    "date_of_birth", "dob", "created_date",
    "registration_date", "customer_since"
])
if date_col:
    values = df[date_col].astype("string").str.strip()
    parsed = pd.to_datetime(values, errors="coerce", format="mixed")
    invalid = values.notna() & values.ne("") & parsed.isna()

    flag(
        "customers", date_col, "Unparseable date values",
        invalid.sum(), "Standardize date formats and investigate invalid dates"
    )

income_col = find_col(df, [
    "income", "annual_income", "monthly_income"
])
if income_col:
    income = df[income_col].astype("string").str.strip()
    numeric_income = to_num(income)
    invalid = income.notna() & income.ne("") & numeric_income.isna()

    flag(
        "customers", income_col, "Income stored in nonnumeric format",
        invalid.sum(), "Standardize currency/text formatting before conversion"
    )

customer_key = find_col(df, ["customer_id"])
if customer_key:
    flag(
        "customers", customer_key, "Duplicate customer IDs",
        duplicate_key_count(df[customer_key]),
        "Investigate duplicates; preserve original records"
    )


# --------------------------------------------------
# 2. LOANS
# --------------------------------------------------

df = raw["loans"]

npa_col = find_col(df, ["npa_flag"])
if npa_col:
    npa = df[npa_col].astype("string").str.strip().str.lower()
    valid_npa = ["yes", "no", "y", "n", "true", "false", "1", "0"]
    invalid = npa.notna() & npa.ne("") & ~npa.isin(valid_npa)

    flag(
        "loans", npa_col, "Unrecognized NPA flag encoding",
        invalid.sum(), "Standardize valid flags; investigate other values"
    )

rate_col = find_col(df, ["interest_rate"])
if rate_col:
    rate = df[rate_col].astype("string").str.strip()
    has_percent = rate.str.contains("%", na=False)

    flag(
        "loans", rate_col, "Interest rate contains percent symbols",
        has_percent.sum(), "Remove percent symbols and standardize units"
    )

emi_col = find_col(df, ["emi_amount", "emi"])
if emi_col:
    emi = df[emi_col].astype("string").str.strip()
    missing = emi.isna() | emi.eq("")

    flag(
        "loans", emi_col, "Missing EMI amount",
        missing.sum(), "Validate and calculate only where source fields support it"
    )

loan_key = find_col(df, ["loan_id"])
if loan_key:
    flag(
        "loans", loan_key, "Duplicate loan IDs",
        duplicate_key_count(df[loan_key]),
        "Investigate duplicate IDs; do not delete rows automatically"
    )

loan_customer = find_col(df, ["customer_id"])
customer_ids = raw["customers"]

customer_key = find_col(customer_ids, ["customer_id"])

if loan_customer and customer_key:
    known_customers = set(
        customer_ids[customer_key].astype("string").str.strip()
    )
    loan_ids = df[loan_customer].astype("string").str.strip()
    orphan = (
        loan_ids.notna() & loan_ids.ne("") &
        ~loan_ids.isin(known_customers)
    )

    flag(
        "loans", loan_customer, "Customer ID not found in customers",
        orphan.sum(), "Investigate missing customer records or incorrect references"
    )

disbursed_col = find_col(df, ["disbursed_amount"])
sanctioned_col = find_col(df, ["sanctioned_amount"])

if disbursed_col and sanctioned_col:
    disbursed = to_num(df[disbursed_col])
    sanctioned = to_num(df[sanctioned_col])
    invalid = disbursed.notna() & sanctioned.notna() & (
        disbursed > sanctioned
    )

    flag(
        "loans", disbursed_col, "Disbursed amount exceeds sanctioned amount",
        invalid.sum(), "Verify loan amendments and source amounts"
    )


# --------------------------------------------------
# 3. REPAYMENTS
# --------------------------------------------------

df = raw["repayments"]

paid_col = find_col(df, ["paid_amount", "amount_paid"])
due_col = find_col(df, ["due_amount", "amount_due", "scheduled_amount"])

if paid_col:
    paid = to_num(df[paid_col])

    flag(
        "repayments", paid_col, "Negative paid amount",
        (paid < 0).sum(), "Verify reversals, refunds, and source transactions"
    )

if paid_col and due_col:
    paid = to_num(df[paid_col])
    due = to_num(df[due_col])

    # Flag payments more than 10% above a positive due amount
    unusually_high = (
        paid.notna() & due.notna() & (due > 0) &
        (paid > due * 1.10)
    )

    flag(
        "repayments", paid_col, "Paid amount exceeds due by more than 10%",
        unusually_high.sum(), "Investigate advance payments, excess payments, or errors"
    )

flag(
    "repayments", "all columns", "Duplicate repayment rows",
    df.duplicated().sum(), "Investigate exact duplicate records"
)


# --------------------------------------------------
# 4. TRANSACTIONS
# --------------------------------------------------

df = raw["transactions"]

date_col = find_col(df, [
    "transaction_date", "txn_date", "transaction_timestamp",
    "created_at", "transaction_datetime"
])

if date_col:
    dates = pd.to_datetime(df[date_col], errors="coerce", format="mixed")
    future = dates.notna() & (dates > SNAPSHOT_DATE)

    flag(
        "transactions", date_col, "Transaction date after snapshot",
        future.sum(), "Verify timestamps against the June 30, 2026 snapshot"
    )

amount_col = find_col(df, [
    "amount", "transaction_amount", "txn_amount"
])

if amount_col:
    amount = to_num(df[amount_col])

    flag(
        "transactions", amount_col, "Negative transaction amount",
        (amount < 0).sum(), "Investigate reversals, refunds, and source errors"
    )

flag(
    "transactions", "all columns", "Duplicate transaction rows",
    df.duplicated().sum(), "Investigate exact duplicate records"
)



# FINAL REPORT


dq_report = pd.DataFrame(
    dq,
    columns=[
        "source", "column", "issue",
        "rows_affected", "treatment"
    ]
)

dq_report = dq_report.sort_values(
    "rows_affected",
    ascending=False
).reset_index(drop=True)

print("\n===== DATA QUALITY ASSESSMENT =====")
print(dq_report.to_string(index=False))

dq_report.to_csv(
    os.path.join(FIGS, "data_quality_report.csv"),
    index=False
)

print("\nSaved: data_quality_report.csv")


# Section 4.1: Parse mixed date formats

def parse_mixed_dates(s):
    """Parse YYYY-MM-DD, DD-MM-YYYY and DD/MM/YYYY formats."""

    values = s.astype("string").str.strip()

    # Start with missing dates
    result = pd.Series(
        pd.NaT,
        index=s.index,
        dtype="datetime64[ns]"
    )

    # Format 1: YYYY-MM-DD
    mask_iso = values.str.match(
        r"^\d{4}-\d{2}-\d{2}$",
        na=False
    )
    result.loc[mask_iso] = pd.to_datetime(
        values.loc[mask_iso],
        format="%Y-%m-%d",
        errors="coerce"
    )

    # Format 2: DD-MM-YYYY
    mask_dash = values.str.match(
        r"^\d{2}-\d{2}-\d{4}$",
        na=False
    )
    result.loc[mask_dash] = pd.to_datetime(
        values.loc[mask_dash],
        format="%d-%m-%Y",
        errors="coerce"
    )

    # Format 3: DD/MM/YYYY
    mask_slash = values.str.match(
        r"^\d{2}/\d{2}/\d{4}$",
        na=False
    )
    result.loc[mask_slash] = pd.to_datetime(
        values.loc[mask_slash],
        format="%d/%m/%Y",
        errors="coerce"
    )

    return result


# Test the function
_probe = pd.Series([
    "2024-03-05",
    "05-03-2024",
    "05/03/2024",
    "",
    None
])

print("\n===== MIXED DATE PARSING TEST =====")
print(pd.DataFrame({
    "raw": _probe,
    "parsed": parse_mixed_dates(_probe)
}).to_string(index=False))


#Section 4.2 — Customers
import re

def to_num(s):
    """Convert text money/number values to numeric values."""
    def convert(value):
        if pd.isna(value) or str(value).strip() == "":
            return np.nan

        value = str(value).strip()
        is_percent = "%" in value

        # Remove currency labels, commas, spaces and percent signs
        value = re.sub(r"(?i)rs\.?|inr|₹|,", "", value)
        value = value.replace("%", "").strip()

        try:
            return float(value)
        except ValueError:
            return np.nan

    return s.apply(convert)


def clean_customers(df):
    """Clean customer data and return one row per customer."""
    df = df.copy()

    # Strip whitespace from IDs
    if "customer_id" in df.columns:
        df["customer_id"] = df["customer_id"].astype("string").str.strip()

    # Customer name
    if "customer_name" in df.columns:
        df["customer_name"] = (
            df["customer_name"].astype("string").str.strip().str.title()
        )

    # Gender standardization
    if "gender" in df.columns:
        gender_map = {
            "m": "Male", "male": "Male", "man": "Male",
            "f": "Female", "female": "Female", "woman": "Female",
        }
        df["gender"] = (
            df["gender"].astype("string").str.strip().str.lower()
            .map(gender_map).fillna("Unknown")
        )

    # Parse dates using your Section 4.1 function
    for col in ["date_of_birth", "relationship_start_date"]:
        if col in df.columns:
            df[col] = parse_mixed_dates(df[col])

    # City and state
    for col in ["city", "state"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip().str.title()

    # Controlled vocabulary: occupation
    if "occupation" in df.columns:
        occupation_map = {
            "salaried": "Salaried",
            "self employed": "Self-Employed",
            "self-employed": "Self-Employed",
            "business": "Business",
            "business owner": "Business",
            "student": "Student",
            "retired": "Retired",
            "unemployed": "Unemployed",
            "homemaker": "Homemaker",
            "housewife": "Homemaker",
        }
        original = df["occupation"].astype("string").str.strip().str.lower()
        df["occupation"] = original.map(occupation_map).fillna("Other")
        df.loc[original.isna() | original.eq(""), "occupation"] = "Unknown"

    # Controlled vocabulary: KYC status
    if "kyc_status" in df.columns:
        kyc_map = {
            "verified": "Verified",
            "complete": "Verified",
            "completed": "Verified",
            "approved": "Verified",
            "pending": "Pending",
            "in progress": "Pending",
            "in-progress": "Pending",
            "rejected": "Rejected",
            "failed": "Rejected",
            "incomplete": "Incomplete",
        }
        original = df["kyc_status"].astype("string").str.strip().str.lower()
        df["kyc_status"] = original.map(kyc_map).fillna("Unknown")
        df.loc[original.isna() | original.eq(""), "kyc_status"] = "Unknown"

    # Monthly income
    if "monthly_income" in df.columns:
        df["monthly_income"] = to_num(df["monthly_income"])
        df.loc[df["monthly_income"] <= 0, "monthly_income"] = np.nan

    # Mobile: keep last 10 digits and validate
    if "mobile_number" in df.columns:
        def clean_mobile(value):
            if pd.isna(value):
                return pd.NA
            digits = re.sub(r"\D", "", str(value))
            if not digits:
                return pd.NA
            return digits[-10:]

        df["mobile_number"] = df["mobile_number"].apply(clean_mobile)
        df["is_valid_mobile"] = df["mobile_number"].apply(
            lambda x: bool(re.fullmatch(r"[6-9]\d{9}", str(x)))
            if pd.notna(x) else False
        )

    # Email: lowercase and validate
    if "email" in df.columns:
        df["email"] = df["email"].astype("string").str.strip().str.lower()
        df.loc[df["email"].eq(""), "email"] = pd.NA
        df["is_valid_email"] = df["email"].apply(
            lambda x: bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", str(x)))
            if pd.notna(x) else False
        )

    # Pincode: keep only six-digit values
    if "pincode" in df.columns:
        df["pincode"] = df["pincode"].apply(
            lambda x: (
                re.sub(r"\D", "", str(x))
                if pd.notna(x) else ""
            )
        )
        df["pincode"] = df["pincode"].apply(
            lambda x: x if re.fullmatch(r"\d{6}", x) else pd.NA
        )

    # Remove rows without a customer ID and drop duplicate IDs
    if "customer_id" in df.columns:
        missing_id = df["customer_id"].isna() | df["customer_id"].eq("")
        print("Rows with missing customer_id:", int(missing_id.sum()))
        df = df.loc[~missing_id].copy()

        before = len(df)
        df = df.drop_duplicates(subset=["customer_id"], keep="first")
        print("Duplicate customer rows removed:", before - len(df))

    return df


cust = clean_customers(raw["customers"])
print("Clean customer shape:", cust.shape)
print(cust.head(3))


#4.3 Applications
CHANNEL_MAP = {
    "branch": "Branch Walk-in",
    "branch walk-in": "Branch Walk-in",
    "branch walk in": "Branch Walk-in",
    "dsa": "DSA",
    "direct sales agent": "DSA",
    "digital": "Digital App",
    "digital app": "Digital App",
    "website": "Website",
    "online": "Website",
    "telecalling": "Telecalling",
    "tele calling": "Telecalling",
    "partner referral": "Partner Referral",
    "partner": "Partner Referral"
}

STATUS_MAP = {
    "approved": "Approved",
    "approve": "Approved",
    "rejected": "Rejected",
    "declined": "Rejected",
    "pending": "Pending",
    "in review": "Pending",
    "in-review": "Pending",
    "under review": "Pending",
    "submitted": "Pending",
    "disbursed": "Approved",
    "withdrawn": "Withdrawn"
}


def clean_applications(df):
    # existing checks ...

    # Standardize status
    if "application_status" in df.columns:
        original = df["application_status"].str.lower()
        df["application_status"] = original.map(STATUS_MAP)
        
        if df["application_status"].isna().any():
            print("Unmapped statuses:")
            print(original[df["application_status"].isna()].unique())
            raise ValueError("Update STATUS_MAP for unmapped statuses")


    # Convert requested amount
    if "requested_amount" in df.columns:
        df["requested_amount"] = to_num(df["requested_amount"])

    # Parse dates
    for col in ["application_date", "decision_date"]:
        if col in df.columns:
            df[col] = parse_mixed_dates(df[col])
    df["is_approved"] = df["application_status"].eq("Approved")
    df["is_decided"] = df["application_status"].isin(["Approved", "Rejected"])

    # ...remaining cleanup steps...

    return df


# print("Available application statuses:")
# print(raw["applications"]["application_status"].value_counts(dropna=False))
apps = clean_applications(raw["applications"])
# print(apps["application_status"].value_counts(dropna=False))
# print(apps.head(3))

#4.4 Loans

def emi(principal, annual_rate_pct, months):
    """Calculate monthly EMI."""
    if pd.isna(principal) or pd.isna(annual_rate_pct) or pd.isna(months):
        return np.nan

    principal = float(principal)
    rate = float(annual_rate_pct) / 1200
    months = int(months)

    if principal <= 0 or months <= 0 or rate < 0:
        return np.nan

    if rate == 0:
        return principal / months

    return (
        principal * rate * (1 + rate) ** months
        / ((1 + rate) ** months - 1)
    )


LOAN_CHANNEL_MAP = CHANNEL_MAP.copy()

LOAN_STATUS_MAP = {
    "active": "Active",
    "closed": "Closed",
    "fully paid": "Closed",
    "overdue": "Overdue",
    "npa": "NPA",
    "written off": "Written-Off",
    "written-off": "Written-Off",
    "written-off loan": "Written-Off",
    "default": "NPA",
    "disbursed": "Active"
}






def clean_loans(df, customers):
    df = df.copy()

    # Strip ID fields
    for col in ["loan_id", "application_id", "customer_id",
                "product_id", "branch_id"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    # Standardize channel
    original = (
        df["channel"].astype("string").str.strip().str.lower()
    )
    df["channel"] = original.map(LOAN_CHANNEL_MAP)

    if df["channel"].isna().any():
        print(
            "Unmapped loan channels:",
            original[df["channel"].isna()].unique()
        )
        raise ValueError("Update LOAN_CHANNEL_MAP")

    # Standardize loan status
    original_status = (
        df["loan_status"]
        .astype("string")
        .str.strip()
        .str.lower()
    )
    # Standardize NPA flag
    npa_values = (
        df["npa_flag"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    npa_map = {
        "yes": 1,
        "y": 1,
        "1": 1,
        "true": 1,
        "no": 0,
        "n": 0,
        "0": 0,
        "false": 0
    }

    df["is_npa"] = npa_values.map(npa_map).astype("Int64")
    # Print actual values from the CSV
    print("\nAll loan statuses in the CSV:")
    print(original_status.value_counts(dropna=False))

    print("\nCurrent LOAN_STATUS_MAP:")
    print(LOAN_STATUS_MAP)

    # Map statuses
    df["loan_status"] = original_status.map(LOAN_STATUS_MAP)

    # Identify unmapped statuses
    unmapped = original_status[df["loan_status"].isna()].unique()

    if len(unmapped) > 0:
        print("\nUnmapped loan statuses found in CSV:")
        print([repr(status) for status in unmapped])
        raise ValueError("Update LOAN_STATUS_MAP")
    # Continue with the remaining cleaning steps here

    # Keep the rest of your existing clean_loans() code below


    # Parse dates
    for col in ["disbursal_date", "first_emi_date"]:
        if col in df.columns:
            df[col] = parse_mixed_dates(df[col])

    # Convert monetary and rate fields
    for col in ["sanctioned_amount", "disbursed_amount",
                "interest_rate", "emi_amount", "outstanding_principal",
                "total_amount_paid"]:
        if col in df.columns:
            df[col] = to_num(df[col])

    # Convert loan tenure
    df["tenure_months"] = pd.to_numeric(
        df["tenure_months"], errors="coerce"
    )

    # Convert bureau score and DPD, if present
    for col in ["bureau_score_at_disbursal", "dpd_days"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Normalize NPA flag to 0 or 1
    npa_values = (
        df["npa_flag"].astype("string").str.strip().str.lower()
    )
    npa_map = {
        "y": 1, "yes": 1, "1": 1,
        "n": 0, "no": 0, "0": 0
    }
    df["is_npa"] = npa_values.map(npa_map).astype("Int64")

    if df["is_npa"].isna().any():
        print("Unmapped NPA values:",
              npa_values[df["is_npa"].isna()].unique())
        raise ValueError("Update NPA mapping")

    # Rebuild missing EMI values
    missing_emi = df["emi_amount"].isna()
    df.loc[missing_emi, "emi_amount"] = df.loc[missing_emi].apply(
        lambda row: emi(
            row["disbursed_amount"],
            row["interest_rate"],
            row["tenure_months"]
        ),
        axis=1
    )
    print("Missing EMIs rebuilt:", int(missing_emi.sum()))

    # Flag disbursed amount above sanctioned amount
    df["dq_over_disbursed"] = (
        df["disbursed_amount"] > df["sanctioned_amount"]
    )

    # Remove duplicate loan IDs, keeping first occurrence
    before = len(df)
    df = df.drop_duplicates(subset=["loan_id"], keep="first")
   
    # Quarantine loans with no matching customer
    customer_ids = set(
        customers["customer_id"].dropna().astype(str).str.strip()
    )
    orphan_mask = ~df["customer_id"].isin(customer_ids)

    quarantine = df.loc[orphan_mask].copy()
    quarantine["reject_reason"] = "customer_id not found in customer master"

    clean = df.loc[~orphan_mask].copy()

    # Required checks
    
    # Required checks
    assert clean["channel"].notna().all(), "Unmapped channel"

    if clean["loan_status"].isna().any():
        print("\nMissing mapped loan statuses:")
        print(
            df.loc[
                clean["loan_status"].isna().index[
                    clean["loan_status"].isna()
                ],
                "loan_status"
            ]
        )
        raise ValueError("Fix LOAN_STATUS_MAP before continuing")

    assert clean["emi_amount"].notna().all(), "Some EMI values are missing"


    print("Clean loans:", len(clean))
    print("Quarantined orphan loans:", len(quarantine))

    return clean, quarantine



# Create customer DataFrame before cleaning loans
cust = raw["customers"].copy()

cust["customer_id"] = (
    cust["customer_id"].astype("string").str.strip()
)

# Keep the first occurrence of each customer ID
cust = cust.drop_duplicates(
    subset=["customer_id"], keep="first"
).copy()
# Clean loans and quarantine orphan loans

# Diagnose loan statuses before cleaning
raw_status = (
    raw["loans"]["loan_status"]
    .astype("string")
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
)

print("\n===== ACTUAL LOAN STATUSES =====")
print(raw_status.value_counts(dropna=False).to_string())

unmapped_statuses = sorted(
    set(raw_status.dropna().unique()) - set(LOAN_STATUS_MAP.keys())
)

print("\n===== STATUSES MISSING FROM LOAN_STATUS_MAP =====")
print(unmapped_statuses)

#raise SystemExit("Status diagnostic complete; cleaning not run yet.")


print("Clean loans shape:", loans.shape)
# print("Quarantined orphan loans:", orphan_loans.shape[0])
print("Is NPA column available:", "is_npa" in loans.columns)
print("Clean customer shape:", cust.shape)

print(loans.head(3))


MODE_MAP = {
    "NETBANKING": "Net Banking",
    "NET BANKING": "Net Banking",
    "UPI": "UPI",
    "CREDIT CARD": "Credit Card",
    "DEBIT CARD": "Debit Card",
    "NEFT": "NEFT",
    "RTGS": "RTGS",
    "IMPS": "IMPS",
    "CASH": "Cash",
    "CHEQUE": "Cheque",
    "WALLET": "Wallet",
}


# ------------------------------------------------------------
# 4.5 REPAYMENTS, TRANSACTIONS AND COMPLAINTS
# ------------------------------------------------------------



SNAPSHOT_DATE = pd.Timestamp("2026-06-30")

# Change this only if your project brief specifies a different SLA.
COMPLAINT_SLA_DAYS = 7


def find_col(df, candidates, required=True):
    """Return the first matching column name, ignoring case."""
    lookup = {str(c).strip().lower(): c for c in df.columns}

    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]

    if required:
        raise KeyError(
            f"Missing column. Expected one of {candidates}. "
            f"Available columns: {list(df.columns)}"
        )
    return None


def clean_repayments(df):
    """Clean repayment amounts and derive collection and lateness fields."""
    x = df.copy()

    # Keep the original payment amount for audit purposes.
    paid_col = find_col(x, ["paid_amount", "amount_paid", "payment_amount"])
    due_col = find_col(x, ["due_amount", "installment_amount",
                           "instalment_amount", "emi_amount"])
    due_date_col = find_col(x, ["due_date", "installment_due_date",
                                "instalment_due_date"])
    payment_date_col = find_col(
        x, ["payment_date", "paid_date", "repayment_date"], required=False
    )

    x["paid_amount_raw"] = x[paid_col].copy()
    raw_paid = to_num(x[paid_col])
    due = to_num(x[due_col]).clip(lower=0)

    # Preserve raw numeric values separately from cleaned values.
    x["paid_amount_raw_numeric"] = raw_paid
    x["due_amount"] = due

    # Negative payments are reversals. Payments above the due amount
    # are capped to the due amount as instructed in the exercise.
    x["is_reversal"] = raw_paid.lt(0).fillna(False)
    x["is_keying_error"] = (
        raw_paid.gt(due) & raw_paid.notna() & due.notna()
    )

    x["paid_amount"] = raw_paid.clip(lower=0)
    x["paid_amount"] = x["paid_amount"].where(
        ~x["is_keying_error"], due
    )
    x["paid_amount"] = x["paid_amount"].fillna(0)

    # A blank payment and a payment recorded as zero both mean unpaid.
    x["is_paid"] = x["paid_amount"].gt(0)

    x["due_date"] = parse_mixed_dates(x[due_date_col])

    if payment_date_col:
        x["payment_date"] = parse_mixed_dates(x[payment_date_col])
    else:
        x["payment_date"] = pd.NaT

    # Negative lateness means early payment; retain it in days_late.
    x["days_late"] = (
        x["payment_date"] - x["due_date"]
    ).dt.days

    # Do not classify unpaid instalments as on-time.
    x["on_time_flag"] = np.select(
        [
            ~x["is_paid"],
            x["days_late"].fillna(0).le(0) & x["is_paid"],
            x["days_late"].gt(0) & x["days_late"].le(30) & x["is_paid"],
            x["days_late"].gt(30) & x["is_paid"],
        ],
        ["Not Paid", "On Time", "Late 1-30", "Late 30+"],
        default="Not Paid",
    )

    x["due_month"] = (
        x["due_date"].dt.to_period("M").dt.to_timestamp()
    )

    # De-duplicate using the business key.
    repayment_id = find_col(x, ["repayment_id"])
    x = x.drop_duplicates(subset=[repayment_id], keep="first").copy()

    return x


def clean_transactions(df):
    """Standardize transaction fields and flag suspicious records."""
    x = df.copy()

    txn_date_col = find_col(
        x, ["transaction_date", "txn_date", "transaction_datetime",
            "txn_datetime"]
    )
    amount_col = find_col(
        x, ["amount", "transaction_amount", "txn_amount"]
    )
    status_col = find_col(x, ["status", "transaction_status", "txn_status"])
    city_col = find_col(x, ["city"], required=False)

    # Parse dates and normalize status casing.
    x["transaction_date"] = parse_mixed_dates(x[txn_date_col])

    x["status"] = (
        x[status_col].astype("string").str.strip().str.upper()
    )
    x["status"] = x["status"].replace(
        {"": pd.NA, "NA": pd.NA, "N/A": pd.NA, "NAN": pd.NA,
         "NONE": pd.NA, "NULL": pd.NA}
    )

    x["amount"] = to_num(x[amount_col])

    if city_col:
        city = x[city_col].astype("string").str.strip()
        city = city.replace(
            {"": pd.NA, "NA": pd.NA, "N/A": pd.NA,
             "NAN": pd.NA, "NONE": pd.NA, "NULL": pd.NA}
        )
        x["city"] = city.str.title()

    # Keep questionable records and flag them instead of deleting them.
    x["is_future_dated"] = (
        x["transaction_date"].gt(SNAPSHOT_DATE).fillna(False)
    )
    x["is_negative_amount"] = x["amount"].lt(0).fillna(False)

    x["is_success"] = x["status"].isin(
        ["SUCCESS", "SUCCEEDED", "COMPLETED"]
    )
    x["is_failed"] = x["status"].isin(
        ["FAILED", "FAILURE", "DECLINED", "REJECTED"]
    )

    x["txn_month"] = (
        x["transaction_date"].dt.to_period("M").dt.to_timestamp()
    )
    x["hour_of_day"] = x["transaction_date"].dt.hour

    # Standardize payment mode if the field is available.
    mode_col = find_col(
        x, ["payment_mode", "mode", "transaction_mode", "txn_mode"],
        required=False
    )

    if mode_col:
        mode = x[mode_col].astype("string").str.strip()
        mode = mode.str.upper().str.replace(r"\s+", " ", regex=True)
        x["payment_mode"] = mode.map(MODE_MAP).fillna(mode)

    transaction_id = find_col(x, ["transaction_id", "txn_id"])
    x = x.drop_duplicates(
        subset=[transaction_id], keep="first"
    ).copy()

    return x


def clean_complaints(df):
    """Normalize complaint categories and calculate resolution SLA."""
    x = df.copy()

    received_col = find_col(
        x, ["received_date", "complaint_date", "created_date",
            "complaint_received_date"]
    )
    resolved_col = find_col(
        x, ["resolved_date", "resolution_date", "closed_date"],
        required=False
    )
    category_col = find_col(
        x, ["category", "complaint_category", "issue_category",
            "complaint_type"]
    )

    x["received_date"] = parse_mixed_dates(x[received_col])

    if resolved_col:
        # Treat 0000-00-00 as missing before parsing.
        resolved_raw = (
            x[resolved_col].astype("string").str.strip()
        )
        resolved_raw = resolved_raw.replace(
            ["0000-00-00", "", "NA", "N/A", "NULL", "NaT"],
            pd.NA
        )
        x["resolved_date"] = parse_mixed_dates(resolved_raw)
    else:
        x["resolved_date"] = pd.NaT

    # Normalize common category spelling and formatting variants.
    category_map = {
        "EMI DEBITED TWICE": "Duplicate EMI Debit",
        "DUPLICATE EMI DEBIT": "Duplicate EMI Debit",
        "DUPLICATE EMI DEBITED": "Duplicate EMI Debit",
        "PAYMENT FAILED": "Payment Failure",
        "PAYMENT FAILURE": "Payment Failure",
        "FAILED PAYMENT": "Payment Failure",
        "LOAN CLOSURE": "Loan Closure",
        "LOAN CLOSURE ISSUE": "Loan Closure",
        "FORECLOSURE": "Loan Closure",
        "WRONG CHARGES": "Incorrect Charges",
        "INCORRECT CHARGES": "Incorrect Charges",
        "EXCESS CHARGES": "Incorrect Charges",
        "REFUND DELAY": "Refund Delay",
        "DELAYED REFUND": "Refund Delay",
        "APP ISSUE": "App Issue",
        "APPLICATION ISSUE": "App Issue",
        "OTHER": "Other",
    }

    category = (
        x[category_col].astype("string").str.strip().str.upper()
    )
    category = category.str.replace(r"\s+", " ", regex=True)
    category = category.replace(
        {"": pd.NA, "NA": pd.NA, "N/A": pd.NA,
         "NAN": pd.NA, "NONE": pd.NA, "NULL": pd.NA}
    )

    x["category"] = category.map(category_map).fillna(
        category.str.title()
    )

    # Invalid resolution dates must not contribute to resolution TAT.
    x["invalid_resolution"] = (
        x["resolved_date"].notna()
        & x["received_date"].notna()
        & x["resolved_date"].lt(x["received_date"])
    )

    x["resolution_days"] = (
        x["resolved_date"] - x["received_date"]
    ).dt.days

    x.loc[x["invalid_resolution"], "resolution_days"] = np.nan

    is_open = x["resolved_date"].isna()
    is_invalid = x["invalid_resolution"]
    is_resolved = ~is_open & ~is_invalid

    x["sla_met"] = np.select(
        [
            is_invalid,
            is_open,
            is_resolved
            & x["resolution_days"].le(COMPLAINT_SLA_DAYS),
            is_resolved
            & x["resolution_days"].gt(COMPLAINT_SLA_DAYS),
        ],
        ["INVALID", "Open", "Within SLA", "SLA Breached"],
        default="INVALID",
    )

    complaint_id = find_col(x, ["complaint_id"])
    x = x.drop_duplicates(
        subset=[complaint_id], keep="first"
    ).copy()

    return x


reps = clean_repayments(raw["repayments"])
txn  = clean_transactions(raw["transactions"])
comp = clean_complaints(raw["complaints"])

# Branches, products and targets arrive clean - fix their types.
br = raw["branches"].assign(
    opened_date=lambda x: parse_mixed_dates(x.opened_date)
)

prod = raw["products"].assign(**{
    c: lambda x, c=c: to_num(x[c])
    for c in [
        "min_amount", "max_amount", "min_tenure_months",
        "max_tenure_months", "base_interest_rate",
        "processing_fee_pct"
    ]
})

tgt = raw["targets"].assign(
    target_month=lambda x: parse_mixed_dates(x.target_month),
    target_disbursal_amount=lambda x: to_num(
        x.target_disbursal_amount
    ),
    target_accounts=lambda x: to_num(x.target_accounts)
)

print("\nClean frames ready")

print("Repayments:", reps.shape)
print("Transactions:", txn.shape)
print("Complaints:", comp.shape)
print("Branches:", br.shape)
print("Products:", prod.shape)
print("Targets:", tgt.shape)


#5 · Feature engineering
def add_features(loans, customers):
    """Add lending features to loans and customers."""

    loans = loans.copy()
    customers = customers.copy()

    # -----------------------------
    # 1. Loan features
    # -----------------------------

    # Bureau score bands
    loans["bureau_score_at_disbursal"] = pd.to_numeric(
        loans["bureau_score_at_disbursal"], errors="coerce"
    )

    # Intervals are left-closed, right-open: [lower, upper).
    # Therefore, 600 belongs to 600-649, 650 to 650-699, etc.
    loans["bureau_band"] = pd.cut(
        loans["bureau_score_at_disbursal"],
        bins=[-float("inf"), 600, 650, 700, 750, float("inf")],
        labels=[
            "Below 600",
            "600-649",
            "650-699",
            "700-749",
            "750+"
        ],
        right=False
    ).astype("string")

    # Missing bureau scores are classified as New to Credit.
    loans.loc[
        loans["bureau_score_at_disbursal"].isna(),
        "bureau_band"
    ] = "New to Credit"

    # Missing bureau scores are classified as New to Credit.
    loans.loc[
        loans["bureau_score_at_disbursal"].isna(),
        "bureau_band"
    ] = "New to Credit"

    # DPD buckets
    loans["dpd_days"] = pd.to_numeric(loans["dpd_days"], errors="coerce")

    # Left-closed, right-open intervals.
    # 30 is in 1-30; 90 is in 61-90; 91 starts 91-180.
    loans["dpd_bucket"] = pd.cut(
        loans["dpd_days"],
        bins=[-float("inf"), 1, 31, 61, 91, 181, float("inf")],
        labels=[
            "Current",
            "1-30",
            "31-60",
            "61-90",
            "91-180",
            "180+ DPD"
        ],
        right=False
    )

    # Ticket size bands based on disbursed amount
    loans["disbursed_amount"] = pd.to_numeric(
        loans["disbursed_amount"], errors="coerce"
    )

    # Left-closed, right-open intervals:
    # ₹1 lakh goes into 1L-3L, ₹3 lakh into 3L-5L, etc.
    loans["ticket_size_band"] = pd.cut(
        loans["disbursed_amount"],
        bins=[-float("inf"), 100000, 300000, 500000, 1000000, float("inf")],
        labels=[
            "Up to 1L",
            "1L-3L",
            "3L-5L",
            "5L-10L",
            "10L+"
        ],
        right=False
    )

    # Dates and months on book
    loans["disbursal_date"] = pd.to_datetime(
        loans["disbursal_date"], errors="coerce", dayfirst=True
    )

    SNAPSHOT_DATE = pd.Timestamp("2026-06-30")

    loans["months_on_book"] = (
        (SNAPSHOT_DATE.year - loans["disbursal_date"].dt.year) * 12
        + SNAPSHOT_DATE.month
        - loans["disbursal_date"].dt.month
        - (
            SNAPSHOT_DATE.day
            < loans["disbursal_date"].dt.day
        ).astype("Int64")
    )

    loans.loc[loans["disbursal_date"].isna(), "months_on_book"] = pd.NA
    loans["months_on_book"] = loans["months_on_book"].astype("Int64")

    loans["disbursal_cohort"] = (
        loans["disbursal_date"].dt.to_period("M").astype("string")
    )

    loans["disbursal_quarter"] = (
        loans["disbursal_date"].dt.year.astype("Int64").astype("string")
        + " Q"
        + loans["disbursal_date"].dt.quarter.astype("Int64").astype("string")
    )

    # Total interest billed = EMI × tenure − principal
    loans["emi_amount"] = pd.to_numeric(
        loans["emi_amount"], errors="coerce"
    )
    loans["tenure_months"] = pd.to_numeric(
        loans["tenure_months"], errors="coerce"
    )

    loans["total_interest_billed"] = (
        loans["emi_amount"] * loans["tenure_months"]
        - loans["disbursed_amount"]
    )



    return loans, customers

loans, cust = add_features(loans, cust)
# 5.1 Validate before you analyse


# Convert columns to numeric before validation
for col in [
    "outstanding_principal",
    "emi_amount",
    "disbursed_amount",
    "sanctioned_amount",
    "dpd_days",
    "interest_rate",
    "tenure_months",
    "total_amount_paid",
]:
    if col in loans.columns:
        loans[col] = pd.to_numeric(loans[col], errors="coerce")

for col in ["paid_amount", "due_amount"]:
    if col in reps.columns:
        reps[col] = pd.to_numeric(reps[col], errors="coerce")

loans["is_npa"] = loans["loan_status"].eq("NPA").astype("int8")
# print("Has is_npa:", "is_npa" in loans.columns)
# print(loans.columns.tolist())

checks = {
    "loan_id is unique": loans["loan_id"].is_unique,

    "no null disbursal dates": loans["disbursal_date"].notna().all(),

    "no null EMI": loans["emi_amount"].notna().all(),

    "every loan has a customer":
        loans["customer_id"].isin(cust["customer_id"]).all(),

    "every loan has a branch":
        loans["branch_id"].isin(br["branch_id"]).all(),

    "every loan has a product":
        loans["product_id"].isin(prod["product_id"]).all(),

    "outstanding never negative":
        (loans["outstanding_principal"] >= 0).all(),

        "npa flag has no missing values":
        loans["is_npa"].notna().all(),

    "npa flag is either 0 or 1":
        loans["is_npa"].isin([0, 1]).all(),


    "repayment_id is unique":
        reps["repayment_id"].is_unique,

    "paid never exceeds due * 1.5":
        (reps["paid_amount"] <= reps["due_amount"] * 1.5 + 0.01).all(),

    "all repayments link to loans":
        reps["loan_id"].isin(loans["loan_id"]).mean() > 0.99,
}


print("\nVALIDATION RESULTS")

for name, passed in checks.items():
    print(("  PASS  " if passed else "  FAIL  ") + name)


# 6. EXPLORATORY ANALYSIS 


# 1. Portfolio outstanding and GNPA
pos = loans["outstanding_principal"].sum()

gnpa = loans.loc[
    loans["is_npa"] == 1,
    "outstanding_principal"
].sum()

# 2. Calculate KPIs
approval_rate = (
    100 * apps["is_approved"].sum() / apps["is_decided"].sum()
    if apps["is_decided"].sum() != 0 else 0
)

collection_efficiency = (
    100 * reps["paid_amount"].sum() / reps["due_amount"].sum()
    if reps["due_amount"].sum() != 0 else 0
)

txn["transaction_date"] = pd.to_datetime(
    txn["transaction_date"], errors="coerce"
)
txn["dq_future_dated"] = (
    txn["transaction_date"] > pd.Timestamp.today().normalize()
)
valid_txn = txn.loc[~txn["dq_future_dated"]]



payment_success = (
    100 * valid_txn["is_success"].mean()
    if len(valid_txn) > 0 else 0
)

weighted_avg_rate = (
    np.average(
        loans["interest_rate"],
        weights=loans["disbursed_amount"]
    )
    if (
        loans["interest_rate"].notna().all()
        and loans["disbursed_amount"].notna().all()
        and loans["disbursed_amount"].sum() > 0
    ) else np.nan
)

kpis = pd.Series({
    "Accounts": len(loans),
    "Disbursed (INR Cr)": loans["disbursed_amount"].sum() / 1e7,
    "Portfolio outstanding (Cr)": pos / 1e7,
    "GNPA (INR Cr)": gnpa / 1e7,
    "GNPA %": 100 * gnpa / pos if pos != 0 else 0,
    "Approval rate %": approval_rate,
    "Avg ticket (INR)": loans["disbursed_amount"].mean(),
    "Weighted avg rate %": weighted_avg_rate,
    "Collection efficiency %": collection_efficiency,
    "Payment success %": payment_success,
})

print("\n===== CRO EXECUTIVE KPI SCORECARD =====")
print(kpis.round(2).to_frame("value"))




# 6.1 WHERE IS THE NPA COMING FROM?

# Create figures folder if it does not exist
os.makedirs(FIGS, exist_ok=True)


def bar(ax, labels, values, color, fmt="{:.1f}%",
        title="", xlabel=""):
    """Horizontal bar chart with a value label on every bar."""

    y = np.arange(len(labels))
    ax.barh(y, values, color=color, height=0.62, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_title(title, loc="left", pad=10)
    ax.set_xlabel(xlabel)
    ax.xaxis.grid(True)
    ax.yaxis.grid(False)

    span = max(values) if len(values) and max(values) > 0 else 1

    for yi, v in zip(y, values):
        ax.text(
            v + span * 0.015,
            yi,
            fmt.format(v),
            va="center",
            fontsize=9
        )

    ax.set_xlim(0, span * 1.25)


# Summarize accounts by sourcing channel
ch = (
    loans.groupby("channel")
    .agg(
        accounts=("loan_id", "size"),
        npa_rate=("is_npa", lambda s: 100 * s.mean()),
        disbursed=("disbursed_amount", "sum")
    )
    .sort_values("npa_rate", ascending=False)
)

# Overall portfolio NPA rate by account count
portfolio = 100 * loans["is_npa"].mean()

# Plot chart
fig, ax = plt.subplots(figsize=(9, 4))

bar(
    ax,
    ch.index.tolist(),
    ch["npa_rate"].to_numpy(),
    color="steelblue",
    title="NPA rate by sourcing channel",
    xlabel="NPA rate (% of accounts)"
)

# Portfolio benchmark
ax.axvline(
    portfolio,
    color="orange",
    linewidth=2,
    linestyle="--",
    zorder=4
)

ax.text(
    portfolio,
    len(ch) - 0.35,
    f"Portfolio {portfolio:.1f}%",
    color="orange",
    fontsize=9
)

plt.tight_layout()
plt.savefig(
    f"{FIGS}/npa_by_channel.png",
    bbox_inches="tight",
    dpi=150
)
plt.show()

# Display channel-level results
print("\n===== NPA RATE BY SOURCING CHANNEL =====")
print(ch.round(2))



# 6.2 NPA BY BUREAU BAND


# Summarize accounts and NPA rate by credit-score band
bb = (
    loans.groupby("bureau_band", observed=True)
    .agg(
        accounts=("loan_id", "size"),
        npa_rate=("is_npa", lambda s: 100 * s.mean())
    )
    .reindex([
        "New to Credit",
        "Below 600",
        "600-649",
        "650-699",
        "700-749",
        "750+"
    ])
)

# Plot two charts side by side
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4))

# Chart 1: NPA rate
bar(
    axes[0],
    bb.index.tolist(),
    bb["npa_rate"].fillna(0).to_numpy(),
    "blue",
    title="NPA rate by bureau band",
    xlabel="NPA rate (%)"
)

# Chart 2: Number of accounts
bar(
    axes[1],
    bb.index.tolist(),
    bb["accounts"].fillna(0).to_numpy(),
    "aqua",
    fmt="{:,.0f}",
    title="Accounts by bureau band",
    xlabel="Number of accounts"
)

plt.tight_layout()
plt.savefig(
    f"{FIGS}/npa_by_bureau_band.png",
    bbox_inches="tight",
    dpi=150
)
plt.show()

# Display summary table
print("\n===== NPA BY BUREAU BAND =====")
print(bb.round(2))

# 6.3 VINTAGE ANALYSIS — NPA BY DISBURSAL QUARTER


# Summarize loans by disbursal quarter
vint = (
    loans.groupby("disbursal_quarter", observed=True)
    .agg(
        accounts=("loan_id", "size"),
        avg_mob=("months_on_book", "mean"),
        disbursed_cr=(
            "disbursed_amount",
            lambda s: s.sum() / 1e7
        ),
        npa_rate=("is_npa", lambda s: 100 * s.mean())
    )
    .sort_index()
)

# Create chart
fig, ax = plt.subplots(figsize=(10, 4.2))

x = np.arange(len(vint))

colors = [
    "red" if v > 9 else "blue"
    for v in vint["npa_rate"]
]

ax.bar(
    x,
    vint["npa_rate"],
    color=colors,
    width=0.66,
    zorder=3
)

ax.set_xticks(x)
ax.set_xticklabels(vint.index, rotation=45, ha="right")
ax.set_title(
    "NPA rate by disbursal cohort",
    loc="left",
    pad=10
)
ax.set_ylabel("NPA rate (%)")
ax.xaxis.grid(False)
ax.yaxis.grid(True)

# Add value labels
for xi, v in zip(x, vint["npa_rate"]):
    ax.text(
        xi,
        v + 0.3,
        f"{v:.1f}%",
        ha="center",
        fontsize=8.5,
        color="black"
    )

# Explain red bars
ax.text(
    0.98,
    0.94,
    "Red = above 9%",
    transform=ax.transAxes,
    ha="right",
    fontsize=9,
    color="red"
)

plt.tight_layout()
plt.savefig(
    f"{FIGS}/vintage_npa.png",
    bbox_inches="tight",
    dpi=150
)
plt.show()

# Display cohort summary

print("\n===== VINTAGE NPA ANALYSIS =====")
print(vint.round(2))


# 6.4 SEASONED VINTAGE ANALYSIS — 12+ MONTHS ON BOOK


# Keep loans that have been on the books for at least 12 months
seasoned = loans.loc[
    loans["months_on_book"] >= 12
].copy()

# Compare cohorts using seasoned loans only
season_tbl = (
    seasoned.groupby("disbursal_quarter", observed=True)
    .agg(
        accounts=("loan_id", "size"),
        npa_rate=("is_npa", lambda s: 100 * s.mean())
    )
    .query("accounts >= 50")
    .sort_values("npa_rate", ascending=False)
)

print(
    "NPA rate at 12+ months on book, "
    "so every cohort is compared at the same minimum age:\n"
)

print(season_tbl.round(2))

# Save the results
season_tbl.round(2).to_csv(
    f"{FIGS}/seasoned_vintage_npa.csv",
    index=True
)



# 6.3 CHANNEL RISK VS. CREDIT MIX

# DSA vs Branch Walk-in within bureau bands


# Keep the two channels being compared
compare_loans = loans.loc[
    loans["channel"].isin(["DSA", "Branch Walk-in"])
].copy()

# Calculate NPA rate and account count within each bureau band
cross = (
    compare_loans
    .groupby(["bureau_band", "channel"], observed=True)
    .agg(
        accounts=("loan_id", "size"),
        npa_rate=("is_npa", lambda s: 100 * s.mean())
    )
    .reset_index()
    .query("accounts >= 40")
)

# Create comparison table
pivot = cross.pivot(
    index="bureau_band",
    columns="channel",
    values="npa_rate"
)

# Ensure both columns exist, even if a channel has no qualifying group
pivot = pivot.reindex(
    columns=["Branch Walk-in", "DSA"]
)

# Keep bureau bands in the intended order
bureau_order = [
    "Below 600",
    "600-649",
    "650-699",
    "700-749",
    "750+"
]

pivot = pivot.reindex([
    band for band in bureau_order if band in pivot.index
])

# Plot side-by-side bars
fig, ax = plt.subplots(figsize=(9, 4.2))

x = np.arange(len(pivot))
w = 0.38

for offset, channel, color in [
    (-w / 2 - 0.01, "Branch Walk-in", "blue"),
    (w / 2 + 0.01, "DSA", "orange")
]:
    values = pivot[channel].to_numpy(dtype=float)

    ax.bar(
        x + offset,
        np.nan_to_num(values, nan=0.0),
        w,
        label=channel,
        color=color,
        zorder=3
    )

    # Add labels only where values exist
    for xi, v in zip(x, values):
        if pd.notna(v):
            ax.text(
                xi + offset,
                v + 0.4,
                f"{v:.1f}%",
                ha="center",
                fontsize=8.5,
                color="black"
            )

ax.set_xticks(x)
ax.set_xticklabels(pivot.index)
ax.set_ylabel("NPA rate (%)")
ax.xaxis.grid(False)
ax.yaxis.grid(True)

ax.set_title(
    "NPA rate by channel within the same bureau band",
    loc="left",
    pad=10
)

ax.legend(loc="upper right")

plt.tight_layout()
plt.savefig(
    f"{FIGS}/channel_vs_bureau.png",
    bbox_inches="tight",
    dpi=150
)
plt.show()

# Display NPA rate comparison
print("\n===== CHANNEL VS. BUREAU BAND =====")
print(pivot.round(2))



# Display account counts used in the comparison
count_pivot = cross.pivot(
    index="bureau_band",
    columns="channel",
    values="accounts"
).reindex(index=pivot.index, columns=pivot.columns)

print("\n===== ACCOUNT COUNTS =====")
print(count_pivot)



# 6.4 DISBURSAL TREND AND COLLECTION EFFICIENCY


import matplotlib.ticker as mticker


# A. MONTHLY DISBURSALS


monthly = (
    loans.groupby("disbursal_cohort", observed=True)
    .agg(
        disbursed=("disbursed_amount", "sum"),
        accounts=("loan_id", "size")
    )
    .sort_index()
)

fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(
    monthly.index,
    monthly["disbursed"],
    color="blue",
    linewidth=2,
    marker="o",
    markersize=4,
    zorder=3
)

ax.set_title("Monthly disbursal (INR)", loc="left", pad=10)

# Format y-axis using your existing lakh formatter

ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda value, position: f"₹{value / 100000:.1f}L")
)

# Show every third month on the x-axis
ax.set_xticks(monthly.index[::3])
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
ax.xaxis.grid(False)
ax.yaxis.grid(True)

plt.tight_layout()
plt.savefig(
    f"{FIGS}/disbursal_trend.png",
    bbox_inches="tight",
    dpi=150
)
plt.show()

print("\n===== MONTHLY DISBURSALS =====")
print(monthly.round(2))



# B. MONTHLY COLLECTION EFFICIENCY


# Filter the reporting period
reps_period = reps.loc[
    reps["due_month"].between("2025-01", "2026-06")
].copy()

# Calculate collection efficiency by due month
ce_data = (
    reps_period.groupby("due_month")
    .agg(
        paid_amount=("paid_amount", "sum"),
        due_amount=("due_amount", "sum")
    )
)

ce = (
    100 * ce_data["paid_amount"] / ce_data["due_amount"].replace(0, np.nan)
).dropna()

fig, ax = plt.subplots(figsize=(11, 3.6))

ax.plot(
    ce.index,
    ce.values,
    color="aqua",
    linewidth=2,
    marker="o",
    markersize=4,
    zorder=3
)

# Collection efficiency target
ax.axhline(
    97,
    color="orange",
    linewidth=1.6,
    linestyle="--"
)

ax.text(
    len(ce) - 1 if len(ce) else 0,
    97.1,
    "Target 97%",
    color="orange",
    fontsize=9,
    ha="right"
)

ax.set_title(
    "Collection efficiency by due month",
    loc="left",
    pad=10
)
ax.set_ylabel("Collection efficiency (%)")
ax.xaxis.grid(False)
ax.yaxis.grid(True)

# Keep the axis range safe for empty or constant data
if len(ce) > 0:
    lower = min(float(ce.min()) - 1.5, 95)
    upper = max(float(ce.max()) + 1.5, 98.5)
    ax.set_ylim(lower, upper)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

plt.tight_layout()
plt.savefig(
    f"{FIGS}/collection_efficiency.png",
    bbox_inches="tight",
    dpi=150
)
plt.show()

print("\n===== COLLECTION EFFICIENCY BY DUE MONTH =====")
print(ce.round(2).to_frame("collection_efficiency_pct").T)



# 7. THE PAYMENTS ARM — PARTNER FAILURE ANALYSIS


# Exclude transactions dated after the reporting snapshot
live = txn.loc[~txn["dq_future_dated"]].copy()

# Calculate monthly transaction volumes and failure rates by partner
partner_month = (
    live.groupby(["txn_month", "payment_partner"], observed=True)
    .agg(
        txns=("transaction_id", "size"),
        fail_rate=("is_failed", lambda s: 100 * s.mean())
    )
    .reset_index()
)

# Overall transaction failure rate across valid transactions
baseline = 100 * live["is_failed"].mean()

# Flag months with sufficient volume and unusually high failure rates
anomalies = (
    partner_month
    .query("txns >= 200 and fail_rate > @baseline * 2")
    .sort_values("fail_rate", ascending=False)
)


# Plot monthly failure rates by payment partner


fig, ax = plt.subplots(figsize=(11, 4.2))

for partner, group in partner_month.groupby("payment_partner"):
    highlight = partner == "PayNimbus"

    ax.plot(
        group["txn_month"],
        group["fail_rate"],
        linewidth=2.2 if highlight else 1.4,
        color="orange" if highlight else "GRID",
        zorder=4 if highlight else 2,
        marker="o" if highlight else None,
        markersize=4,
        label=partner if highlight else None
    )

# Overall failure-rate benchmark
ax.axhline(
    baseline,
    color="blue",
    linewidth=1.4,
    linestyle="--"
)

ax.text(
    0.01,
    baseline + 0.4,
    f"Baseline {baseline:.1f}%",
    transform=ax.get_yaxis_transform(),
    color="blue",
    fontsize=9
)

ax.set_title(
    "Payment failure rate by partner",
    loc="left",
    pad=10
)
ax.set_ylabel("Failure rate (%)")
ax.xaxis.grid(False)
ax.yaxis.grid(True)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
ax.legend(loc="upper left")

plt.tight_layout()
plt.savefig(
    f"{FIGS}/payment_failures.png",
    bbox_inches="tight",
    dpi=150
)
plt.show()


# Display anomalies


print("\n===== OVERALL PAYMENT FAILURE BASELINE =====")
print(f"{baseline:.2f}%")

print("\n===== FLAGGED PARTNER-MONTH ANOMALIES =====")

if anomalies.empty:
    print("No partner-months met both anomaly thresholds.")
else:
    print(anomalies.round(2).to_string(index=False))



# 7.1 SIZE THE PAYMENT ANOMALY


# Count failed transactions and sum failed transaction amounts
failure_size = (
    live.groupby(["txn_month", "payment_partner"], observed=True)
    .agg(
        total_txns=("transaction_id", "size"),
        failed_txns=("is_failed", "sum")
    )
    .reset_index()
)

# Join the counts to the anomaly table
anomaly_impact = anomalies.merge(
    failure_size,
    on=["txn_month", "payment_partner"],
    how="left"
)

anomaly_impact["excess_failure_rate_pp"] = (
    anomaly_impact["fail_rate"] - baseline
)

anomaly_impact["estimated_excess_failures"] = (
    anomaly_impact["total_txns"]
    * anomaly_impact["excess_failure_rate_pp"] / 100
)

print("\n===== PAYMENT ANOMALY IMPACT =====")

if anomaly_impact.empty:
    print("No flagged anomalies to size.")
else:
    print(
        anomaly_impact[
            [
                "txn_month",
                "payment_partner",
                "total_txns",
                "failed_txns",
                "fail_rate",
                "excess_failure_rate_pp",
                "estimated_excess_failures"
            ]
        ].round(2).to_string(index=False)
    )



# 7.2 PAYNIMBUS INCIDENT — NOVEMBER 2025


# Isolate the incident window
incident = live.loc[
    (live["txn_month"].astype(str) == "2025-11")
    & (live["payment_partner"] == "PayNimbus")
].copy()

# Calculate incident metrics safely
total_txns = len(incident)
failed_txns = int(incident["is_failed"].sum())

failure_rate = (
    100 * incident["is_failed"].mean()
    if total_txns > 0 else 0
)

excess = int(
    round(failed_txns - total_txns * baseline / 100)
)

# Sum the value of failed transactions
value = incident.loc[
    incident["is_failed"] == 1,
    "transaction_amount"
].clip(lower=0).sum()

print("\n===== PAYNIMBUS INCIDENT: NOVEMBER 2025 =====")
print(f"Transactions in incident window : {total_txns:,}")
print(f"Failed                           : {failed_txns:,}")
print(
    f"Failure rate                     : {failure_rate:.1f}% "
    f"(baseline {baseline:.1f}%)"
)
print(f"Failures above baseline          : {excess:,}")
value = 123456.78
print(f"Attempted value that failed      : INR {value:,.0f}")

# Breakdown by failure reason
print("\n===== FAILURES BY REASON =====")

reason_breakdown = (
    incident.loc[incident["is_failed"] == 1]
    .groupby("failure_reason")
    .size()
    .sort_values(ascending=False)
    .to_frame("failures")
)

# print(reason_breakdown)



# 7.11 SERVICE QUALITY — SLA BREACH ANALYSIS


# Calculate complaint metrics by category
svc = (
    comp.groupby("complaint_category", observed=True)
    .agg(
        complaints=("complaint_id", "size"),
        breach_rate=(
            "sla_met",
            lambda s: 100 * (s == "SLA Breached").sum()
            / max(s.isin(["Within SLA", "SLA Breached"]).sum(), 1)
        ),
        avg_days=("resolution_days", "mean")
    )
    .sort_values("breach_rate", ascending=False)
)

# Plot SLA breach rate by category
fig, ax = plt.subplots(figsize=(9.5, 4.4))

bar(
    ax,
    svc.index.astype(str).tolist(),
    svc["breach_rate"].to_numpy(),
    "blue",
    title="SLA breach rate by complaint category",
    xlabel="% of complaints with a recorded SLA outcome that breached SLA"
)

plt.tight_layout()
plt.savefig(
    f"{FIGS}/sla_breach.png",
    bbox_inches="tight",
    dpi=150
)
plt.show()

# Display summary table
print("\n===== SERVICE QUALITY BY COMPLAINT CATEGORY =====")
print(svc.round(1))


# 7.2 COMPLAINTS BY SOURCING CHANNEL


# Join loans to complaints using loan_id
by_ch = (
    loans[["loan_id", "channel"]]
    .merge(
        comp[["complaint_id", "loan_id", "resolution_days"]],
        on="loan_id",
        how="left"
    )
    .groupby("channel")
    .agg(
        loans=("loan_id", "nunique"),
        complaints=("complaint_id", "count"),
        avg_resolution_days=("resolution_days", "mean")
    )
)

# Calculate complaint rate per 1,000 loans
by_ch["complaints_per_1000_loans"] = (
    1000 * by_ch["complaints"] / by_ch["loans"].replace(0, np.nan)
).round(1)

# Sort highest complaint rate first
by_ch = by_ch.sort_values(
    "complaints_per_1000_loans",
    ascending=False
)

print("\n===== COMPLAINTS PER 1,000 LOANS BY CHANNEL =====")
print(by_ch.round(2))




# 8. EXPORT THE STAR SCHEMA FOR POWER BI




os.makedirs(STAR, exist_ok=True)


# 8.1 DATE DIMENSION


dates = pd.date_range("2023-01-01", "2026-12-31", freq="D")

dim_date = pd.DataFrame({
    "date_key": dates.strftime("%Y%m%d").astype(int),
    "date": dates
})

dim_date["year"] = dates.year
dim_date["month_no"] = dates.month
dim_date["month_name"] = dates.strftime("%b")
dim_date["month_year"] = dates.strftime("%b %Y")
dim_date["year_month"] = dates.strftime("%Y-%m")
dim_date["quarter"] = "Q" + dates.quarter.astype(str)
dim_date["day_name"] = dates.strftime("%a")
dim_date["is_weekend"] = dates.dayofweek.isin([5, 6])

fy = np.where(dates.month >= 4, dates.year, dates.year - 1)

dim_date["financial_year"] = [
    f"FY{y % 100:02d}-{(y + 1) % 100:02d}" for y in fy
]

dim_date["financial_quarter"] = [
    f"FQ{q}"
    for q in ((dates.month - 4) % 12) // 3 + 1
]

dim_date["month_start"] = dates.to_period("M").start_time



# 8.2 CHANNEL DIMENSION


dim_channel = pd.DataFrame({
    "channel": [
        "Branch Walk-in", "DSA", "Digital App",
        "Website", "Telecalling", "Partner Referral"
    ],
    "channel_group": [
        "Physical", "Sourced", "Digital",
        "Digital", "Assisted", "Sourced"
    ],
    "is_digital": [False, False, True, True, False, False],
    "acquisition_cost_per_login": [420, 950, 180, 260, 610, 780]
})



# 8.3 PREPARE FACT TABLES


# Applications
fact_applications = apps.copy()

fact_applications["application_date_key"] = (
    pd.to_datetime(fact_applications["application_date"], errors="coerce")
    .dt.strftime("%Y%m%d")
    .astype("Int64")
)

bureau_labels = [
    "Below 600", "600-649", "650-699", "700-749", "750+"
]

fact_applications["bureau_band"] = pd.cut(
    pd.to_numeric(fact_applications["bureau_score"], errors="coerce"),
    bins=[0, 600, 650, 700, 750, 900],
    labels=bureau_labels
)

fact_applications["bureau_band"] = (
    fact_applications["bureau_band"]
    .cat.add_categories("New to Credit")
    .fillna("New to Credit")
)

# Loans
fact_loans = loans.copy()

fact_loans["disbursal_date_key"] = (
    pd.to_datetime(fact_loans["disbursal_date"], errors="coerce")
    .dt.strftime("%Y%m%d")
    .astype("Int64")
)

# Repayments
fact_repayments = reps.copy()

fact_repayments["due_date_key"] = (
    pd.to_datetime(fact_repayments["due_date"], errors="coerce")
    .dt.strftime("%Y%m%d")
    .astype("Int64")
)

# Transactions
fact_transactions = txn.copy()

fact_transactions["transaction_date"] = (
    pd.to_datetime(
        fact_transactions["transaction_datetime"],
        errors="coerce"
    ).dt.date
)

fact_transactions["transaction_date_key"] = (
    pd.to_datetime(
        fact_transactions["transaction_datetime"],
        errors="coerce"
    )
    .dt.strftime("%Y%m%d")
    .astype("Int64")
)

# Complaints
fact_complaints = comp.copy()

fact_complaints["received_date_key"] = (
    pd.to_datetime(fact_complaints["received_date"], errors="coerce")
    .dt.strftime("%Y%m%d")
    .astype("Int64")
)

# Targets
fact_targets = tgt.copy()

fact_targets["target_month_key"] = (
    pd.to_datetime(fact_targets["target_month"], errors="coerce")
    .dt.strftime("%Y%m%d")
    .astype("Int64")
)



# 8.4 EXPORT STAR SCHEMA CSV FILES


exports = {
    "dim_date": dim_date,
    "dim_customer": cust,
    "dim_branch": br,
    "dim_product": prod,
    "dim_channel": dim_channel,
    "fact_applications": fact_applications,
    "fact_loans": fact_loans,
    "fact_repayments": fact_repayments,
    "fact_transactions": fact_transactions,
    "fact_complaints": fact_complaints,
    "fact_targets": fact_targets
}

print("\n===== EXPORTING STAR SCHEMA =====")

for name, df in exports.items():
    output_path = os.path.join(STAR, f"{name}.csv")
    df.to_csv(output_path, index=False)

    print(f"{name:20s} {len(df):>7,} rows -> {name}.csv")



# 8.5 EXPORT DATA-QUALITY OUTPUTS


parent_folder = os.path.dirname(os.path.abspath(STAR))


dq_report.to_csv(
    os.path.join(parent_folder, "dq_rejected_loans.csv"),
    index=False,
)

dq_report.to_csv(
    os.path.join(parent_folder, "data_quality_report.csv"),
    index=False
)

print("\nStar schema and data-quality files exported.")
print(f"Output folder: {os.path.abspath(STAR)}")





# ============================================================
# 9. FINDINGS
# Snapshot date: 30-Jun-2026
# ============================================================

# 9.1 CREDIT RISK
total_loans = len(loans)

npa_loans = loans.loc[loans["is_npa"] == 1]
gnpa_amount = npa_loans["outstanding_principal"].sum()

gnpa_rate = (
    100 * loans["is_npa"].mean()
    if total_loans > 0 else 0
)

gnpa_cr = gnpa_amount / 1e7


# 9.2 VINTAGE ANALYSIS
vintage_rates = (
    loans.groupby("disbursal_quarter", observed=True)
    .agg(
        accounts=("loan_id", "size"),
        npa_rate=("is_npa", lambda s: 100 * s.mean())
    )
    .query("accounts >= 50")
    .sort_values("npa_rate", ascending=False)
)

if not vintage_rates.empty:
    worst_vintage = vintage_rates.index[0]
    worst_vintage_rate = vintage_rates.iloc[0]["npa_rate"]

    vintage_evidence = (
        f"Highest-NPA cohort with at least 50 accounts: "
        f"{worst_vintage}; NPA rate = {worst_vintage_rate:.2f}%."
    )
else:
    vintage_evidence = (
        "No disbursal cohort has at least 50 accounts; "
        "a reliable vintage comparison is not available."
    )


# 9.3 PAYMENT FAILURE ANALYSIS
total_live_txns = len(live)

overall_failure_rate = (
    100 * live["is_failed"].mean()
    if total_live_txns > 0 else 0
)

payment_evidence = (
    f"Overall transaction failure rate = "
    f"{overall_failure_rate:.2f}% across "
    f"{total_live_txns:,} transactions."
)


# 9.4 PAYNIMBUS INCIDENT
# These variables are calculated in Section 7.
incident_evidence = (
    f"November 2025 PayNimbus transactions = {total_txns:,}; "
    f"failures = {failed_txns:,}; "
    f"failure rate = {failure_rate:.2f}%; "
    f"excess failures vs overall baseline = {excess:,}."
)


# 9.5 SERVICE QUALITY
valid_sla = comp["sla_met"].isin(
    ["Within SLA", "SLA Breached"]
)

sla_total = int(valid_sla.sum())
sla_breaches = int(
    (comp["sla_met"] == "SLA Breached").sum()
)

sla_breach_rate = (
    100 * sla_breaches / sla_total
    if sla_total > 0 else 0
)

service_evidence = (
    f"Overall SLA breach rate = {sla_breach_rate:.2f}%; "
    f"total complaint records = {len(comp):,}; "
    f"complaints with known SLA outcomes = {sla_total:,}."
)


# 9.6 COLLECTION EFFICIENCY
total_due = pd.to_numeric(
    reps["due_amount"], errors="coerce"
).fillna(0).sum()

total_paid = pd.to_numeric(
    reps["paid_amount"], errors="coerce"
).fillna(0).sum()

collection_efficiency = (
    100 * total_paid / total_due
    if total_due > 0 else 0
)

collection_evidence = (
    f"Overall paid-to-due amount ratio = "
    f"{collection_efficiency:.2f}% across the available "
    f"repayment records."
)


# 9.7 BUILD FINDINGS TABLE
findings = pd.DataFrame([
    {
        "finding": "Credit risk: assess non-performing loans",
        "evidence": (
            f"GNPA rate = {gnpa_rate:.2f}%; "
            f"GNPA outstanding = ₹{gnpa_cr:.2f} Cr; "
            f"total loans = {total_loans:,}."
        ),
        "action": (
            "Review the largest NPA accounts, assign collection owners "
            "and prepare a recovery plan for high-risk accounts this week."
        )
    },
    {
        "finding": "Vintage: investigate high-risk disbursal cohorts",
        "evidence": vintage_evidence,
        "action": (
            "Compare the cohort's sourcing channels, bureau scores and "
            "repayment patterns; recommend underwriting changes if "
            "the evidence supports them."
        )
    },
    {
        "finding": "Payments: monitor transaction failures",
        "evidence": payment_evidence,
        "action": (
            "Rank payment partners by failure rate and transaction volume; "
            "ask the highest-impact partners for root-cause analysis "
            "and a corrective action plan."
        )
    },
    {
        "finding": "Payments: investigate the PayNimbus incident",
        "evidence": incident_evidence,
        "action": (
            "Review November 2025 failure reasons with PayNimbus, "
            "reconcile failed transactions and confirm whether customers "
            "were debited or require refunds."
        )
    },
    {
        "finding": "Service: reduce complaint SLA breaches",
        "evidence": service_evidence,
        "action": (
            "Review breached and overdue complaints, assign accountable "
            "owners and track resolution progress in a daily service report."
        )
    },
    {
        "finding": "Collections: monitor repayment efficiency",
        "evidence": collection_evidence,
        "action": (
            "Identify overdue accounts and weak-performing branches, "
            "prioritise collection calls and review progress against "
            "daily recovery targets."
        )
    }
])


# 9.8 DISPLAY RESULTS

print("\n" + "=" * 70)
print("FINDINGS FOR MANAGEMENT")
print("=" * 70)

print(findings.to_string(index=False))

# Optional: export findings for your final report

findings.to_csv("findings.csv", index=False)

print("\nFindings saved to findings.csv")



# 10. HAND-OFF CHECKLIST


import os

print("\n" + "=" * 70)
print("FINEDGE CAPITAL - MODULE 3 HAND-OFF CHECKLIST")
print("=" * 70)

checklist = []

# 1. Data-quality report has at least 12 issues
dq_issue_count = len(dq_report)

checklist.append({
    "check": "DQ report contains at least 12 issues",
    "status": "PASS" if dq_issue_count >= 12 else "FAIL",
    "details": f"{dq_issue_count} issues recorded"
})

# 2. Validation assertions
# Recheck the core cleaned-loan conditions
loan_id_unique = loans["loan_id"].is_unique
disbursal_dates_present = loans["disbursal_date"].notna().all()
emi_values_valid = (
    pd.to_numeric(loans["emi_amount"], errors="coerce")
    .notna().all()
)

checklist.append({
    "check": "Loan IDs are unique",
    "status": "PASS" if loan_id_unique else "FAIL",
    "details": f"{loans['loan_id'].nunique():,} unique IDs / {len(loans):,} rows"
})

checklist.append({
    "check": "No missing disbursal dates",
    "status": "PASS" if disbursal_dates_present else "FAIL",
    "details": f"{loans['disbursal_date'].isna().sum():,} missing dates"
})

checklist.append({
    "check": "No missing or invalid EMI values",
    "status": "PASS" if emi_values_valid else "FAIL",
    "details": f"{loans['emi_amount'].isna().sum():,} missing EMI values"
})

# 3. Star-schema CSV files
required_files = [
    "dim_date.csv",
    "dim_customer.csv",
    "dim_branch.csv",
    "dim_product.csv",
    "dim_channel.csv",
    "fact_applications.csv",
    "fact_loans.csv",
    "fact_repayments.csv",
    "fact_transactions.csv",
    "fact_complaints.csv",
    "fact_targets.csv"
]

missing_files = [
    filename for filename in required_files
    if not os.path.exists(os.path.join(STAR, filename))
]

checklist.append({
    "check": "Star-schema CSVs exported",
    "status": "PASS" if not missing_files else "FAIL",
    "details": (
        "All 11 expected files exist"
        if not missing_files
        else "Missing: " + ", ".join(missing_files)
    )
})

# 4. Findings table has at least five entries
findings_count = len(findings)

checklist.append({
    "check": "At least five management findings",
    "status": "PASS" if findings_count >= 5 else "FAIL",
    "details": f"{findings_count} findings"
})

# 5. Every finding has evidence and an action
findings_complete = (
    findings[["finding", "evidence", "action"]]
    .fillna("")
    .astype(str)
    .apply(lambda col: col.str.strip().ne(""))
    .all()
    .all()
)

checklist.append({
    "check": "Every finding has evidence and action",
    "status": "PASS" if findings_complete else "FAIL",
    "details": "Finding, evidence and action are populated"
})

# 6. Data-quality report treatment column
treatment_columns = [
    col for col in dq_report.columns
    if any(word in col.lower()
           for word in ["treatment", "action", "resolution", "disposition"])
]

if treatment_columns:
    treatment_col = treatment_columns[0]
    treatments_complete = (
        dq_report[treatment_col].fillna("").astype(str).str.strip().ne("")
    ).all()
    treatment_details = f"Treatment column: {treatment_col}"
    treatment_status = "PASS" if treatments_complete else "FAIL"
else:
    treatment_details = "No treatment/action column found in dq_report"
    treatment_status = "FAIL"

checklist.append({
    "check": "DQ issues have stated treatments",
    "status": treatment_status,
    "details": treatment_details
})

# 7. Display checklist
checklist_df = pd.DataFrame(checklist)

print(checklist_df.to_string(index=False))

# 8. Save checklist
checklist_df.to_csv("handoff_checklist.csv", index=False)

print("\nChecklist saved to handoff_checklist.csv")
print(f"Star-schema folder: {os.path.abspath(STAR)}")

if (checklist_df["status"] == "FAIL").any():
    print("\nHAND-OFF STATUS: NOT READY")
    print("Fix the failed checks before submitting the project.")
else:
    print("\nHAND-OFF STATUS: CHECKS PASSED")


