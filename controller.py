from datetime import date, datetime
import re
from flask import *
import uuid
from model.model import Hackaholics
app=Flask(__name__)
app.secret_key = "div"

# session email addresses
email_addresses = []

@app.route('/',methods=["POST","GET"])
def Home():
    if request.method=="GET":
        if 'D_email' in session and session['D_email'] in email_addresses:
            email_addresses.remove(session['D_email'])
            del session['D_email']
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
                return render_template("Patient_home.html",id=out['Id'])            
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("Login.html",email=out['Email'])

        elif output:
            if output['Password']==password:
                if email not in email_addresses:
                    email_addresses.append(email)
                    session['D_email']=email
                    print(email_addresses)
                return render_template("Patient_home.html",id=output['Id'])            
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("Login.html",email=output['Email'])
        else:
            flash("Email you have entered has not been registered. Please register")
            return render_template("Login.html")
        
        
# Patient_home
@app.route("/Patient_home/<id>",methods=["GET","POST"])
def Patient_home(id):
    return render_template("Patient_home.html",id=id)
    
@app.route('/patient_register',methods=["GET","POST"])
def Patient_register():
    obj=Hackaholics()
    if request.method=="GET":
        return render_template('Patient_register.html')
    elif request.method=="POST":
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
        out = obj.insert_into_diagnostics(data['Id'])
        flash("You've been registered successfully!")
        return render_template("login.html")
        
@app.route('/consultation/<id>',methods=["GET"])
def Consultation(id):
    if request.method=="GET":
        return render_template('consultation.html',id=id)

@app.route('/consultation_patient_info/<id>',methods=["GET","POST"])
def Consultation_patient_info(id):
    if request.method=="GET":
        return render_template('consultation_patient_info.html',id=id)

    if request.method=="POST":
        Patient_name = request.form['name']
        Gender=request.form['gender']
        Language=request.form['language']
        Specialization=request.form['specialization']
        
        return redirect(url_for('Consult_filter',id=id,Patient_name = Patient_name,Gender=Gender,Language=Language,Specialization = Specialization,category="all"))


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
        
@app.route('/consult_filter/<id>/<Patient_name>/<Gender>/<Language>/<Specialization>/<category>',methods=["GET","POST"])
def Consult_filter(id,Patient_name,Gender,Language,Specialization,category):
    obj = Hackaholics()
    if request.method=="GET":
        data_doc=[]
        print("email",email_addresses)
        if category == "all":
            out = obj.get_email_doctor_filter_consult(email_addresses,Language,Specialization)
            if out:
                data_doc.append(out)
        elif category == "r_lth":
            out = obj.get_email_doctor_rating_lth_consult(email_addresses,Language,Specialization)
            if out:
                data_doc.append(out)
        elif category == "r_htl":
            out = obj.get_email_doctor_rating_htl_consult(email_addresses,Language,Specialization)
            if out:
                data_doc.append(out)
        elif category == "e_htl":
            out = obj.get_email_doctor_experience_htl_consult(email_addresses,Language,Specialization)
            if out:
                data_doc.append(out)
        elif category == "e_lth":
            out = obj.get_email_doctor_experience_lth_consult(email_addresses,Language,Specialization)
            if out:
                data_doc.append(out)
        elif category == "male":
            out = obj.get_email_doctor_male_consult(email_addresses,Language,Specialization)
            if out:
                data_doc.append(out)
        elif category == "female":
            out = obj.get_email_doctor_female_consult(email_addresses,Language,Specialization)
            if out:
                data_doc.append(out)

        print("data_doc",data_doc)
        if len(data_doc)>0:
            return render_template('consult_filter.html',id=id,Patient_name=Patient_name,Gender=Gender,Language=Language,Specialization=Specialization,data_doc=data_doc[0])

        else:
            return render_template('consult_filter.html',id=id,Patient_name=Patient_name,Gender=Gender,Language=Language,Specialization=Specialization)

@app.route('/consult_meeting_info/<id>/<doc_id>/<doc_name>/<Patient_name>/<Lang>/<Special>',methods=["GET","POST"])
def Consult_meeting_info(id,doc_id,doc_name,Patient_name,Lang,Special):
    if request.method=="GET":
        consultation_id = uuid.uuid4().hex
        obj=Hackaholics()
        insert_consult_data = {
            'ConsultationId':consultation_id,
            'PId': id,
            'DId': doc_id,
            'PName':Patient_name,
            'DName':doc_name,
            'Language': Lang,
            'Status':'Pending',
            'ConsultationDate':date.today().strftime("%Y-%M-%d"),
            'Fees':"500",
            'Speciality':Special,
            'Time':datetime.now().strftime("%H:%M:%S")
        }
        print("insertdata",insert_consult_data)
        out = obj.insert_consult_info(insert_consult_data)
        return render_template('consult_meeting_info.html',id=id,doc_id =doc_id,doc_name = doc_name,Patient_name = Patient_name,Lang = Lang, Special =Special)
    
    elif request.method=="POST":
        rating = request.form['rating']
        print(rating)
        obj=Hackaholics()
        consult_id = obj.get_pending_status()
        out = obj.update_doctor_rating(rating,doc_id)
        out = obj.update_consult_status(consult_id)
        return redirect(url_for('Patient_home',id=id))
    

