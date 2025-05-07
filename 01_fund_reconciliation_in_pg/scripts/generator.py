from random import randrange, choice 
from datetime import datetime, timedelta 
import psycopg2 
from psycopg2.extras import execute_values 
import csv 
import declxml as xml 
import os 
import glob 

CONNECTION = psycopg2.connect(user = os.environ["POSTGRES_USER"], 
                                password=os.environ["POSTGRES_PASSWORD"],
                                host="oltp",
                                port="5432",
                                database="sales_oltp")

def generate_bank_account_records(n = 100):
    statuses = ['ACTIVE', "FROZEN"]
    types = ['CORPORATE', 'INDIVIDUAL']
    bank_accounts = [] 

    for _ in range(n):
        now = datetime.now() 
        account = {
            'id': str(uuid4()),
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
                unique(account_no),
                key idx_user_no (user_no)
            )
        """)

        query = "INSERT INTO bank_account({}) VALUES %s".format(','.join(columns))
        values = [[row[col] for col in columns] for row in accounts]
        execute_values(cur, query, values)

        conn.commit()
        print(f"{len(accounts)} records inserted.")