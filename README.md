# PostgreSQL Experiment Lab for Blog Articles 
This repository is a **PostgreSQL lab environment** built to support articles published on Medium and other blog platforms. 
Each folder contains datasets, SQL scripts, and mock data scripts written in Python for validating concetps discussed in technical blog posts on [Medium](https://medium.com/@rurutia1027/list/pgdbtopic-2bd18224e127). 

## Supported Blog Articles 

## Complete EDR Diagram 
This section covers the core business data tables for banking, payment platforms, and e-commerce platforms, which serve as the foundation for my blog. It further elaborates on the data queries and index creations used in various subsequent validation stages, all selected from the current data models.  

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
    primary key (id)
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
    primary key (id)
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
   key idx_user_no (user_no)
) comment = 'Stores user-linked bank account and card data for initiating and managing payments.';
```

- **payment_trade_order_record** 

```sql 
-- =============================================
-- Table: payment_trade_order_record
-- Description: Represents merchant-submitted orders before payment occurs.
-- =============================================

create table payment_trade_order_record (
   id                         varchar(50) not null comment 'Primary identifier',
   version                    int not null default 0 comment 'Record version (for optimistic locking)',
   create_time                datetime not null comment 'Timestamp of record creation',
   editor                     varchar(100) comment 'Last modified by',
   creater                    varchar(100) comment 'Record created by',
   edit_time                  datetime comment 'Last modification timestamp',
   status                     varchar(50) comment 'Order status (refer to enum: OrderStatusEnum)',
   product_name               varchar(300) comment 'Product or service name',
   merchant_order_no          varchar(30) not null comment 'Merchant-side order reference',
   order_amount               decimal(20,6) default 0 comment 'Total order amount (EUR)',
   order_from                 varchar(30) comment 'Order source channel (e.g., Web, App)',
   merchant_name              varchar(100) comment 'Registered merchant name',
   merchant_no                varchar(100) not null comment 'Unique merchant ID assigned by platform/acquirer',
   order_time                 datetime comment 'Time of order submission',
   order_date                 date comment 'Date of order placement',
   order_ip                   varchar(50) comment 'Client IP address at order time (captured on gateway page)',
   order_referer_url          varchar(100) comment 'Referring page URL (for anti-fraud purposes)',
   return_url                 varchar(600) comment 'Client-side callback URL after payment',
   notify_url                 varchar(600) comment 'Server-side asynchronous callback URL',
   cancel_reason              varchar(600) comment 'Reason for order cancellation (if applicable)',
   order_period               smallint comment 'Order validity period (in minutes)',
   expire_time                datetime comment 'Order expiration timestamp',
   pay_way_code               varchar(50) comment 'Payment method code (e.g., IBAN_TRANSFER, CARD_EU)',
   pay_way_name               varchar(100) comment 'Payment method name',
   remark                     varchar(200) comment 'Internal note or merchant comment regarding payment',
   trx_type                   varchar(30) comment 'Transaction type (e.g., PURCHASE, TOPUP)',
   trx_no                     varchar(50) comment 'Platform-level payment transaction reference',
   pay_type_code              varchar(50) comment 'Payment channel type code (e.g., STRIPE, AIB, PAYPAL)',
   pay_type_name              varchar(100) comment 'Payment channel name',
   fund_into_type             varchar(30) comment 'Fund flow type (e.g., TO_ESCROW, DIRECT_TO_MERCHANT)',
   is_refund                  varchar(30) default '101' comment 'Indicates if refund occurred (100 = Yes, 101 = No)',
   refund_times               int default 0 comment 'Number of successful refunds issued',
   success_refund_amount      decimal(20,6) comment 'Total amount refunded successfully (EUR)',
   field1                     varchar(500) comment 'Custom field 1 (reserved)',
   field2                     varchar(500) comment 'Custom field 2 (reserved)',
   field3                     varchar(500) comment 'Custom field 3 (reserved)',
   field4                     varchar(500) comment 'Custom field 4 (reserved)',
   field5                     varchar(500) comment 'Custom field 5 (reserved)',
   primary key (id),
   unique key ak_key_2 (merchant_order_no, merchant_no)
) 
comment = 'Merchant order table representing submitted orders and metadata before payment processing.';
```

- **payment_trade_record** 
```sql 
-- =============================================
-- Table: payment_trade_record
-- Description: Final record for a completed transaction.
-- =============================================

