from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, List, Optional 
import datetime
import sqlite3
from contextlib import asynccontextmanager

DATABASE_URL = "transactiondata.db"

def db_initialisation():
    con = sqlite3.connect(DATABASE_URL)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Transactions
    (
    id Integer PRIMARY KEY AUTOINCREMENT,
    description Text NOT NULL,
    amount Real NOT NULL,
    category Text NOT NULL,
    type Text NOT NULL,
    date Text NOT NULL
    )""")
    con.commit()
    con.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Database is being initialized...")
    db_initialisation()
    print("Database initialized successfully.")
    yield

app = FastAPI(lifespan=lifespan)
class Transaction(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    type: Literal['income', 'expense']
    date: datetime.date



current_id = 1
#Helper
def convert_to_transaction(transaction_row: tuple):
    converted_transaction = Transaction(
        id = transaction_row[0],
        description = transaction_row[1],
        amount = transaction_row[2],
        category = transaction_row[3],
        type = transaction_row[4],
        date = transaction_row[5]
    )
    return converted_transaction
#Helper
def find_transaction_by_id(transaction_id: int) -> Optional[Transaction]:
    con = sqlite3.connect(DATABASE_URL)
    cur = con.cursor()
    cur.execute("SELECT * FROM Transactions WHERE id=?",(transaction_id,))
    specific_transaction = cur.fetchone()
    con.close()
    if specific_transaction:
        converted_transaction = convert_to_transaction(specific_transaction)
        return converted_transaction
    return None

#Helper
def convert_to_tuple(transaction: Transaction):
    transaction_tuple = (transaction.description,transaction.amount,
                         transaction.category,transaction.type,transaction.date.isoformat())
    return transaction_tuple

@app.post("/api/transactions")
def create_new_transaction(transaction: Transaction) -> Transaction:
    con = sqlite3.connect(DATABASE_URL)
    cur = con.cursor()
    transaction_data = convert_to_tuple(transaction)
    cur.execute("""
    INSERT INTO Transactions (description, amount, category, type, date)
    VALUES (?, ?, ?, ?, ?);
""", transaction_data)
    con.commit()
    new_id = cur.lastrowid
    con.close()

    transaction.id = new_id
    return transaction

@app.get("/api/transactions")
def get_all_transactions() -> List[Transaction]:
    con = sqlite3.connect(DATABASE_URL)
    cur = con.cursor()
    cur.execute("SELECT * FROM Transaction")
    db: List[Transaction] = []
    all_transactions = cur.fetchall()
    con.close()
    for transaction in all_transactions:
        converted_transaction = convert_to_transaction(transaction)
        db.append(converted_transaction)
    return db


@app.delete("/api/transactions")
def delete_all_transactions() -> dict:
    con = sqlite3.connect(DATABASE_URL)
    cur = con.cursor()
    cur.execute("DELETE FROM Transactions")
    con.commit()
    con.close()
    return {"message": "All transactions deleted successfully"}
        
@app.get("/api/transactions/{transaction_id}")
def get_specific_transaction(transaction_id: int) -> Transaction:
    specific_transaction = find_transaction_by_id(transaction_id)
    if specific_transaction is None: 
        raise HTTPException(status_code=404, detail="Transaction not found")
    else:
        return specific_transaction
    
@app.delete("/api/transactions/{transaction_id}") 
def delete_specific_transaction(transaction_id: int) -> dict:
    transaction_to_delete = find_transaction_by_id(transaction_id)
    
    #Check if it exists
    if not transaction_to_delete:
        raise HTTPException(status_code=404, detail="Transaction not found")
    else:
        con = sqlite3.connect(DATABASE_URL)
        cur = con.cursor()
        cur.execute("DELETE FROM Transactions WHERE id=?",(transaction_id,))
        con.commit()
        con.close()
    return {"message": "Transaction deleted successfully"}
    
    
@app.put("/api/transactions/{transaction_id}")
def update_specific_transaction(transaction_id: int, new_transaction: Transaction) -> Transaction:
# find old transaction, make sure it actually exists
    transaction_to_update = find_transaction_by_id(transaction_id)
    if not transaction_to_update:
        raise HTTPException(status_code=404, detail="Transaction not found")
    con = sqlite3.connect(DATABASE_URL)  
    cur = con.cursor()
    new_transaction_tuple = convert_to_tuple(new_transaction)
    cur.execute("""UPDATE Transactions SET description = ?, amount = ? 
                category = ?, type = ?, date = ?
                WHERE id=?""",new_transaction_tuple + (transaction_id,)
                )
    con.commit()
    con.close()
    new_transaction.id = transaction_id
    return new_transaction