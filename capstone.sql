/*CREATE TABLE stg_customers (
    customer_id             TEXT,
    customer_name           TEXT,
    gender                  TEXT,
    date_of_birth           TEXT,
    mobile_number           TEXT,
    email                   TEXT,
    city                    TEXT,
    state                   TEXT,
    pincode                 TEXT,
    occupation              TEXT,
    employer_name           TEXT,
    monthly_income          TEXT,
    kyc_status              TEXT,
    customer_segment        TEXT,
    relationship_start_date TEXT
);


CREATE TABLE stg_applications (
    application_id          TEXT,
    customer_id             TEXT,
    product_id              TEXT,
    branch_id               TEXT,
    channel                 TEXT,
    application_date        TEXT,
    requested_amount        TEXT,
    tenure_months           TEXT,
    bureau_score            TEXT,
    declared_monthly_income TEXT,
    application_status      TEXT,
    decision_date           TEXT,
    rejection_reason        TEXT
);

CREATE TABLE stg_loans (
    loan_id                   TEXT,
    application_id            TEXT,
    customer_id               TEXT,
    product_id                TEXT,
    branch_id                 TEXT,
    channel                   TEXT,
    disbursal_date            TEXT,
    sanctioned_amount         TEXT,
    disbursed_amount          TEXT,
    interest_rate             TEXT,
    tenure_months             TEXT,
    emi_amount                TEXT,
    first_emi_date            TEXT,
    bureau_score_at_disbursal TEXT,
    loan_status               TEXT,
    outstanding_principal     TEXT,
    total_amount_paid         TEXT,
    dpd_days                  TEXT,
    npa_flag                  TEXT,
    insurance_opted           TEXT
);

CREATE TABLE stg_repayments (
    repayment_id        TEXT,
    loan_id             TEXT,
    installment_no      TEXT,
    due_date            TEXT,
    due_amount          TEXT,
    principal_component TEXT,
    interest_component  TEXT,
    paid_date           TEXT,
    paid_amount         TEXT,
    payment_mode        TEXT
);

CREATE TABLE stg_transactions (
    transaction_id       TEXT,
    customer_id          TEXT,
    transaction_datetime TEXT,
    transaction_type     TEXT,
    merchant_category    TEXT,
    merchant_name        TEXT,
    transaction_amount   TEXT,
    transaction_status   TEXT,
    payment_partner      TEXT,
    device_type          TEXT,
    city                 TEXT,
    failure_reason       TEXT
);

CREATE TABLE stg_complaints (
    complaint_id       TEXT,
    customer_id        TEXT,
    loan_id            TEXT,
    product_id         TEXT,
    branch_id          TEXT,
    received_date      TEXT,
    complaint_category TEXT,
    received_channel   TEXT,
    priority           TEXT,
    sla_days           TEXT,
    resolved_date      TEXT,
    complaint_status   TEXT
);*/


/*CREATE TABLE dim_branch (
    branch_id       VARCHAR(50) PRIMARY KEY,
    branch_name     VARCHAR(200) NOT NULL,
    city            VARCHAR(100),
    state           VARCHAR(100),
    region          VARCHAR(100),
    zone            VARCHAR(100),
    branch_type     VARCHAR(100),
    branch_manager  VARCHAR(200),
    opened_date     DATE
);*/
--drop table if exists  dim_product;

/*CREATE TABLE dim_product (
    product_id           varchar(60) PRIMARY KEY,
    product_name        varchar(50) NOT NULL,
    product_category    varchar(50),
    min_amount          NUMERIC,
    max_amount          NUMERIC,
    min_tenure_months   INTEGER,
    max_tenure_months   INTEGER,
    base_interest_rate  NUMERIC,
    processing_fee_pct  NUMERIC
);*/

--DROP TABLE IF EXISTS fact_targets;

/*CREATE TABLE fact_target (
    target_month                     DATE,
    branch_id                        varchar(50) REFERENCES dim_branch(branch_id),
    target_disbursal_amount          NUMERIC,
    target_accounts                  INTEGER,
    target_collection_efficiency_pct NUMERIC,
    target_month_key                NUMERIC
);*/







/*BULK INSERT stg_customers
FROM 'C:\Users\harat\Downloads\clean dataset\customers_clean.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);*/



/*BULK INSERT stg_applications
FROM 'C:\Users\harat\Downloads\clean dataset\loan_applications_clean.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
)*/

/*BULK INSERT stg_loans 
FROM 'C:\Users\harat\Downloads\clean dataset\loans_clean.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
)*/


/*BULK INSERT stg_repayments
FROM 'C:\Users\harat\Downloads\clean dataset\repayments_clean.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
)*/

/*BULK INSERT stg_transactions
FROM 'C:\Users\harat\Downloads\clean dataset\transactions_clean.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
)*/



/*BULK INSERT stg_complaints
FROM 'C:\Users\harat\Downloads\clean dataset\complaints_clean.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
)*/



/*BULK INSERT dim_branch
FROM 'C:\Users\harat\Downloads\clean dataset\branches_clean.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
)*/


/*BULK INSERT dim_product
FROM 'C:\Users\harat\Downloads\clean dataset\products_clean.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
)*/

--select * from dim_product

/*BULK INSERT fact_target

FROM 'C:\Users\harat\Downloads\clean dataset\monthly_targets_clean.csv'
WITH
(
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
)*/






