from flask import *  
import sqlite3 
#con = sqlite3.connect("employee.db", check_same_thread=False)
import employeedb,loginDB
import os
 

app = Flask(__name__, static_url_path='')  

#In order to use session in flask you need to set the secret key in your application settings. secret key is a random key used to encrypt your cookies and save send them to the browser
app.secret_key = 'this is a secret key'

#set app root name into a variable
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#checking login.py and extracting email id as cookie
#storing all data of paricular email specified into the user variable
#storing into individual variables using user list
#if cookie present in browser then go to getin.html else login.html
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

#function redirects to login.html
@app.route("/login")
def login():
    return render_template("login.html")
    
#from login.html data is taken and stored into email & password
#user password takes password from db and checks with the form password if they are same
#(important) create http response create
#cookie is set using response(resp) object where 'email' is the title from cookie, email is the content from the form, and max_age is the time within which the cookie expires  
#returning the response object to everyone else password fails return to login
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


@app.route("/signup")  
def signup():
    return render_template("signup.html")

#target variable stores the path to the profile images 
#taking data from form
#else condition is not understood
#.filename name retrive
#.save() function saves the image in the desired path
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

#why no content in this cookie
@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('email', expires=0)
    return resp

#request.cookies.get pulls the email cookie from browser
#all the below functions have requested cookie as if condition else redirected to login panel
#reason being we remove access from entering website using the urls shown
#hence removing unauthorized access
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

@app.route("/savedetails/exc",methods = ["POST","GET"])  
def saveDetailsExc(): 
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
            Qty = (request.form.get("Qty"))
            ExcRatePerUnit = round(float(request.form.get("ExcRatePerUnit")),2)
            Gst = round(float(request.form.get("Gst")),2)
            IncRatePerUnit = round((ExcRatePerUnit + (ExcRatePerUnit*Gst)/100),2)
            
            TaxableValue = round(((ExcRatePerUnit) * float(Qty)),2)
            totaltax = round((TaxableValue*(Gst))/100,2)
            Cgst=round(totaltax/2,2)
            Sgst=round(totaltax/2,2)
            TotalAmount = round((TaxableValue + totaltax),2)

            #exclRate = round((RatePerUnit - (RatePerUnit*Gst/100)),2)
            #TaxableValue = round(((exclRate) * float(Qty)),2)
            #totaltax = round(((RatePerUnit*float(Qty))-TaxableValue),2)
            #Cgst=round(totaltax/2,2)
            #Sgst=round(totaltax/2,2)
            #TotalAmount = round((TaxableValue + totaltax),2)#

            email = request.cookies.get('email')
            
            employeedb.addData(DescriptionOfGoods,HSNSAC,Qty,ExcRatePerUnit,IncRatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount,email)
            msg = "Data successfully Added"  
            return render_template("success.html",msg = msg,email=email,name=name,image=image)
        else:
            msg = "We can not add the Data to the list"
            return render_template("success.html",msg = msg,email=email,name=name,image=image)
    else:
        return redirect(url_for('login'))

#####################################################

@app.route("/savedetails/inc",methods = ["POST","GET"])  
def saveDetailsInc(): 
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
            Qty = (request.form.get("Qty"))
            IncRatePerUnit = round(float(request.form.get("IncRatePerUnit")),2)
            Gst = round(float(request.form.get("Gst")),2)
            ExcRatePerUnit = round(((IncRatePerUnit*100)/(100+Gst)),2)
            
            TaxableValue = round(((ExcRatePerUnit) * float(Qty)),2)
            totaltax = round((TaxableValue*(Gst))/100,2)
            Cgst=round(totaltax/2,2)
            Sgst=round(totaltax/2,2)
            TotalAmount = round((TaxableValue + totaltax),2)

            #exclRate = round((RatePerUnit - (RatePerUnit*Gst/100)),2)
            #TaxableValue = round(((exclRate) * float(Qty)),2)
            #totaltax = round(((RatePerUnit*float(Qty))-TaxableValue),2)
            #Cgst=round(totaltax/2,2)
            #Sgst=round(totaltax/2,2)
            #TotalAmount = round((TaxableValue + totaltax),2)#

            email = request.cookies.get('email')
            
            employeedb.addData(DescriptionOfGoods,HSNSAC,Qty,ExcRatePerUnit,IncRatePerUnit,Gst,TaxableValue,Cgst,Sgst,TotalAmount,email)
            msg = "Data successfully Added"  
            return render_template("success.html",msg = msg,email=email,name=name,image=image)
        else:
            msg = "We can not add the Data to the list"
            return render_template("success.html",msg = msg,email=email,name=name,image=image)
    else:
        return redirect(url_for('login'))

#################################################


@app.route("/view")  
def view():  
    if (request.cookies.get('email')): 
        #image = loginDB.userImage(request.cookies.get('email'))
        user = loginDB.getUser(request.cookies.get('email'))
        email = user[0][0]
        name = user[0][1]
        image = user[0][3]
          
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
        #email = user[0][0]
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
        Qty = float(request.form.get("Qty"))
        ExcRatePerUnit = round(float(request.form.get("ExcRatePerUnit")),2)
        Gst = round(float(request.form.get("Gst")),2)
        IncRatePerUnit = round((ExcRatePerUnit + (ExcRatePerUnit*Gst)/100),2)
        
        TaxableValue = round(((ExcRatePerUnit) * float(Qty)),2)
        totaltax = round((TaxableValue*(Gst))/100,2)
        Cgst=round(totaltax/2,2)
        Sgst=round(totaltax/2,2)
        TotalAmount = round((TaxableValue + totaltax),2)

        #exclRate = round((RatePerUnit - (RatePerUnit*Gst/100)),2)
        #TaxableValue = round(((exclRate) * float(Qty)),2)
        #totaltax = round(((RatePerUnit*float(Qty))-TaxableValue),2)
        #Cgst=round(totaltax/2,2)
        #Sgst=round(totaltax/2,2)
        #TotalAmount = round((TaxableValue + totaltax),2)
    
        employeedb.edit(eid,DescriptionOfGoods,HSNSAC,Qty,ExcRatePerUnit,IncRatePerUnit, Gst,TaxableValue,Cgst,Sgst,TotalAmount,email)
        return render_template("success.html",msg = msg, email=email, name=name, image=image)
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5001, debug=True)