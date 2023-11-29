from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL 
import MySQLdb.cursors
from logging import FileHandler,WARNING
import os
import sys
import cv2
app = Flask(__name__)
app.secret_key = 'many random bytes'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'OnlineAds'

fh=FileHandler('errorlog.txt')
fh.setLevel(WARNING)

app.logger.addHandler(fh)

mysql = MySQL(app)
app.secret_key = os.urandom(24)
 
cars_cascade = cv2.CascadeClassifier('cars4.xml')
global cnt
cnt=0

@app.route('/')
def home():   
    return render_template('Homepage.html' )

@app.route('/about')
def about():   
    return render_template('Aboutus.html' )

@app.route('/contact')
def contact():   
    return render_template('Contactus.html' )


@app.route('/Register')
def Register(): 
    cur = mysql.connection.cursor()
    cur.execute("select MAX(Regid) from Register")
    data = cur.fetchone()
    rid=data[0]
    if rid==None:
            rid="1"
            print(rid)
    else:         
         rid=rid+1            
     
    return render_template('Register.html',Regid=rid)

 
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        
        try:
            Regid = request.form['Regid']  
            rname  = request.form['rname']
            gender = request.form['gender']
            contact = request.form['contact']
            email = request.form['email']
            Address = request.form['Address']
            city = request.form['city']
            role = request.form['role']
            uname = request.form['uname']
            password = request.form['password']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Register (rname, gender,contact,email,Address,city,role,uname,password) VALUES(%s, %s, %s, %s,%s,%s,%s,%s,%s)", (rname, gender,contact,email,Address,city,role,uname,password))

            mysql.connection.commit()
            flash("Data Inserted Successfully")      
            return redirect(url_for('Register')) 
        except (Exception) as e: 
             print(e)
        return render_template('Register.html')

@app.route('/checklogin', methods = ['POST'])
def checklogin():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        utype=request.form['utype']
        if username=='Admin' and password=='Admin' and utype=='Admin':
           return redirect(url_for('viewpost1'))
        else:          
            cur = mysql.connection.cursor() 
            cur.execute("SELECT  uname,password,role FROM Register WHERE uname = '%s' AND password = '%s'"% (username, password))
            account = cur.fetchone() 
            uname,pw,role=account 
            if account :
                if role=="Seller":
                    cur.close()                
                    return redirect(url_for('postads'))
                elif role=="Buyer":
                    cur.close()                
                    return redirect(url_for('viewpost'))            
            else:
                flash("Record not found")    
    return render_template('login.html')

@app.route('/viewpost')
def viewpost():
    cur = mysql.connection.cursor()
    cur.execute("select * from PostAds")
    data = cur.fetchall() 
    return render_template('ViewAds.html',postlist=data)

@app.route('/viewpost1')
def viewpost1():
    cur = mysql.connection.cursor()
    cur.execute("select * from PostAds")
    data = cur.fetchall() 
    return render_template('ViewAds1.html',postlist=data)

@app.route('/postads')
def postads():
    cur = mysql.connection.cursor()
    cur.execute("select MAX(postid) from PostAds")
    data = cur.fetchone()
    postid=data[0]
    if postid==None:
            postid="1" 
    else:         
         postid=postid+1   
    return render_template('PostAds.html',postid=postid)
 
def detect_cars(frame):
    cars = cars_cascade.detectMultiScale(frame, 1.15, 4)
    print(len(cars),"checkpoint2")
    for (x, y, w, h) in cars:
        num=cv2.rectangle(frame, (x, y), (x+w,y+h), color=(0, 255, 0), thickness=2)
    if len(cars):
        print(True)
        return True
    else:
        print(False)
        return False

def Simulator(video):
    print("checkpointpre")
    imgUMat = cv2.imread("static/uploads/"+video)
    print("checkpointprett")
    res = detect_cars(imgUMat)
    return res
    

    
@app.route('/insertAds', methods = ['POST'])
def insertAds():
    if request.method == "POST":
        print("checkpointpre1232")
        try:
            postid = request.form['postid']  
            ownername  = request.form['ownername']
            contact = request.form['contact']
            vname = request.form['vname']
            vtype = request.form['vtype']
            vnumber = request.form['vnumber']
            vmodelno = request.form['vmodelno'] 
            vmodelname = request.form['vmodelname']
            postalcode = request.form['postalcode']
            address = request.form['address']
            noofowner = request.form['noofowner']
            description = request.form['description']
            price = request.form['price']
            f = request.files['file']   
            f.save("static/uploads/" + f.filename)

            cars_cascade = cv2.CascadeClassifier('cars4.xml')
            is_fake = Simulator(f.filename)

            if is_fake:
                cur = mysql.connection.cursor()
                cur.execute("SELECT  ownername,vnumber,vname,vmodelno,vmodelname,pincode FROM Vehicledetails  where ownername = '%s' AND vnumber = '%s' AND vname = '%s' AND vmodelno = '%s' AND vmodelname = '%s' AND pincode = '%s'  "%
                            (ownername,vnumber,vname,vmodelno,vmodelname,postalcode ))
                data = cur.fetchone()
                cur.close()
                if data:                        
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO postads (ownername, contact,vname,vtype,vnumber,vmodelno,vmodelname,postalcode,address,noofowner,description,price,video)  VALUES(%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (ownername, contact,vname,vtype,vnumber,vmodelno,vmodelname,postalcode,address,noofowner, description,price,f.filename))

                    mysql.connection.commit()
                    flash("Data Inserted Successfully")      
                return redirect(url_for('postads'))

            else:
                flash("Fake Image or Invalid Data")      
                return redirect(url_for('postads'))
            
          
          
        except (Exception) as e:
             exc_type, exc_obj, exc_tb = sys.exc_info()
             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
             print(e,exc_type, fname, exc_tb.tb_lineno)
            
        return render_template('Register.html')
    
@app.route('/login')
def login():   
    return render_template('Login.html' )

@app.route('/Logout')
def Logout():   
    return render_template('Login.html' )

@app.route('/Addfeedback')
def Addfeedback(): 
    return render_template('Feedback.html'   )

@app.route('/Viewfeedback')
def Viewfeedback():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM feedback")
    data = cur.fetchall() 
    cur.close()
    return render_template('Viewfeedback.html', feedbacklist=data )


 
@app.route('/insertfeedback', methods = ['POST'])
def insertfeedback():
    if request.method == "POST":        
        try:
            cdate = request.form['cdate']  
            clientname  = request.form['clientname']
            prodname = request.form['prodname']
            prodtype = request.form['prodtype']
            feedback = request.form['feedback']
            description = request.form['descri'] 
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Feedback (cdate,clientname,prodname,prodtype,feedback,description) VALUES ( %s, %s, %s,%s,%s,%s)",
                        (cdate,clientname,prodname,prodtype,feedback,description))

            mysql.connection.commit()
            flash("Data Inserted Successfully")      
            return redirect(url_for('Addfeedback')) 
        except (Exception) as e: 
             print(e)
        return redirect(url_for('Addfeedback'))

@app.route('/rules')
def rules():   
    return render_template('Rules.html' )

	  
if __name__ == "__main__":
    #app.run(host='localhost', port=5000)
    app.run()

#pip install Flask-Session
    