create table payment_trade_record (
   id                     varchar(50) not null comment 'Primary identifier of the payment record',
   version                int not null default 0 comment 'Version number (for optimistic locking)',
   create_time            datetime comment 'Record creation timestamp',
   status                 varchar(30) comment 'Transaction status (refer to enum: PaymentRecordStatusEnum)',
   editor                 varchar(100) comment 'Last modified by',
   creater                varchar(100) comment 'Created by',
   edit_time              datetime comment 'Last modified timestamp',
   product_name           varchar(50) comment 'Product or service name',
   merchant_order_no      varchar(50) not null comment 'Merchant-side order number',
   trx_no                 varchar(50) not null comment 'Platform transaction reference number',
   bank_order_no          varchar(50) comment 'Bank-side order number',
   bank_trx_no            varchar(50) comment 'Bank transaction reference number',
   merchant_name          varchar(300) comment 'Merchant business name',
   merchant_no            varchar(50) not null comment 'Merchant identifier',
   payer_user_no          varchar(50) comment 'Payer user identifier',
   payer_name             varchar(60) comment 'Payer full name',
   payer_pay_amount       decimal(20,6) default 0 comment 'Amount paid by payer',
   payer_fee              decimal(20,6) default 0 comment 'Transaction fee charged to payer',
   payer_account_type     varchar(30) comment 'Payer account type (refer to enum: AccountTypeEnum)',
   receiver_user_no       varchar(15) comment 'Payee user identifier',
   receiver_name          varchar(60) comment 'Payee full name',
   receiver_pay_amount    decimal(20,6) default 0 comment 'Amount received by payee',
   receiver_fee           decimal(20,6) default 0 comment 'Transaction fee charged to payee',
   receiver_account_type  varchar(30) comment 'Payee account type (refer to enum: AccountTypeEnum)',
   order_ip               varchar(30) comment 'IP address from which the order was placed (client IP)',
   order_referer_url      varchar(100) comment 'Referrer URL for fraud monitoring or analytics',
   order_amount           decimal(20,6) default 0 comment 'Total order amount',
   plat_income            decimal(20,6) comment 'Platform income from this transaction',
   fee_rate               decimal(20,6) comment 'Fee rate applied to the transaction',
   plat_cost              decimal(20,6) comment 'Platform cost associated with the transaction',
   plat_profit            decimal(20,6) comment 'Net profit from this transaction',
   return_url             varchar(600) comment 'Callback URL for user-facing frontend',
   notify_url             varchar(600) comment 'Callback URL for backend asynchronous notification',
   pay_way_code           varchar(50) comment 'Payment method code',
   pay_way_name           varchar(100) comment 'Payment method name (e.g., Credit Card, SEPA)',
   pay_success_time       datetime comment 'Timestamp of successful payment',
   complete_time          datetime comment 'Timestamp of full transaction completion',
   is_refund              varchar(30) default '101' comment 'Indicates whether refund occurred (100: Yes, 101: No)',
   refund_times           int default 0 comment 'Number of refund occurrences (default: 0)',
   success_refund_amount  decimal(20,6) comment 'Total successfully refunded amount',
   trx_type               varchar(30) comment 'Transaction type (e.g., Purchase, Top-up)',
   order_from             varchar(30) comment 'Channel/source from which the order originated',
   pay_type_code          varchar(50) comment 'Payment type code',
   pay_type_name          varchar(100) comment 'Payment type name (e.g., Instant, Scheduled)',
   fund_into_type         varchar(30) comment 'Fund flow direction (e.g., to platform, merchant)',
   remark                 varchar(3000) comment 'Additional remarks or notes',
   field1                 varchar(500) comment 'Reserved field 1 (custom extension)',
   field2                 varchar(500) comment 'Reserved field 2 (custom extension)',
   field3                 varchar(500) comment 'Reserved field 3 (custom extension)',
   field4                 varchar(500) comment 'Reserved field 4 (custom extension)',
   field5                 varchar(500) comment 'Reserved field 5 (custom extension)',
   bank_return_msg        varchar(2000) comment 'Bank-side response message',
   primary key (id),
   unique key ak_key_2 (trx_no)
)
comment = 'Final payment record detailing all financial attributes of a processed order.';
```
- **payment_refund_transaction_record** 

```sql 

