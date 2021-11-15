from flask import *   
from flask_mail import *
from datetime import date
from datetime import datetime
import uuid
from model.model import Hackaholics
import chatbot
app=Flask(__name__)
app.secret_key = "div"


app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'hackaholics4@gmail.com'  
app.config['MAIL_PASSWORD'] = 'DaggUs4#'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

# session email addresses
email_addresses = []





import datetime
app = Flask(__name__) #creating the Flask class object  
app.secret_key="div"

app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'hackaholics4@gmail.com'  
app.config['MAIL_PASSWORD'] = 'DaggUs4#'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/',methods=["POST","GET"])
def Home():
    if request.method=="GET":
        if 'D_email' in session and session['D_email'] in email_addresses:
            email_addresses.remove(session['D_email'])
            del session['D_email']
        return render_template("home.html")



# Doctor Register
@app.route('/Doc_Register',methods=["POST","GET"])
def Doc_SignUp():
    if request.method=="GET":
        return render_template("Doctor_register.html")
    elif request.method=="POST":
        h=Hackaholics()
        Id=uuid.uuid1()
        lang=request.form.getlist('language')
        if 'Tamil' in lang:Tamil=1
        else:Tamil=0
        if 'Telugu' in lang:Telugu=1
        else:Telugu=0
        if 'Kannada' in lang:Kannada=1
        else:Kannada=0
        if 'Hindi' in lang:Hindi=1
        else:Hindi=0
        if 'Malayalam' in lang:Malayalam=1
        else:Malayalam=0
        if 'English' in lang:English=1
        else:English=0
        
        data={
            'Id':Id.hex,
            'Name':request.form["Name"],
            'Degree':request.form["Degree"],
            'State':request.form["State"],
            'District':request.form["District"],
            'Firm':request.form["Firm"],
            'Age':request.form["Age"],
            'Experience':request.form["Experience"],
            'Specialization':request.form["Specialization"],
            'AboutMe':request.form["AboutMe"],
            'Email':request.form["Email"],
            'Password':request.form["Password"],
            'LinkedIn':request.form["LinkedIn"],
            'Facebook':request.form["Facebook"],
            'Tamil':Tamil,
            'Malayalam':Malayalam,
            'Kannada':Kannada,
            'Telugu':Telugu,
            'Hindi':Hindi,
            'English':English,
            'Gender':request.form["Gender"]
        }
        h.insert_into_doctor(data)
        return render_template("Login.html")


# Login For Both Doctor & Patient
@app.route('/login',methods=["POST","GET"])
def Login():
    obj = Hackaholics()
    if request.method=="GET":
        return render_template("Login.html")
    elif request.method=="POST":
        email=request.form["Email"]
        password=request.form["Password"]
        out=obj.get_email_patient(email)
        output=obj.get_email_doctor(email)
        if out:
            if out['Password']==password:
                return redirect(url_for("Patient_home",id=out['Id'])  )          
            else:
                flash("Password is wrong.Please enter correct password")
                return render_template("Login.html",email=out['Email'])

        elif output:
            if output['Password']==password:
                if email not in email_addresses:
                    email_addresses.append(email)
                    session['D_email']=email
                    print(email_addresses)
                return redirect( url_for("Doctor_Home",id=output['Id'],name = output['Name']) )           
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
            'MobileNo':request.form['mobileno'],
            'Gender':request.form['Gender']
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


@app.route('/patient_profile/<id>',methods=["GET","POST"])
def Patient_profile(id):
    if request.method=="GET":
        obj = Hackaholics()
        out = obj.get_info_patient(id)
        return render_template('Patient_profile.html',out=out,id = id)

    if request.method == "POST":
        obj = Hackaholics()
        
        data={
            'Id':id,
            'Name': request.form['username'],
            'State': request.form['State'],
            'District':request.form['District'],
            'Age':request.form['age'],
            'Email': request.form['email'],
            'Password':request.form['password'],
            'MobileNo':request.form['mobileno'],
            'Gender':request.form['Gender']
        }
        out = obj.update_profile_patient(id,data)
        flash("Successfully updated details")
        out = obj.get_info_patient(id)
        return render_template('Patient_profile.html',out = out,id = id)


