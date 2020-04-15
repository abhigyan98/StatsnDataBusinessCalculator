import sqlite3  
  
con = sqlite3.connect("employee.db", check_same_thread=False)  
db = con.cursor()
print("Database opened successfully")  

#con.execute("create table IF NOT EXISTS SnD (id INTEGER PRIMARY KEY AUTOINCREMENT, DescriptionOfGoods VARCHAR(30) NOT NULL, HSNSAC NUMBER , Qty NUMBER NOT NULL, ExcRatePerUnit NUMBER NOT NULL, IncRatePerUnit NUMBER NOT NULL, Gst NUMBER NOT NULL, TaxableValue NUMBER NOT NULL, Cgst NUMBER NOT NULL, Sgst NUMBER NOT NULL, TotalAmount NUMBER NOT NULL, Email VARCHAR2(30) NOT NULL)")  
#con.execute("create table Userss (id INTEGER PRIMARY KEY , name TEXT NOT NULL, email TEXT NOT NULL, password VARCHAR(20) NOT NULL)")  
def createTable():
    #con.execute("create table IF NOT EXISTS SnD (id INTEGER PRIMARY KEY AUTOINCREMENT, DescriptionOfGoods VARCHAR(30) NOT NULL, HSNSAC NUMBER , Qty NUMBER NOT NULL, ExcRatePerUnit NUMBER NOT NULL, IncRatePerUnit NUMBER NOT NULL, Gst NUMBER NOT NULL, TaxableValue NUMBER NOT NULL, Cgst NUMBER NOT NULL, Sgst NUMBER NOT NULL, TotalAmount NUMBER NOT NULL, Email VARCHAR2(30) NOT NULL)")  
    print("Table created successfully")
  

def addData(DescriptionOfGoods,HSNSAC,Qty,ExcRatePerUnit,IncRatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount,Email):
    db.execute("INSERT INTO SnD VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)",(DescriptionOfGoods,HSNSAC,Qty,ExcRatePerUnit,IncRatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount, Email))
    con.commit()

def viewData(email):
    db.execute("SELECT * FROM SnD WHERE Email=(?)",(email,))
    data = db.fetchall()
    return data

def delete(rid):
    db.execute("DELETE FROM SnD WHERE id=(?)",(rid,))
    con.commit()

def edit(rid,DescriptionOfGoods,HSNSAC,Qty,ExcRatePerUnit,IncRatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount,Email):
    db.execute("UPDATE SnD SET DescriptionOfGoods=(?),HSNSAC=(?),Qty=(?),ExcRatePerUnit=(?),IncRatePerUnit=(?),Gst=(?),TaxableValue=(?),Cgst=(?),Sgst=(?),TotalAmount=(?),Email=(?) WHERE id=(?)",(DescriptionOfGoods,HSNSAC,Qty,ExcRatePerUnit,IncRatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount,Email,rid))
    con.commit()

def getdata(rid):
    db.execute("SELECT * FROM SnD WHERE id=(?)",(rid,))
    data = db.fetchall()
    return data
#createTable()
#con.close()