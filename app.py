from flask import *  
import sqlite3 
#con = sqlite3.connect("employee.db", check_same_thread=False)
import employeedb
 

app = Flask(__name__, static_url_path='')  
app.secret_key = 'this is a secret key'
 
@app.route("/")  
def index():  
    return render_template("getin.html");  
 
@app.route("/add")  
def add():  
    return render_template("add.html")  
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        #database variable names:-
        #DescriptionOfGoods
        #HSNSAC
        #Qty
        #RatePerUnit
        #Gst
        #TaxableValue
        #Cgst
        #Sgst
        #TotalAmount

        DescriptionOfGoods = request.form.get("DescriptionOfGoods")
        HSNSAC = request.form.get("HSNSAC") 
        Qty = request.form.get("Qty")
        RatePerUnit = round(float(request.form.get("RatePerUnit")),2)
        Gst = round(float(request.form.get("Gst")),2)

        #cgst = gst/2
        #sgst = gst/2

        TaxableValue = (RatePerUnit) * float(Qty)
        totaltax = round((TaxableValue*(Gst))/100,2)
        Cgst=round(totaltax/2,2)
        Sgst=round(totaltax/2,2)
        TotalAmount = round((TaxableValue + totaltax),2)
        
        #with sqlite3.connect("employee.db", check_same_thread=False) as con:  
        #cur = con.cursor()  
        #exist = cur.fetchone()
        #cur.execute("INSERT into SnDA (DescriptionOfGoods, HSNSAC, Qty, RatePerUnit, Gst, TaxableValue, Cgst, Sgst, TotalAmount) values (?,?,?,?,?,?,?,?,?)", (DescriptionOfGoods,HSNSAC,Qty,RatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount))  
        #con.commit()  
        employeedb.addData(DescriptionOfGoods,HSNSAC,Qty,RatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount)
        msg = "Data successfully Added"  
        return render_template("success.html",msg = msg)

        #except:  
        #    #con.rollback()  
        #    msg = "We can not add the Data to the list"  
        #finally:  
        #    return render_template("success.html",msg = msg)  
        #    #con.close()  
    else:
        msg = "We can not add the Data to the list"
        return render_template("success.html",msg = msg)
 
@app.route("/view")  
def view():  
    #con = sqlite3.connect("employee.db")  
    #con.row_factory = sqlite3.Row  
    #cur = con.cursor()  
    #cur.execute("select DescriptionOfGoods, HSNSAC, Qty, RatePerUnit, Gst, TaxableValue, Cgst, Sgst, TotalAmount from SnDA")  
    #cur.execute("select * from SnDA")  
    rows = employeedb.viewData()
    return render_template("view.html",rows = rows)  
  

@app.route("/deleterecord/<row_id>",methods = ["POST"])  
def deleterecord(row_id):  
    #id = request.form["id"]  
    employeedb.delete(row_id)
    msg = "record successfully deleted!"
    return render_template("delete_record.html",msg = msg)  

@app.route("/edit/<row_id>",methods=["POST"])
def getdata(row_id):
    data = employeedb.getdata(row_id)
    return render_template("edit.html", data=data)

@app.route("/editdetails/<eid>",methods = ["POST","GET"])  
def editDetails(eid):
    msg = "Data edited successfully!"  
    DescriptionOfGoods = request.form.get("DescriptionOfGoods")
    HSNSAC = request.form.get("HSNSAC") 
    Qty = request.form.get("Qty")
    RatePerUnit = round(float(request.form.get("RatePerUnit")),2)
    Gst = round(float(request.form.get("Gst")),2)

    #cgst = gst/2
    #sgst = gst/2

    TaxableValue = (RatePerUnit) * float(Qty)
    totaltax = round((TaxableValue*(Gst))/100,2)
    Cgst=round(totaltax/2,2)
    Sgst=round(totaltax/2,2)
    TotalAmount = round((TaxableValue + totaltax),2)
    employeedb.edit(eid,DescriptionOfGoods,HSNSAC,Qty,RatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount)
    return render_template("success.html",msg = msg)
    #else:
    #    msg = "We can not add the Data to the list"
    #    return render_template("success.html",msg = msg)

@app.route("/signup",methods = ["POST","GET"])  
def signup():
    render_template("signup.html")

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5001, debug=True)