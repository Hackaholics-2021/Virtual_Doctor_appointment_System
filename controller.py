from flask import *

app=Flask(__name__)

# Patient_home
@app.route("/",methods=["GET","POST"])
def Patient_home():
    return render_template("Patient_home.html")


if(__name__=="__main__"):
    app.run(debug = True)