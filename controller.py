from flask import *   
from flask_mail import *
from random import *
import uuid
from model.model import Hackaholics  
app = Flask(__name__) #creating the Flask class object  
app.secret_key="div"

email_addresses=[]

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
                return render_template("Doctor_home.html",id=doc["Id"],name=doc["Name"])
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

# Return to Doctor Home Page
@app.route('/DoctorHome/<id>/<name>',methods=["POST","GET"])
def Doctor_Home(id,name):
    if request.method=="GET":
        return render_template("Doctor_home.html",id=id,name=name)


# View Patients
@app.route('/Patients/<id>/<name>',methods=["POST","GET"])
def Patients(id,name):
    h=Hackaholics()
    if request.method=="GET":
        res=h.get_patients(id)
        return render_template('Patients.html',id=id,name=name,out=res)

@app.route('/Patients_Details/<PId>/<DId>/<name>',methods=["POST","GET"])
def Get_Patient_Details(PId,DId,name):
    h=Hackaholics()
    if request.method=="POST":
        details,diagnostics,appointments=h.get_patient_details(PId,DId)
        res=h.get_patients(DId)
        return render_template('Patients.html',id=DId,name=name,details=details,diagnostics=diagnostics,appointments=appointments,out=res)

@app.route('/Profile/<id>/<name>',methods=["POST","GET"])
def Profile(id,name):
    h=Hackaholics()
    if request.method=="GET":
        out=h.get_profile_doctor(id)
        return render_template('Profile.html',data=out,id=id,name=name)

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

@app.route('/Logout')
def Logout():
    session.pop('User_name',None)
    return redirect(url_for('home.html'))

@app.route('/doctor_register',methods=['POST','GET'])
def Doctor_register():
    if request.method=="GET":
        return render_template('Doctor_register.html')







if(__name__=="__main__"):
    app.run(debug=True)
