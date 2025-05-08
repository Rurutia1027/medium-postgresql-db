import random
from random import randrange, choice 
from datetime import datetime, timedelta 
import psycopg2 
from psycopg2.extras import execute_values 
import uuid 

def generate_bank_account_records(n = 100):
    statuses = ['ACTIVE', "FROZEN"]
    types = ['CORPORATE', 'INDIVIDUAL']
    bank_accounts = [] 

    for _ in range(n):
        now = datetime.now() 
        account = {
            'id': str(uuid.uuid4()),
            'account_no': f'ACC{random.randint(1000000, 9999999)}',
            'balance': round(random.uniform(1000, 100000), 6),
            'unbalance': round(random.uniform(0, 1000), 6),
            'security_money': round(random.uniform(0, 500), 6),
            'status': random.choice(statuses),
            'total_income': round(random.uniform(10000, 500000), 6),
            'total_expend': round(random.uniform(1000, 400000), 6),
            'today_income': round(random.uniform(0, 10000), 6),
            'today_expend': round(random.uniform(0, 10000), 6),
            'account_type': random.choice(types),
            'sett_amount': round(random.uniform(0, 10000), 6),
            'user_no': f'USER{random.randint(1000, 9999)}',
            'create_time': now,
            'edit_time': now + timedelta(minutes=random.randint(0, 60)),
            'version': 1,
            'remark': 'Auto-generated test record'
        }
        bank_accounts.append(account)
    return bank_accounts

def insert_bank_accounts(): 
    print('Inserting bank accounts')

    accounts = generate_bank_account_records()
    # here we fetch column names as list 
    columns = accounts[0].keys()

    with CONNECTION as conn: 
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS bank_account")
        cur.execute("""
             CREATE TABLE bank_account (
                id                  varchar(50) primary key, 
                account_no          varchar(50) not null, 
                balance             decimal(20, 6) not null, 
                unbalance           decimal(20, 6) not null, 
                security_money      decimal(20, 6) not null, 
                status              varchar(36) not null, 
                total_income        decimal(20, 6) not null, 
                total_expend        decimal(20, 6) not null, 
                today_income        decimal(20, 6) not null, 
                today_expend        decimal(20, 6) not null, 
                account_type        varchar(50) not null, 
                sett_amount         decimal(20, 6) not null, 
                user_no             varchar(50), 
                create_time         timestamp not null,
                edit_time           timestamp, 
                version             bigint not null,
                remark              varchar(200), 
                unique(account_no)
            )
        """)

        query = "INSERT INTO bank_account({}) VALUES %s".format(','.join(columns))
        values = [[row[col] for col in columns] for row in accounts]
        execute_values(cur, query, values)

        conn.commit()
        print(f"{len(accounts)} records inserted.")

def generate_bank_account_history(account_nos, n_per_account=3):
    trx_types = ['PAYMENT', 'REFUND', 'SETTLEMENT']
    directions = ['IN', 'OUT']
    records = []

    for account_no in account_nos:
        balance = round(random.uniform(1000, 100000), 6)

        for _ in range(n_per_account):
            amount = round(random.uniform(100, 5000), 6)
            direction = random.choice(directions)
            trx_type = random.choice(trx_types)

            if direction == 'OUT':
                balance = max(0, balance - amount)
            else:
                balance = balance + amount

            now = datetime.now()
            record = {
                'id': str(uuid.uuid4()),
                'account_no': account_no,
                'amount': amount,
                'balance': balance,
                'fund_direction': direction,
                'trx_type': trx_type,
                'request_no': f'REQ{random.randint(100000, 999999)}',
                'bank_trx_no': f'BANK{random.randint(100000, 999999)}',
                'is_allow_sett': random.choice(['Y', 'N']),
                'is_complete_sett': random.choice(['Y', 'N']),
                'risk_day': random.randint(0, 7),
                'user_no': f'USER{random.randint(1000, 9999)}',
                'create_time': now,
                'edit_time': now + timedelta(minutes=random.randint(1, 60)),
                'version': 1,
                'remark': 'Auto-generated txn record'
            }

            records.append(record)

    return records