@app.route('/book_filter/<id>/<Patient_name>/<Gender>/<State>/<District>/<Specialization>/<Description>/<category>',methods=["GET"])
def Book_filter(id,Patient_name,Gender,State,District,Specialization,Description,category):
    obj = Hackaholics()
    if request.method=="GET":
        data_doc=[]
        print("email",email_addresses)
        if category == "all":
            out = obj.get_email_doctor_filter_booking(email_addresses,State,District,Specialization)
            if out:
                data_doc.append(out)
        elif category == "r_lth":
            out = obj.get_email_doctor_rating_lth_booking(email_addresses,State,District,Specialization)
            if out:
                data_doc.append(out)
        elif category == "r_htl":
            out = obj.get_email_doctor_rating_htl_booking(email_addresses,State,District,Specialization)
            if out:
                data_doc.append(out)
        elif category == "e_htl":
            out = obj.get_email_doctor_experience_htl_booking(email_addresses,State,District,Specialization)
            if out:
                data_doc.append(out)
        elif category == "e_lth":
            out = obj.get_email_doctor_experience_lth_booking(email_addresses,State,District,Specialization)
            if out:
                data_doc.append(out)
        elif category == "male":
            out = obj.get_email_doctor_male_booking(email_addresses,State,District,Specialization)
            if out:
                data_doc.append(out)
        elif category == "female":
            out = obj.get_email_doctor_female_booking(email_addresses,State,District,Specialization)
            if out:
                data_doc.append(out)

        print("data_doc",data_doc)
        if len(data_doc)>0:
            return render_template('book_filter.html',id=id,Patient_name=Patient_name,Gender=Gender,State = State,District = District,Specialization=Specialization,Description = Description,data_doc=data_doc[0])

        else:
            return render_template('book_filter.html',id=id,Patient_name=Patient_name,Gender=Gender,State = State,District = District,Specialization=Specialization,Description = Description)

@app.route('/appointment_patient_info/<id>',methods=["GET","POST"])
def Appointment_patient_info(id):
    if request.method=="GET":
        return render_template('appointment_patient_info.html',id=id)

    if request.method=="POST":
        Patient_name = request.form['name']
        Gender=request.form['gender']
        State=request.form['location']
        District = request.form['District']
        Specialization=request.form['specialization']
        Description = request.form['description']
        
        return redirect(url_for('Book_filter',id=id,Patient_name = Patient_name,Gender=Gender,State=State,District = District,Specialization = Specialization,Description = Description,category="all"))

@app.route('/confirm_appointment/<id>/<doc_id>/<doc_name>/<Patient_name>/<State>/<District>/<Specialization>/<Description>',methods=["GET","POST"])
def Confirm_appointment(id,doc_id,doc_name,Patient_name,State,District,Specialization,Description):
    if request.method=="GET":
        appointment_id = uuid.uuid4().hex
        obj=Hackaholics()
        out_patient = obj.get_info_patient(id)
        out_doctor = obj.get_info_doctor(doc_id)
        data = {
            'AppointmentId':appointment_id,
            'PId':id,
            'DId':doc_id,
            'PName':Patient_name,
            'DName':doc_name,
            'PEmail':out_patient['Email'],
            'DEmail':out_doctor['Email'],
            'Status':'Pending',
            'BookingDate':date.today().strftime("%Y-%M-%d"),
            'Fees':500,
            'Description':Description,
            'Time':datetime.now().strftime("%H:%M:%S"),
            'Speciality':Specialization,
            'State':State,
            'District':District
        }
        out = obj.insert_into_booking(data)
        return render_template('confirm_appointment.html',data = data,id=id,appointment_id = appointment_id)

@app.route('/thankyou_appointment/<id>/<appointment_id>',methods=["GET","POST"])
def Thankyou_appointment(id,appointment_id):
    if request.method=="GET":
        return render_template('thankyou_appointment.html',id=id)

    if request.method =="POST":
        Time = request.form['time']
        Date = request.form['date']
        obj = Hackaholics()
        out = obj.update_booking_info(Time,Date,appointment_id)
        return render_template('thankyou_appointment.html',id=id)

@app.route('/thankyou_consultation/<id>/<doc_id>/<doc_name>/<Patient_name>/<Lang>/<Special>',methods=["GET","POST"])
def Thankyou_consultation(id,doc_id,doc_name,Patient_name,Lang,Special):
    if request.method=="GET":
        return render_template('thankyou_consultation.html',id=id,doc_id =doc_id,doc_name = doc_name,Patient_name = Patient_name,Lang = Lang, Special =Special)


if(__name__=="__main__"):
    app.run(debug=True)