@app.route('/todays_appointment/<id>',methods=["GET","POST"])
def Todays_appointment_patient(id):
    if request.method=="GET":
        obj = Hackaholics()
        today=obj.get_todays_appointment_patient(id)
        return render_template('todays_appointment.html',id = id, today = today)

@app.route('/prescription_patient/<id>',methods=["GET","POST"])
def Prescription_patient(id):
    h=Hackaholics()
    if request.method=="GET":
        res=h.get_appointment_info(id)
        return render_template('prescription_patient.html',out=res,id=id)

#View Prescription Details
@app.route('/Detailed_Prescription/<bid>/<id>',methods=['POST','GET'])
def View_Prescription_Details(bid,id):
    h=Hackaholics()
    if request.method=="GET":
        res=h.get_appointment_info(id)
        prescription=h.get_prescription(bid)
        return render_template('prescription_patient.html',out=res,id=id,prescription=prescription)

@app.route('/rescheduled_appointment_patient/<id>/<appointment_id>',methods=["GET","POST"])
def Rescheduled_appointment_patient(id,appointment_id):
    if request.method == "GET":
        obj = Hackaholics()
        out = obj.get_cancelled_appointment_info(id)
        return render_template('rescheduled_appointment.html',id = id,out = out)

    if request.method =="POST":
        obj = Hackaholics()
        out = obj.get_info_appointment(appointment_id)
        return render_template('confirm_appointment.html',id = id,appointment_id = appointment_id,data = out)

@app.route('/lab_records/<id>',methods=["GET","POST"])
def Lab_records_patient(id):
    if request.method=="GET":
        obj = Hackaholics()
        out = obj.get_info_diagnostics(id)
        return render_template('lab_records.html',id = id, out = out)

    if request.method == "POST":
        obj = Hackaholics()
        data = {
            'CT':request.form['ctscan'],
            'MRI':request.form['mriscan'],
            'ECG':request.form['ECG'],
            'EEG':request.form['EEG'],
            'Gastroscopy':request.form['gastroscopy'],
            'Eye':request.form['eye'],
            'PET':request.form['pet'],
            'Xrays':request.form['xray'],
            'Ultrasound':request.form['ultra'],
            'Biopsy':request.form['biopsy']
        }
        out = obj.update_diagnostics(id,data)
        out = obj.get_info_diagnostics(id)
        return render_template('lab_records.html',id = id, out = out)

        
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
            'ConsultationDate':date.today(),
            'Fees':"500",
            'Speciality':Special,
            'Time':datetime.datetime.now().strftime("%H:%M:%S")
        }
        print("insertdata",insert_consult_data)
        out = obj.insert_consult_info(insert_consult_data)
        return render_template('consult_meeting_info.html',id=id,doc_id =doc_id,doc_name = doc_name,Patient_name = Patient_name,Lang = Lang, Special =Special)
    
    elif request.method=="POST":
        rating = request.form['rating']
        print(rating)
        obj=Hackaholics()
        consult_id = obj.get_pending_status()
        out = obj.get_info_doctor(doc_id)
        old_rating = out['Rating']
        rating = (old_rating+rating)//2
        out = obj.update_doctor_rating(rating,doc_id)
        out = obj.update_consult_status(consult_id)
        return redirect(url_for('Patient_home',id=id))

@app.route('/consult_meeting_info/<id>/<name>',methods=["GET","POST"])
def Consult_meeting_info_doc(id,name):
    if request.method=="GET":
        return render_template('consult_meeting_info_doc.html',id = id,name = name)
    