-- =============================================
-- Table: payment_refund_transaction_record
-- Description: Tracks refund transactions tied to original payments, including refund amounts, statuses, 
--              related bank references, and auit metadata (e.g., requestor ID, timestamps).
-- =============================================
create table payment_refund_transaction_record (
   id                         varchar(50) not null comment 'Primary identifier',
   version                    int not null comment 'Record version (optimistic locking)',
   create_time                datetime comment 'Record creation timestamp',
   editor                     varchar(100) comment 'Last modified by (editor)',
   creater                    varchar(100) comment 'Created by (creator)',
   edit_time                  datetime comment 'Last modification timestamp',
   org_merchant_order_no      varchar(50) comment 'Original merchant order reference',
   org_trx_no                 varchar(50) comment 'Original payment transaction ID',
   org_bank_order_no          varchar(50) comment 'Original acquiring bank order reference',
   org_bank_trx_no            varchar(50) comment 'Original acquiring bank transaction reference',
   merchant_name              varchar(100) comment 'Merchant business name',
   merchant_no                varchar(100) not null comment 'Merchant ID (assigned by platform/acquirer)',
   org_product_name           varchar(60) comment 'Original product or service name',
   org_biz_type               varchar(30) comment 'Original transaction business type (e.g., Purchase, Top-Up)',
   org_payment_type           varchar(30) comment 'Original payment method type (e.g., Card, IBAN)',
   refund_amount              decimal(20,6) comment 'Refund amount (EUR)',
   refund_trx_no              varchar(50) not null comment 'Unique refund transaction ID (internal)',
   refund_order_no            varchar(50) not null comment 'Refund order reference number',
   bank_refund_order_no       varchar(50) comment 'Bank-side refund order reference',
   bank_refund_trx_no         varchar(30) comment 'Bank-side refund transaction reference',
   result_notify_url          varchar(500) comment 'Notification URL for refund result callback',
   refund_status              varchar(30) comment 'Current status of the refund (e.g., Pending, Completed, Failed)',
   refund_from                varchar(30) comment 'Originating platform or gateway for the refund',
   refund_way                 varchar(30) comment 'Refund method (e.g., Original Route, Manual Bank Transfer)',
   refund_request_time        datetime comment 'Time of refund request submission',
   refund_success_time        datetime comment 'Timestamp when refund was successfully processed',
   refund_complete_time       datetime comment 'Finalization timestamp of refund completion',
   request_apply_user_id      varchar(50) comment 'User login ID who requested the refund',
   request_apply_user_name    varchar(90) comment 'Full name of the user who requested the refund',
   refund_reason              varchar(500) comment 'Stated reason for the refund request (e.g., Duplicate Payment)',
   remark                     varchar(3000) comment 'Internal notes or merchant comments regarding the refund',
   primary key (id),
   unique key ak_key_2 (refund_trx_no)
);
```
- **payment_settlement_record** 

```sql 
-- =============================================
-- Table: payment_settlement_record
-- Description: Records details of settlements to user or merchant accounts, including account/bank info, 
--              remittance metadata, fees, and operator/audit data. 
-- =============================================

