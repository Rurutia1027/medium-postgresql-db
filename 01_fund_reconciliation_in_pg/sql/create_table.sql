-- =============================================
-- Table: bank_account
-- =============================================
CREATE TABLE bank_account (
    id VARCHAR(50) PRIMARY KEY,
    account_no VARCHAR(50) NOT NULL UNIQUE,
    balance NUMERIC(20, 6) NOT NULL,
    unbalance NUMERIC(20, 6) NOT NULL,
    security_money NUMERIC(20, 6) NOT NULL,
    status VARCHAR(36) NOT NULL,
    total_income NUMERIC(20, 6) NOT NULL,
    total_expend NUMERIC(20, 6) NOT NULL,
    today_income NUMERIC(20, 6) NOT NULL,
    today_expend NUMERIC(20, 6) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    sett_amount NUMERIC(20, 6) NOT NULL,
    user_no VARCHAR(50),
    create_time DATE NOT NULL,
    edit_time DATE,
    version BIGINT NOT NULL,
    remark VARCHAR(200)
);

CREATE TABLE bank_account_history (
    id VARCHAR(50) PRIMARY KEY,
    account_no VARCHAR(50) NOT NULL,
    amount NUMERIC(20, 6) NOT NULL,
    balance NUMERIC(20, 6) NOT NULL,
    fund_direction VARCHAR(36) NOT NULL,
    trx_type VARCHAR(36) NOT NULL,
    request_no VARCHAR(36) NOT NULL,
    bank_trx_no VARCHAR(30),
    is_allow_sett VARCHAR(36),
    is_complete_sett VARCHAR(36),
    risk_day INTEGER,
    user_no VARCHAR(50),
    create_time TIMESTAMP NOT NULL,
    edit_time TIMESTAMP,
    version BIGINT NOT NULL,
    remark VARCHAR(200)
);

CREATE TABLE payment_user_bank_account (
    id VARCHAR(50) PRIMARY KEY,
    version BIGINT NOT NULL DEFAULT 0,
    create_time TIMESTAMP NOT NULL,
    edit_time TIMESTAMP,
    creater VARCHAR(100),
    editor VARCHAR(100),
    status VARCHAR(36) NOT NULL,
    user_no VARCHAR(50) NOT NULL,
    bank_name VARCHAR(200) NOT NULL,
    bank_code VARCHAR(50) NOT NULL,
    bank_account_name VARCHAR(100) NOT NULL,
    bank_account_no VARCHAR(36) NOT NULL,
    card_type VARCHAR(36) NOT NULL,
    card_no VARCHAR(36) NOT NULL,
    mobile_no VARCHAR(50) NOT NULL,
    is_default VARCHAR(36),
    province VARCHAR(20),
    city VARCHAR(20),
    areas VARCHAR(20),
    street VARCHAR(300),
    bank_account_type VARCHAR(36) NOT NULL
);
