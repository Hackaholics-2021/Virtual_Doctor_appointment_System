
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

if(__name__=="__main__"):
    app.run(debug = True)