def insert_bank_account_history():
    print("Inserting bank account history records")

    with CONNECTION as conn:
        cur = conn.cursor()

        # Get account_no list from existing bank_account table
        cur.execute("SELECT account_no FROM bank_account LIMIT 20")
        account_nos = [row[0] for row in cur.fetchall()]

        # Drop and recreate the table
        cur.execute("DROP TABLE IF EXISTS bank_account_history")
        cur.execute("""
            CREATE TABLE bank_account_history (
                id varchar(50) primary key, 
                account_no varchar(50) not null, 
                amount decimal(20, 6) not null, 
                balance decimal(20, 6) not null, 
                fund_direction varchar(36) not null, 
                trx_type varchar(36) not null, 
                request_no varchar(36) not null, 
                bank_trx_no varchar(30), 
                is_allow_sett varchar(36), 
                is_complete_sett varchar(36), 
                risk_day int, 
                user_no varchar(50), 
                create_time timestamp not null, 
                edit_time timestamp, 
                version bigint not null, 
                remark varchar(200)
            )
        """)

        history = generate_bank_account_history(account_nos)
        columns = history[0].keys()
        query = "INSERT INTO bank_account_history ({}) VALUES %s".format(','.join(columns))
        values = [[row[col] for col in columns] for row in history]
        execute_values(cur, query, values)

        conn.commit()
        print(f"{len(history)} records inserted.")     

def generate_payment_user_bank_accounts(n=20):
    banks = ['AIB', 'Barclays', 'Chase', 'HSBC', 'Wells Fargo']
    card_types = ['CREDIT', 'DEBIT']
    account_types = ['PERSONAL', 'BUSINESS']
    statuses = ['ACTIVE', 'DISABLED']

    records = []

    for _ in range(n):
        now = datetime.now()
        record = {
            'id': str(uuid.uuid4()),
            'version': 0,
            'create_time': now,
            'edit_time': now + timedelta(minutes=random.randint(1, 60)),
            'creater': 'system',
            'editor': 'system',
            'status': random.choice(statuses),
            'user_no': f'USER{random.randint(1000, 9999)}',
            'bank_name': random.choice(banks),
            'bank_code': f'BK{random.randint(1000, 9999)}',
            'bank_account_name': f'User{random.randint(100, 999)}',
            'bank_account_no': f'ACCT{random.randint(100000, 999999)}',
            'card_type': random.choice(card_types),
            'card_no': f'****{random.randint(1000, 9999)}',
            'mobile_no': f'08{random.randint(10000000, 99999999)}',
            'is_default': random.choice(['YES', 'NO']),
            'province': 'Leinster',
            'city': 'Dublin',
            'areas': 'District A',
            'street': f'{random.randint(1, 100)} Example St',
            'bank_account_type': random.choice(account_types),
        }
        records.append(record)

    return records


def insert_payment_user_bank_accounts():
    print("Inserting payment user bank account records")

    with CONNECTION as conn:
        cur = conn.cursor()

        # Drop and recreate the table
        cur.execute("DROP TABLE IF EXISTS payment_user_bank_account")
        cur.execute("""
            CREATE TABLE payment_user_bank_account (
                id varchar(50) NOT NULL,
                version bigint NOT NULL DEFAULT 0,
                create_time date NOT NULL,
                edit_time date,
                creater varchar(100),
                editor varchar(100),
                status varchar(36) NOT NULL,
                user_no varchar(50) NOT NULL,
                bank_name varchar(200) NOT NULL,
                bank_code varchar(50) NOT NULL,
                bank_account_name varchar(100) NOT NULL,
                bank_account_no varchar(36) NOT NULL,
                card_type varchar(36) NOT NULL,
                card_no varchar(36) NOT NULL,
                mobile_no varchar(50) NOT NULL,
                is_default varchar(36),
                province varchar(20),
                city varchar(20),
                areas varchar(20),
                street varchar(300),
                bank_account_type varchar(36) NOT NULL,
                PRIMARY KEY (id)
            )
        """)

        data = generate_payment_user_bank_accounts()
        columns = data[0].keys()
        query = "INSERT INTO payment_user_bank_account ({}) VALUES %s".format(','.join(columns))
        values = [[row[col] for col in columns] for row in data]
        execute_values(cur, query, values)

        conn.commit()
        print(f"{len(data)} records inserted.")    


CONNECTION = psycopg2.connect(user = "admin", 
                                password= "admin",
                                host="localhost",
                                port="5432",
                                database="01_fund_reconciliation")

def main():
    try:
        insert_bank_accounts()
        insert_bank_account_history()
        insert_payment_user_bank_accounts()

    except psycopg2.Error as e:
        print(f"Database error: {e}")  

    print("Now close PG DB Connection")   
    CONNECTION.close()         

if __name__ == "__main__":
    main()       