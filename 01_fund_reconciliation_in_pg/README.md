# Fund Reconciliation in PostgreSQL: Indexing, EXPLAIN ANALYZE, and Troubleshotting 

## DB Table Schemas 
### Bank Entities & SQL 
- **bank_account**
```sql 
-- =============================================
-- Table: bank_account
-- Description: Stores current balance, account status, and cumulative transaction history for each user.
-- =============================================

create table bank_account (
    id                  varchar(50) not null comment 'Primary key ID (UUID)', 
    account_no          varchar(50) not null comment 'Unique bank account number', 
    balance             decimal(20, 6) not null comment 'Current available balance', 
    unbalance           decimal(20, 6) not null comment 'Frozen amount in the account', 
    security_money      decimal(20, 6) not null comment 'Security deposit amount for risk control', 
    status              varchar(36) not null comment 'Account status (e.g., ACTIVE, FROZEN)', 
    total_income        decimal(20, 6) not null comment 'Cumulative total income', 
    total_expend        decimal(20, 6) not null comment 'Cumulative total expenditure', 
    today_income        decimal(20, 6) not null comment 'Today total income', 
    today_expend        decimal(20, 6) not null comment 'Today total expenditure', 
    account_type        varchar(50) not null comment 'Account type (e.g., CORPORATE, INDIVIDUAL)', 
    sett_amount         decimal(20, 6) not null comment 'Amount available for settlement', 
    user_no             varchar(50) comment 'Associated user or merchant ID', 
    create_time         datetime not null comment 'Creation timestamp',
    edit_time           datetime comment 'Last modified timestamp', 
    version             bigint not null comment 'Optimistic lock version',
    remark              varchar(200) comment 'Additional remarks or comments', 
    primary key (id),
    unique key uq_account_no(account_no),
    key idx_user_no (user_no)
) comment = 'Bank Account Main Table: Records current balance, status, and cumulative income/expenses'; 
```

- **bank_account_history**
```sql 
-- =============================================
-- Table: bank_account_history
-- Description: Tracks individual transactions and movements in a bank account.
-- =============================================

create table bank_account_history (
    id varchar(50) not null comment 'Primary key ID (UUID)', 
    account_no varchar(50) not null comment 'Bank account number (FK to bank_account#account_no)',
    amount  decimal(20, 6) not null comment 'Transaction amount for this record', 
    balance decimal(20, 6) not null comment 'Account balance snapshot after transaction', 
    fund_direction varchar(36) not null comment 'Fund direction (IN for credit, OUT for debit)', 
    trx_type varchar(36) not null comment 'Transaction type (e.g., PAYMENT, REFUND, SETTLEMENT)', 
    request_no varchar(36) not null comment 'Original business request or order number', 
    bank_trx_no varchar(30) comment 'Bank transaction number (vocher/trace ID)', 
    is_allow_sett varchar(36) comment 'Whether settlement is allowed for this transaction (Y/N)', 
    is_complete_sett varchar(36) comment 'Whether this transaction has been fully settled (Y/N)', 
    risk_day int comment 'Number of risk control days before settlement', 
    user_no varchar(50) comment 'Associated user or merchant ID', 
    create_time datetime not null comment 'Creation timestamp', 
    edit_time datetime comment 'Last modified timestamp', 
    version bigint not null comment 'Optimistic lock version', 
    remark varchar(200) comment 'Additional remarks or comments', 
    primary key (id), 
    key idx_account_no (account_no),
    key idx_user_no (user_no),
    constraint fk_account_no foreign key (account_no) references bank_account(account_no)
) 
comment = 'Bank Account Transaction History: Records each fund movement (e.g., payment, withdrawl, settlement)'; 
```

### Payment Platform Entities & SQL 
- **payment_user_bank_account**
```sql 
-- =============================================
-- Table: payment_user_bank_account
-- Description: Stores user-linked bank account and card metadata for payment processing.
-- =============================================
create table payment_user_bank_account (
   id                      varchar(50) not null comment 'Primary key ID',
   version                 bigint not null default 0 comment 'Version for optimistic locking',
   create_time             datetime not null comment 'Record creation timestamp',
   edit_time               datetime comment 'Record last modified timestamp',
   creater                 varchar(100) comment 'Created by (user/system)',
   editor                  varchar(100) comment 'Edited by (user/system)',
   status                  varchar(36) not null comment 'Account status (active, disabled, etc.)',
   user_no                 varchar(50) not null comment 'User identifier within payment platform',
   bank_name               varchar(200) not null comment 'Bank name (e.g., Barclays, AIB)',
   bank_code               varchar(50) not null comment 'Bank code or SWIFT code',
   bank_account_name       varchar(100) not null comment 'Name on the bank account',
   bank_account_no         varchar(36) not null comment 'Bank account number (encrypted or tokenized)',
   card_type               varchar(36) not null comment 'Card type (e.g., CREDIT, DEBIT)',
   card_no                 varchar(36) not null comment 'Card number (masked/tokenized)',
   mobile_no               varchar(50) not null comment 'Registered phone number',
   is_default              varchar(36) comment 'Is this the user default account (YES/NO)',
   province                varchar(20) comment 'Province or region (if applicable)',
   city                    varchar(20) comment 'City name',
   areas                   varchar(20) comment 'District or area',
   street                  varchar(300) comment 'Street address detail',
   bank_account_type       varchar(36) not null comment 'Account type (e.g., PERSONAL, BUSINESS)',
   field1                  varchar(200) comment 'Reserved field 1',
   field2                  varchar(200) comment 'Reserved field 2',
   primary key (id),
   unique key uq_key_bank_account (user_no, bank_account_no),
   key idx_user_no (user_no)
) comment = 'Stores user-linked bank account and card data for initiating and managing payments.';
```

### Relationships of Entities 