@app.route('/appointment_meeting_info_doc/<id>/<appointment_id>/<name>',methods=["GET","POST"])
def Appointment_meeting_info_doc(id,appointment_id,name):
    if request.method=="GET":
        obj=Hackaholics()
        out = obj.update_appointment_info_status(appointment_id)
        return render_template('appointment_meeting_info_doc.html',id=id,name = name,appointment_id = appointment_id)

@app.route('/appointment_meeting_info/<id>/<doc_id>',methods=["GET","POST"])
def Appointment_meeting_info(id,doc_id):
    if request.method=="GET":
        return render_template('appointment_meeting_info.html',id=id,doc_id = doc_id)

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
        time = datetime.datetime.now()
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
            'Time':time.strftime("%H:%M:%S"),
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
        out_booking = obj.get_info_appointment(appointment_id)
        booking_date = str(out_booking['BookingDate'])
        msg_to_patient=Message('WE4U Virtual Doctor Appointment',sender='hackaholics4@gmail.com',recipients=[out_booking['PEmail']])
        msg_to_patient.html="<h2>Hello "+out_booking['PName']+",</h2><p>Hope you are doing well!</p><p>We hereby inform you that your Appointment request for the doctor named <b> Dr."+out_booking['DName']+"</b> on <b>"+booking_date+"</b> at <b>"+ out_booking['Time']+"</b> has been <b>Booked Successfully!</b><br><h4>We offer you a sincere thanks and gratitude for choosing our service!</h4><p>If you have any questions or concerns, please don't hesitate to contact us hackaholics4@gmail.com. Thanks</p>"
        mail.send(msg_to_patient)
        return render_template('thankyou_appointment.html',id = id)

@app.route('/cancel_appointment_patient/<id>/<appointment_id>',methods=["GET","POST"])
def Cancel_appointment_patient(id,appointment_id):
    if request.method=="GET":
        obj = Hackaholics()
        out = obj.cancel_appointment(appointment_id)
        return redirect( url_for('Todays_appointment_patient',id = id))
        
@app.route('/thankyou_appointment_completed/<id>/<doc_id>',methods=["GET","POST"])
def Thankyou_appointment_completed(id,doc_id):
    if request.method=="GET":
        return render_template('thankyou_appointment_completed.html',id=id,doc_id = doc_id)

    if request.method == "POST":
        rating = request.form['rating']
        print(rating)
        obj=Hackaholics()
        out = obj.update_doctor_rating(rating,doc_id)
        return redirect( url_for('Patient_home',id = id))


@app.route('/thankyou_consultation/<id>/<doc_id>/<doc_name>/<Patient_name>/<Lang>/<Special>',methods=["GET","POST"])
def Thankyou_consultation(id,doc_id,doc_name,Patient_name,Lang,Special):
    if request.method=="GET":
        return render_template('thankyou_consultation.html',id=id,doc_id =doc_id,doc_name = doc_name,Patient_name = Patient_name,Lang = Lang, Special =Special)

@app.route('/appointment_history/<id>',methods=["POST","GET"])
def History_patient(id):
    obj = Hackaholics()
    out_consult = obj.get_consult_info(id)
    out_booking = obj.get_appointment_info(id)
    return render_template('appointment_history_patient.html',id = id,out_consult = out_consult,out_booking = out_booking)

@app.route('/chat',methods=["GET","POST"])
def Chat():
    if request.method == "GET":
        text = request.args.get('data')
        print(text)
        response = chatbot.get_response(text)
        print(response)
        return response
    else:
        return("Help")

# class Chat(Resource):
#     @cross_origin()
#     def get(self):
#         text = request.args.get('data')
#         print(text)
#         response = chatbot.get_response(text)
#         print(response)
#         return response
#     pass

# api.add_resource(Chat, '/chat')

