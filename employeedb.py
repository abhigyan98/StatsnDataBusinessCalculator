import sqlite3  
  
con = sqlite3.connect("employee.db", check_same_thread=False)  
db = con.cursor()
print("Database opened successfully")  
  
#con.execute("create table Userss (id INTEGER PRIMARY KEY , name TEXT NOT NULL, email TEXT NOT NULL, password VARCHAR(20) NOT NULL)")  
def createTable():
    con.execute("create table IF NOT EXISTS SnDB (id INTEGER PRIMARY KEY AUTOINCREMENT, DescriptionOfGoods VARCHAR(30) NOT NULL, HSNSAC NUMBER , Qty NUMBER NOT NULL, RatePerUnit NUMBER NOT NULL, Gst NUMBER NOT NULL, TaxableValue NUMBER NOT NULL, Cgst NUMBER NOT NULL, Sgst NUMBER NOT NULL, TotalAmount NUMBER NOT NULL)")  
    print("Table created successfully")
  

def addData(DescriptionOfGoods,HSNSAC,Qty,RatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount):
    db.execute("INSERT INTO SnDB VALUES (NULL,?,?,?,?,?,?,?,?,?)",(DescriptionOfGoods,HSNSAC,Qty,RatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount))
    con.commit()

def viewData():
    db.execute("SELECT * FROM SnDB")
    data = db.fetchall()
    return data

def delete(rid):
    db.execute("DELETE FROM SnDB WHERE id=(?)",(rid,))
    con.commit()

def edit(rid):
    db.execute("INSERT INTO SnDB VALUES (NULL,?,?,?,?,?,?,?,?,?)",(DescriptionOfGoods,HSNSAC,Qty,RatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount))

#createTable()
#con.close()