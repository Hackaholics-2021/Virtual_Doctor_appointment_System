
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

@app.route('/login',methods=["GET"])
def Login():
    if request.method=="GET":
        return render_template('Patient_login.html')

@app.route('/doc_reg',methods=["GET"])
def Doc_Register():
    if request.method=="GET":
        return render_template('Doctor_register.html')

@app.route('/doc_log',methods=["GET"])
def Doc_Login():
    if request.method=="GET":
        return render_template('Doctor_login.html')

if __name__ == '__main__':
    app.run(debug=True)