#Doctor Home Page
@app.route('/DoctorHome/<id>/<name>',methods=["POST","GET"])
def Doctor_Home(id,name):
    h=Hackaholics()
    if request.method=="GET":
        today,no=h.get_todays_appointment(id)
        consult,count=h.get_consultations(id) 
        # if today!=None and no!=0 and consult!=None and count!=0:
        return render_template("Doctor_home.html",id=id,name=name,today=today,no=no,consult=consult,count=count)
        # elif today==None and no==0 and consult==None and count==0:
        #     return render_template("Doctor_home.html",id=id,name=name,no=0,count=0)
        # elif today!=None and no!=0 and consult==None and count==0:
        #     return render_template("Doctor_home.html",id=id,name=name,today=today,no=no,count=0)
        # else:
        #     return render_template("Doctor_home.html",id=id,name=name,no=0,consult=consult,count=count)

# View Patients
@app.route('/Patients/<id>/<name>',methods=["POST","GET"])
def Patients(id,name):
    h=Hackaholics()
    if request.method=="GET":
        res=h.get_patients(id)
        return render_template('Patients.html',id=id,name=name,out=res)

#View Patients Details
@app.route('/Patients_Details/<PId>/<DId>/<name>',methods=["POST","GET"])
def Get_Patient_Details(PId,DId,name):
    h=Hackaholics()
    if request.method=="POST":
        details,diagnostics,appointments=h.get_patient_details(PId,DId)
        res=h.get_patients(DId)
        return render_template('Patients.html',id=DId,name=name,details=details,diagnostics=diagnostics,appointments=appointments,out=res)


@app.route('/Patients_Details_Prescription/<PId>/<DId>/<name>/<bid>',methods=["POST","GET"])
def View_Prescription(PId,DId,name,bid):
    h=Hackaholics()
    if request.method=="GET":
        details,diagnostics,appointments=h.get_patient_details(PId,DId)
        res=h.get_patients(DId)
        prescription=h.get_prescription(bid)
        return render_template('Patients.html',id=DId,name=name,details=details,diagnostics=diagnostics,appointments=appointments,out=res,prescription=prescription)



#Upcoming
@app.route('/Upcoming/<id>/<name>',methods=["POST","GET"])
def Upcoming(id,name):
    h=Hackaholics()
    if request.method=="GET":    
        new=h.get_new_upcoming_details(id)    
        accepted=h.get_accepted_upcoming_details(id) 
        return render_template('Doc_Upcoming.html',id=id,name=name,new=new,accepted=accepted)

#Cancel Appointment
@app.route('/UpdatedUpcoming/<id>/<name>/<bid>',methods=["POST","GET"])
def Cancel_Appointment(id,name,bid):
    h=Hackaholics()
    if request.method=="GET":
        out=h.cancel_appointment(bid)
        you=h.get_cancel_patient_email(bid)
        new=h.get_new_upcoming_details(id)    
        accepted=h.get_accepted_upcoming_details(id) 
        patient=h.get_email_patient(you['PEmail'])
        app=h.get_appointment(bid)
        
        date=str(app['BookingDate'])
        time=str(app['Time'])
        
        msg_to_patient=Message('WE4U Virtual Doctor Appointment',sender='hackaholics4@gmail.com',recipients=[you['PEmail']])
        msg_to_patient.html="<h2>Hello "+patient['Name']+",</h2><p>Hope you are doing well!</p><p>We regret to inform you that your Appointment request for the doctor named <b>"+app['DName']+"</b> on <b>"+date+"</b> at <b>"+ time+"</b> for "+app['Description']+" have been <i>cancelled</i> by him/her due to personal reasons/timing issues.<br><h4>Feel free to reshcedule your Appointment with the same Doctor</h4><p>If you have any questions or concerns, please don't hesitate to contact us hackaholics4@gmail.com Thanks</p>"
        mail.send(msg_to_patient)
        
        return render_template('Doc_Upcoming.html',id=id,name=name,new=new,accepted=accepted)

