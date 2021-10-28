from flask import *
app=Flask(__name__)

@app.route('/login',methods=["POST","GET"])
def Login():
    if request.method=="GET":
        return render_template("Login.html")

if(__name__=="__main__"):
    app.run(debug=True)