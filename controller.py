from flask import *   
from flask_mail import *
from random import *
import uuid
from model.model import Hackaholics 

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




# Home Page
@app.route('/',methods=["POST","GET"])
def Home():
    if request.method=="GET":
        return render_template('home.html')


# Doctor Register
@app.route('/Register',methods=["POST","GET"])
def SignUp():
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
    h=Hackaholics()
    if request.method=="GET":
        return render_template("Login.html")
    elif request.method=="POST":
        email=request.form["Email"]
        pwd=request.form["Password"]
        doc=h.get_email_doctor(email)
        pat=h.get_email_patient(email)
        if doc:
            if doc["Password"]==pwd:
                return redirect(url_for("Doctor_Home",id=doc["Id"],name=doc["Name"]))
            else:
                flash("Please check Your Password")
                return render_template("Login.html")
        elif pat:
            if pat["Password"]==pwd:
                return render_template("home.html",id=pat["Id"],name=pat["Name"])
            else:
                flash("Please check Your Password")
                return render_template("Login.html")
        else:
            flash("Please Register")
            return render_template("Login.html")

#Doctor Home Page
@app.route('/DoctorHome/<id>/<name>',methods=["POST","GET"])
def Doctor_Home(id,name):
    h=Hackaholics()
    if request.method=="GET":
        today,no=h.get_todays_appointment(id)
        consult,count=h.get_consultations(id) 
        # if today!=None and no!=0 and consult!=None and count!=0:
        #     print('******************',1)
        return render_template("Doctor_home.html",id=id,name=name,today=today,no=no,consult=consult,count=count)
        # elif today==None and no==0 and consult==None and count==0:
        #     print('******************',2)
        #     return render_template("Doctor_home.html",id=id,name=name,no=0,count=0)
        # elif today!=None and no!=0 and consult==None and count==0:
        #     print('******************',3,today)
        #     return render_template("Doctor_home.html",id=id,name=name,today=today,no=no,count=0)
        # elif today==None and no==0 and consult!=None and count!=0:
        #     print('******************',4,today)
        #     return render_template("Doctor_home.html",id=id,name=name,no=0,consult=consult,count=count)
        # else:
        #     print('********************',5)
        #     return render_template("Login.html")

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
        return render_template('Upcoming.html',id=id,name=name,new=new,accepted=accepted)

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
        
        return render_template('Upcoming.html',id=id,name=name,new=new,accepted=accepted)

#Accept Appointment
@app.route('/Updated_Upcoming/<id>/<name>/<bid>',methods=["POST","GET"])
def Accept_Appointment(id,name,bid):
    h=Hackaholics()
    if request.method=="GET":   
        out=h.accept_appointment(bid)   
        new=h.get_new_upcoming_details(id)    
        accepted=h.get_accepted_upcoming_details(id) 
        return render_template('Upcoming.html',id=id,name=name,new=new,accepted=accepted)


#Profile
@app.route('/Profile/<id>/<name>',methods=["POST","GET"])
def Profile(id,name):
    h=Hackaholics()
    if request.method=="GET":
        out=h.get_profile_doctor(id)
        return render_template('Profile.html',data=out,id=id,name=name)

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
        out=h.get_profile_doctor(id)
        return render_template('Profile.html',data=out,id=id,name=name)

#History
@app.route('/History/<id>/<name>',methods=["POST","GET"])
def History(id,name):
    h=Hackaholics()
    if request.method=="GET":    
        appointment=h.get_history_appointments(id)    
        consult=h.get_history_consultations(id) 
        return render_template('History.html',id=id,name=name,appointment=appointment,consult=consult)

#Precription
@app.route('/Prescription',methods=["POST","GET"])
def Prescription():
    if request.method=="GET":
         return render_template('Prescription.html')




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