create table payment_settlement_record (
   id                        varchar(50) not null comment 'Primary record ID',
   version                   int not null default 0 comment 'Record version (used for concurrency control)',
   create_time               datetime not null comment 'Record creation timestamp',
   edit_time                 datetime comment 'Last modification timestamp',
   sett_mode                 varchar(50) comment 'Settlement initiation method (see enum: SettlementModeTypeEnum)',
   account_no                varchar(20) not null comment 'Internal settlement account number',
   user_no                   varchar(20) comment 'Platform user ID',
   user_name                 varchar(200) comment 'User full name (as registered)',
   user_type                 varchar(50) comment 'User type (e.g., INDIVIDUAL, MERCHANT, PSP)',
   sett_date                 date comment 'Date settlement was initiated',
   bank_code                 varchar(20) comment 'Bank BIC or institution code',
   bank_name                 varchar(100) comment 'Bank name',
   bank_account_name         varchar(60) comment 'Name on bank account (beneficiary)',
   bank_account_no           varchar(20) comment 'Bank account number (IBAN or local)',
   bank_account_type         varchar(50) comment 'Type of bank account (e.g., IBAN, SORT_CODE)',
   country                   varchar(200) comment 'Country of the bank',
   province                  varchar(50) comment 'Province/state where the bank is located (if applicable)',
   city                      varchar(50) comment 'City of the bank branch',
   areas                     varchar(50) comment 'Local area or district of the branch',
   bank_account_address      varchar(300) comment 'Full name/address of the bank branch',
   mobile_no                 varchar(20) comment 'Recipient mobile number (for confirmation, if required)',
   sett_amount               decimal(24,10) comment 'Gross settlement amount (EUR)',
   sett_fee                  decimal(16,6) comment 'Settlement service fee deducted (EUR)',
   remit_amount              decimal(16,2) comment 'Final remitted amount to beneficiary (EUR)',
   sett_status               varchar(50) comment 'Settlement status (see enum: SettlementRecordStatusEnum)',
   remit_confirm_time        datetime comment 'Timestamp when remittance was confirmed',
   remark                    varchar(200) comment 'Settlement notes or description',
   remit_remark              varchar(200) comment 'Remarks regarding remittance details',
   operator_loginname        varchar(50) comment 'Operator system login ID',
   operator_realname         varchar(50) comment 'Operator real name (for audit)',
   primary key (id)
); 
```


### Ecommerce Platform Model

- **ecommerce_merchant_profile**
```sql 
-- =============================================
-- Table: ecommerce_merchant_profile
-- Description:  Stores merchant registration and business identify info for the e-commerce platform in Ireland. 
--               Includes regulatory(PPS/CRO), banking, contact, and storefront details. 
-- =============================================

create table ecommerce_merchant_profile (
   id                   varchar(50) not null comment 'Primary key',
   version              int not null default 0 comment 'Version number for optimistic locking',
   create_time          datetime not null comment 'Creation timestamp',
   created_by           varchar(100) comment 'User who created the record',
   edit_time            datetime not null comment 'Last modification timestamp',
   edited_by            varchar(100) comment 'User who last modified the record',

   status               varchar(50) not null comment 'Registration status (e.g. pending, approved)',
   business_code        varchar(32) not null comment 'Business registration reference code',
   merchant_id          varchar(32) comment 'Merchant platform ID (e.g. from Stripe, Revolut)',

   legal_name           varchar(100) not null comment 'Legal name of the individual or company',
   pps_number           varchar(20) comment 'Personal Public Service (PPS) Number for individuals',
   business_number      varchar(32) comment 'Company Registration Number (CRO) for registered businesses',

   bank_account_name    varchar(100) not null comment 'Bank account holder name',
   iban                 varchar(34) not null comment 'IBAN (International Bank Account Number)',
   bic                  varchar(11) comment 'BIC (Bank Identifier Code)',

   store_name           varchar(128) not null comment 'Trading name or shop name',
   store_county         varchar(100) not null comment 'County of business operation (e.g. Dublin, Cork)',
   store_city           varchar(100) not null comment 'City or town where store is located',
   store_street         varchar(255) not null comment 'Street address of the store',
   eircode              varchar(10) comment 'Irish postal code (Eircode)',

   store_front_pic      varchar(256) comment 'Photograph of the storefront',
   store_interior_pic   varchar(256) comment 'Photograph of the interior layout or product display',

   merchant_alias       varchar(50) not null comment 'Short display name used for UI or customer reference',
   contact_phone        varchar(20) not null comment 'Primary business phone number',
   support_phone        varchar(20) comment 'Customer support number (optional)',
   business_description varchar(255) comment 'Description of goods/services offered by the business',
   fee_rate             varchar(50) comment 'Commission or fee rate applied to transactions',
   email_address        varchar(100) comment 'Primary business contact email address',
   website_url          varchar(200) comment 'Business website (optional)',

   primary key (id)
); 
```

## License 
[LICENSE](./LICENSE)