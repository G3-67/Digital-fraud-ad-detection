from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL 
import MySQLdb.cursors
from logging import FileHandler,WARNING
import os
import sys
import cv2
app = Flask(__name__)

app.secret_key = 'many random bytes' 
 
cars_cascade = cv2.CascadeClassifier('haarcascade_car.xml')
global cnt
cnt=0

@app.route('/')
def test():   
    return render_template('test.html' )

 
 
 
 
 
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
            
            f = request.files['file']   
            f.save("static/uploads/" + f.filename)

            cars_cascade = cv2.CascadeClassifier('haarcascade_car.xml')
            is_fake = Simulator(f.filename)

            if is_fake:
                flash("Valid Image")
                return redirect(url_for('test'))

            else:
                flash("Fake Image or Invalid Data")      
                return redirect(url_for('test'))
                
        except (Exception) as e:
             exc_type, exc_obj, exc_tb = sys.exc_info()
             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
             print(e,exc_type, fname, exc_tb.tb_lineno)
            
        return render_template('test.html')
     

	  
if __name__ == "__main__":
    #app.run(host='localhost', port=5000)
    app.run()

#pip install Flask-Session
    