#Accept Appointment
@app.route('/Updated_Upcoming/<id>/<name>/<bid>',methods=["POST","GET"])
def Accept_Appointment(id,name,bid):
    h=Hackaholics()
    if request.method=="GET":   
        out=h.accept_appointment(bid)   
        new=h.get_new_upcoming_details(id)    
        accepted=h.get_accepted_upcoming_details(id) 
        return render_template('Doc_Upcoming.html',id=id,name=name,new=new,accepted=accepted)


#Profile
@app.route('/Profile/<id>/<name>',methods=["POST","GET"])
def Profile(id,name):
    h=Hackaholics()
    if request.method=="GET":
        out=h.get_info_doctor(id)
        return render_template('Doc_Profile.html',data=out,id=id,name=name)

#Update Profile
@app.route('/UpdateProfile/<id>/<name>',methods=["POST","GET"])
def Update_Profile(id,name):
    h=Hackaholics()
    if request.method=="POST":
        lang=request.form.getlist('language')
        if 'Tamil' in lang:Tamil=1
        else:Tamil=0
        if 'Telugu' in lang:Telugu=1
        else:Telugu=0
        if 'Kannada' in lang:Kannada=1
        else:Kannada=0
        if 'Hindi' in lang:Hindi=1
        else:Hindi=0
        if 'Malayalam' in lang:Malayalam=1
        else:Malayalam=0
        if 'English' in lang:English=1
        else:English=0
        data={
            'Name':request.form["Name"],
            'Degree':request.form["Degree"],
            'State':request.form["State"],
            'District':request.form["District"],
            'Firm':request.form["Firm"],
            'Age':request.form["Age"],
            'Experience':request.form["Experience"],
            'Specialization':request.form["Specialization"],
            'AboutMe':request.form["AboutMe"],
            'Email':request.form["Email"],
            'Password':request.form["Password"],
            'LinkedIn':request.form["LinkedIn"],
            'Facebook':request.form["Facebook"],
            'Tamil':Tamil,
            'Malayalam':Malayalam,
            'Kannada':Kannada,
            'Telugu':Telugu,
            'Hindi':Hindi,
            'English':English,
            'Gender':request.form["Gender"]
        }
        res=h.update_profile_doctor(id,data)
        out=h.get_info_doctor(id)
        return render_template('Doc_Profile.html',data=out,id=id,name=name)

#History
@app.route('/History/<id>/<name>',methods=["POST","GET"])
def History(id,name):
    h=Hackaholics()
    if request.method=="GET":    
        appointment=h.get_history_appointments(id)    
        consult=h.get_history_consultations(id) 
        return render_template('Doc_history.html',id=id,name=name,appointment=appointment,consult=consult)

#Precription
@app.route('/Prescription/<bid>',methods=["POST","GET"])
def Prescription(bid):
    if request.method=="GET":
         return render_template('Doc_Prescription.html',bid = bid)

    if request.method == "POST":
        prescription_id = uuid.uuid4().hex
        obj = Hackaholics()
        out_app = obj.get_info_appointment(bid)
        data={
            'Id': prescription_id,
            'BId':bid,
            'PId':out_app['PId'],
            'DId':out_app['DId'],
            'Medication':request.form['Medication'],
            'Frequency':request.form['Frequency'],
            'Meal':request.form['Meal'],
            'Duration':request.form['Duration']
        }
        out = obj.insert_prescription_info(data)
        out = obj.get_info_appointment(bid)
        out_presc = obj.get_prescription(bid)
        return render_template('Doc_Prescription.html',bid =bid,out = out_presc,id = out['DId'],name = out['DName'])




#Logout
@app.route('/Home')
def Logout():
    session.pop('User_name',None)
    return redirect(url_for('Home'))

#Doctor Register
@app.route('/doctor_register',methods=['POST','GET'])
def Doctor_register():
    if request.method=="GET":
        return render_template('Doctor_register.html')






if(__name__=="__main__"):
    app.run(debug=True)
