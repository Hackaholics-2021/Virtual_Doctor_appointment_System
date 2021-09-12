from flask import *   
from flask_mail import *
from random import *
# from model.model import First  
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
        return render_template('Doctor_home.html')



if __name__ =='__main__':  
    app.run(debug = True) 