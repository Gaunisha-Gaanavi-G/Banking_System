from sqlalchemy import *
from sqlalchemy.sql import *
engine=create_engine('mysql://root:admin@127.0.0.1:3306/banking',echo=True)

class Bank:
    def __init__(self):
        self.metadata=MetaData()
        self.customers = Table("customers",self.metadata,autoload=True,autoload_with=engine)
        self.transactions = Table("transactions",self.metadata,autoload=True,autoload_with=engine)

    def get_customers(self):
        stmt = self.customers.select()
        result=engine.execute(stmt)
        res=[dict(r) for r in result] if result else None
        if res: 
            return res
        else:
            return None

    def get_customers_info(self,id):
        stmt=self.customers.select().where(self.customers.c.Customer_Id==id)
        result=engine.execute(stmt)
        res=[dict(r) for r in result] if result else None
        if res:
            return res[0]
        else:
            return None

    def get_receiver_info(self,account_no):
        stmt=self.customers.select().where(self.customers.c.Account_number==account_no)
        result=engine.execute(stmt)
        res=[dict(r) for r in result] if result else None
        if res:
            return res[0]
        else: 
            return None

    def insert_into_transaction(self,data):
        stmt=engine.execute(self.transactions.insert().values(Trans_id= data['Trans_id'],
        Sender_name = data['Sender_name'],
        Receiver_name= data['Receiver_name'],
        Transfered_amount =  data['Transfered_amount'],
        Sender_account = data['Sender_account'],
        Receiver_account = data['Receiver_account'],
        Date = data['Date']),
        Message = data['Message'])
        if stmt:
            return stmt
        else:
            return None

    def update_customers(self,balance_sender,balance_receiver,sender_id,receiver_id):
        stmt1=self.customers.update().where(self.customers.c.Customer_Id==sender_id).values(Balance=balance_sender)
        stmt2=self.customers.update().where(self.customers.c.Customer_Id==receiver_id).values(Balance=balance_receiver)
        result1 = engine.execute(stmt1)
        result2=engine.execute(stmt2)

    def get_history(self):
        stmt=self.transactions.select()
        result=engine.execute(stmt)
        res=[dict(r) for r in result] if result else None
        if res: 
            return res
        else:
            return None


