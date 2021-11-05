import re
from flask import *
import uuid
from model.model import Hackaholics
app=Flask(__name__)
app.secret_key = "abc"



@app.route('/',methods=["POST","GET"])
def Home():
    if request.method=="GET":
        return render_template("home.html")

@app.route('/login',methods=["POST","GET"])
def Login():
    obj = Hackaholics()
    if request.method=="GET":
        return render_template("Login.html")
    elif request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        out=obj.get_email_patient(email)
        output=obj.get_email_doctor(email)
        if out:
            if out['Password']==password:
                return render_template("Patient_home.html")            
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("Login.html",email=out['Email'])

        elif output:
            if output['Password']==password:
                return render_template("Patient_home.html")            
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("Login.html",email=output['Email'])
        else:
            flash("Email you have entered has not been registered. Please register")
            return render_template("Login.html")
        
        
# Patient_home
@app.route("/Patient_home",methods=["GET","POST"])
def Patient_home():
    return render_template("Patient_home.html")
    
@app.route('/patient_register',methods=["GET","POST"])
def Patient_register():
    obj=Hackaholics()
    if request.method=="GET":
        return render_template('Patient_register.html')
    if request.method=="POST":
        patient_id = uuid.uuid4().hex
        data={
            'Id':patient_id,
            'Name': request.form['username'],
            'State': request.form['State'],
            'District':request.form['District'],
            'Age':request.form['age'],
            'Email': request.form['email'],
            'Password':request.form['password'],
            'MobileNo':request.form['mobileno']
        }
        out=obj.insert_into_patient(data)
        flash("You've been registered successfully!")
        return render_template("login.html")
        
@app.route('/consultation',methods=["GET"])
def Consultation():
    if request.method=="GET":
        return render_template('consultation.html')

@app.route('/consult/consultation_patient_info',methods=["GET"])
def Consultation_patient_info():
    if request.method=="GET":
        return render_template('consultation_patient_info.html')

@app.route('/patient_profile',methods=["GET"])
def patient_profile():
    if request.method=="GET":
        return render_template('Patient_profile.html')

@app.route('/todays_appointment',methods=["GET"])
def todays_appointment():
    if request.method=="GET":
        return render_template('todays_appointment.html')

@app.route('/rescheduled_appointment',methods=["GET"])
def rescheduled_appointment():
    if request.method=="GET":
        return render_template('rescheduled_appointment.html')
        
@app.route('/consult_filter',methods=["GET"])
def Consult_filter():
    if request.method=="GET":
        return render_template('consult_filter.html')

@app.route('/consult_meeting_info',methods=["GET"])
def Consult_meeting_info():
    if request.method=="GET":
        return render_template('consult_meeting_info.html')

@app.route('/book_appointment',methods=["GET"])
def Book_appointment():
    if request.method=="GET":
        return render_template('book_appointment.html')

@app.route('/appointment_patient_info',methods=["GET"])
def Appointment_patient_info():
    if request.method=="GET":
        return render_template('appointment_patient_info.html')

@app.route('/confirm_appointment',methods=["GET"])
def Confirm_appointment():
    if request.method=="GET":
        return render_template('confirm_appointment.html')

@app.route('/thankyou',methods=["GET"])
def Thankyou():
    if request.method=="GET":
        return render_template('thankyou.html')


if(__name__=="__main__"):
    app.run(debug=True)
