
from flask import *

app=Flask(__name__)

# Patient_home
@app.route("/Patient_home",methods=["GET","POST"])
def Patient_home():
    return render_template("Patient_home.html")
    
@app.route('/register',methods=["GET"])
def Register():
    if request.method=="GET":
        return render_template('Patient_register.html')


@app.route('/doc_reg',methods=["GET"])
def Doc_Register():
    if request.method=="GET":
        return render_template('Doctor_register.html')

@app.route('/doc_log',methods=["GET"])
def Doc_Login():
    if request.method=="GET":
        return render_template('Doctor_login.html')
        
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

if __name__ == '__main__':
    app.run(debug=True)
