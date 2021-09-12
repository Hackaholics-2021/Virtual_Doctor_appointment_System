from flask import *   
from flask_mail import *
from random import *
app = Flask(__name__) #creating the Flask class object  
app.secret_key="ak"

@app.route('/',methods=["GET"])
def Register():
    if request.method=="GET":
        return render_template('Patient_register.html')
if __name__ == '__main__':
    app.run(debug=True)