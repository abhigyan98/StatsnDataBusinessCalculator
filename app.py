from flask import *  
import sqlite3 
#con = sqlite3.connect("employee.db", check_same_thread=False)
import employeedb,loginDB
import os
 

app = Flask(__name__, static_url_path='')  
app.secret_key = 'this is a secret key'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
 
@app.route("/")  
def index():
    if (request.cookies.get('email')):
        user = loginDB.getUser(request.cookies.get('email'))
        email = user[0][0]
        name = user[0][1]
        image = user[0][3]
        return render_template("getin.html",email=email,name=name,image=image)
    else:
        return redirect(url_for('login'))
 
@app.route("/add")  
def add():  
    if (request.cookies.get('email')):
        #email2 = request.cookies.get('email')
        #image2 = loginDB.userImage(email2)
        user = loginDB.getUser(request.cookies.get('email'))
        email = user[0][0]
        name = user[0][1]
        image = user[0][3]
        return render_template("add.html",email=email,name=name,image=image)  
    else:
        return redirect(url_for('login'))
 
@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails(): 
    if (request.cookies.get('email')): 
        msg = "msg"  
        user = loginDB.getUser(request.cookies.get('email'))
        name = user[0][1]
        image = user[0][3]
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

            TaxableValue = (RatePerUnit) * float(Qty)
            totaltax = round((TaxableValue*(Gst))/100,2)
            Cgst=round(totaltax/2,2)
            Sgst=round(totaltax/2,2)
            TotalAmount = round((TaxableValue + totaltax),2)
            email = request.cookies.get('email')
            #with sqlite3.connect("employee.db", check_same_thread=False) as con:  
            #cur = con.cursor()  
            #exist = cur.fetchone()
            #cur.execute("INSERT into SnDA (DescriptionOfGoods, HSNSAC, Qty, RatePerUnit, Gst, TaxableValue, Cgst, Sgst, TotalAmount) values (?,?,?,?,?,?,?,?,?)", (DescriptionOfGoods,HSNSAC,Qty,RatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount))  
            #con.commit()  
            employeedb.addData(DescriptionOfGoods,HSNSAC,Qty,RatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount,email)
            msg = "Data successfully Added"  
            return render_template("success.html",msg = msg,email=email,name=name,image=image)

        else:
            msg = "We can not add the Data to the list"
            return render_template("success.html",msg = msg,email=email,name=name,image=image)
    else:
        return redirect(url_for('login'))
 
@app.route("/view")  
def view():  
    if (request.cookies.get('email')): 
        #image = loginDB.userImage(request.cookies.get('email'))
        user = loginDB.getUser(request.cookies.get('email'))
        email = user[0][0]
        name = user[0][1]
        image = user[0][3]
        #con = sqlite3.connect("employee.db")  
        #con.row_factory = sqlite3.Row  
        #cur = con.cursor()  
        #cur.execute("select DescriptionOfGoods, HSNSAC, Qty, RatePerUnit, Gst, TaxableValue, Cgst, Sgst, TotalAmount from SnDA")  
        #cur.execute("select * from SnDA")  
        rows = employeedb.viewData(request.cookies.get('email'))
        return render_template("view.html",rows = rows,email=email,name=name,image=image)  
    else:
        return redirect(url_for('login'))
  

@app.route("/deleterecord/<row_id>",methods = ["POST"])  
def deleterecord(row_id):
    if (request.cookies.get('email')):   
        #id = request.form["id"]  
        user = loginDB.getUser(request.cookies.get('email'))
        email = user[0][0]
        name = user[0][1]
        image = user[0][3]
        employeedb.delete(row_id)
        msg = "record successfully deleted!"
        return render_template("delete_record.html",msg = msg,email=email,name=name,image=image) 
    else:
        return redirect(url_for('login'))

@app.route("/edit/<row_id>",methods=["POST"])
def getdata(row_id):
    if (request.cookies.get('email')):   
        user = loginDB.getUser(request.cookies.get('email'))
        email = user[0][0]
        name = user[0][1]
        image = user[0][3]
        data = employeedb.getdata(row_id)
        return render_template("edit.html", data=data, name=name, image=image)
    else:
        return redirect(url_for('login'))


@app.route("/editdetails/<eid>",methods = ["POST","GET"])  
def editDetails(eid):
    if (request.cookies.get('email')):
        user = loginDB.getUser(request.cookies.get('email'))   
        email = user[0][0]
        name = user[0][1]
        image = user[0][3]
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
        email = request.cookies.get('email')
        
        employeedb.edit(eid,DescriptionOfGoods,HSNSAC,Qty,RatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount,email)
        return render_template("success.html",msg = msg, email=email, name=name, image=image)
        #else:
        #    msg = "We can not add the Data to the list"
        #    return render_template("success.html",msg = msg)
    else:
        return redirect(url_for('login'))


@app.route("/signup")  
def signup():
    return render_template("signup.html")


@app.route("/signup/user",methods=["POST"])
def createUser():
    target = APP_ROOT+'/static/profilePics'
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    image = request.files.get("image")
    image_filename = ""

    if(image):
        image_filename = image.filename
        destination = "/".join([target,image_filename])
        image.save(destination)
    else:
        image_filename = "img_avatar.png"

    loginDB.createUser(email,name,password,image_filename)
    return redirect(url_for('login'))



@app.route("/login")
def login():
    return render_template("login.html")
    

@app.route("/getin",methods=["POST"])
def getin():
    email = request.form.get("email")
    password = request.form.get("password")
    userPassword = loginDB.getPasswordForLogin(email)

    if(password == userPassword[0][0]):
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('email', email, max_age=60*60*24*7)
        return resp
    else:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('email', expires=0)
    return resp


if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5001, debug=True)