/*SELECT 'stg_customers'    AS table_name, COUNT(*) AS rows_loaded FROM stg_customers
UNION ALL SELECT 'stg_applications',  COUNT(*) FROM stg_applications
UNION ALL SELECT 'stg_loans',         COUNT(*) FROM stg_loans
UNION ALL SELECT 'stg_repayments',    COUNT(*) FROM stg_repayments
UNION ALL SELECT 'stg_transactions',  COUNT(*) FROM stg_transactions
UNION ALL SELECT 'stg_complaints',    COUNT(*) FROM stg_complaints
UNION ALL SELECT 'dim_branch',        COUNT(*) FROM dim_branch
UNION ALL SELECT 'dim_product',       COUNT(*) FROM dim_product
UNION ALL SELECT 'fact_target',      COUNT(*) FROM fact_target;*/






/*SELECT
      customer_id           ,
    customer_name           ,
    gender                  ,
    date_of_birth           ,
    mobile_number           ,
    email                   ,
    city                    ,
    state                   ,
    pincode                 ,
    occupation              ,
    employer_name           ,
    monthly_income          ,
    kyc_status              ,
    customer_segment        ,
    relationship_start_date
INTO dim_customer
FROM stg_customers;*/



--select*from dim_customer



/*CREATE TABLE dim_channel (
    channel                    varchar(50) PRIMARY KEY,
    channel_group              varchar (50),
    is_digital                 INTEGER,
    acquisition_cost_per_login NUMERIC
);*/


/*INSERT INTO dim_channel VALUES
    ('Branch Walk-in',   'Physical', 0, 420),
    ('DSA',              'Sourced',  0, 950),
    ('Digital App',      'Digital',  1, 180),
    ('Website',          'Digital',  1, 260),
    ('Telecalling',      'Assisted', 0, 610),
    ('Partner Referral', 'Sourced',  0, 780);*/


    --SELECT * FROM stg_applications ;


/*SELECT *
INTO fact_applications
FROM stg_applications
      
--select top 10* from fact_applications

SELECT *
INTO fact_loans
FROM stg_loans

SELECT *
INTO fact_repayments
FROM stg_repayments


SELECT *
INTO fact_transactions
FROM stg_transactions


SELECT *
INTO fact_complaints
FROM stg_complaints*/



/*SELECT
    TABLE_NAME,
    COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN
(
    'fact_loans',
    'fact_applications',
    'fact_repayments',
    'fact_transactions',
    'fact_complaints',
    'dim_customer'
)
ORDER BY TABLE_NAME, ORDINAL_POSITION;*/

/*SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME IN
(
    'stg_loans',
    'stg_customers',
    'stg_applications',
    'stg_repayments',
    'stg_transactions',
    'dq_rejected_loans',
    'dq_issue_log'
);*/


/*SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'dq_rejected_loans';

SELECT l.*
INTO dq_rejected_loans
FROM stg_loans l
LEFT JOIN dim_customer c
    ON LTRIM(RTRIM(CAST(l.customer_id AS VARCHAR(MAX)))) =
       LTRIM(RTRIM(CAST(c.customer_id AS VARCHAR(MAX))))
WHERE c.customer_id IS NULL;

SELECT COUNT(*) AS rejected_loans
FROM dq_rejected_loans;*/




/*DROP TABLE IF EXISTS dq_issue_log;

SELECT *
INTO dq_issue_log
FROM
(
    -- Duplicate loan IDs
   SELECT
        'stg_loans' AS source_table,
        'Duplicate loan_id rows' AS rule_name,
        COUNT(*) - COUNT(DISTINCT CAST(loan_id AS VARCHAR(MAX))) AS rows_affected
    FROM stg_loans

    UNION ALL

    -- Duplicate customer IDs
    SELECT
        'stg_customers',
        'Duplicate customer_id rows',
        COUNT(*) - COUNT(DISTINCT CAST(customer_id AS VARCHAR(MAX)))
    FROM stg_customers

    UNION ALL

    -- Duplicate application IDs
    SELECT
        'stg_applications',
        'Duplicate application_id rows',
        COUNT(*) - COUNT(DISTINCT CAST(application_id AS VARCHAR(MAX)))
    FROM stg_applications

    UNION ALL

    -- Duplicate repayment IDs
    SELECT
        'stg_repayments',
        'Duplicate repayment_id rows',
        COUNT(*) - COUNT(DISTINCT CAST(repayment_id AS VARCHAR(MAX)))
    FROM stg_repayments

    UNION ALL

    -- Duplicate transaction IDs
    SELECT
        'stg_transactions',
        'Duplicate transaction_id rows',
        COUNT(*) - COUNT(DISTINCT CAST(transaction_id AS VARCHAR(MAX)))
    FROM stg_transactions

    UNION ALL

    -- Orphan loans
    SELECT
        'stg_loans',
        'Orphan customer_id (no master record)',
        COUNT(*)
    FROM dq_rejected_loans
) AS dq;

SELECT *
FROM dq_issue_log;*/



/*SELECT 'dim_customer' AS tbl, COUNT(*) AS rows FROM dim_customer
UNION ALL SELECT 'fact_applications', COUNT(*) FROM fact_applications
UNION ALL SELECT 'fact_loans',        COUNT(*) FROM fact_loans
UNION ALL SELECT 'fact_repayments',   COUNT(*) FROM fact_repayments
UNION ALL SELECT 'fact_transactions', COUNT(*) FROM fact_transactions
UNION ALL SELECT 'fact_complaints',   COUNT(*) FROM fact_complaints
UNION ALL SELECT 'dq_rejected_loans', COUNT(*) FROM dq_rejected_loans;*/








