from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from datetime import datetime
import pyrebase

Config = {
  "apiKey": "AIzaSyADtRMxmHOHxShv9VU-MRAyDxv1Us0ftF0",
  "authDomain": "firstpproject-2c172.firebaseapp.com",
  "projectId": "firstpproject-2c172",
  "storageBucket": "firstpproject-2c172.appspot.com",
  "messagingSenderId": "528781920158",
  "appId": "1:528781920158:web:bd4f746d35f0d96451788f",
  "measurementId": "G-0D3CMPHEDJ",
  "databaseURL":"https://firstpproject-2c172-default-rtdb.firebaseio.com/"
};



firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
 
    # trying = {"userid":UID,"userName":"Fatma Azaizah","date":"01-08-2023","story":"my journy in lessan was very exciting, i learned aot of usefull things that helped me alot finding a higher paied job, and in general just meeting new people and developing relationship with israelis"}
    # db.child("Posts").child(UID).set(trying)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = {"email":request.form['email'],
            "password":request.form['password'],
            "full_name":request.form['full_name'],
            "username":request.form['username'],
            "current_image":"static/imgs/barcelona.jpg"
           }

        print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
  
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)    
            UID = login_session['user']['localId']
            # cities = db.child("Cities").get().val().keys()
            # username = db.child("Users").child(UID).child("username").get().val()
            # pic = random.choice(list(db.child("Cities").get().val().keys()))
     
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            print("error")
    return render_template("signup.html",error = "authentication failed")



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""

    if request.method == 'POST':

        try:
            email = request.form['email']
            password = request.form['password']


            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "signin failed"  
    return render_template("signin.html",error = "Authentication failed")


@app.route('/home',methods=['GET','POST'])
def home(): 
    if request.method == 'POST':
        print("post")
        choice = request.form['choice']
        UID = login_session['user']['localId']
        bg = ["static/imgs/2009.jpg","static/imgs/messi1.jpg","static/imgs/team.jpeg","static/imgs/barcelona.jpg","static/imgs/b.jpeg","static/imgs/barcelona2.jpg","static/imgs/barcelona3.jpg"]
        db.child("Users").child(UID).child("current_image").set(bg[int(choice)])
        current = db.child("Users").child(UID).child("current_image").get().val()
        return render_template("home.html",bg = bg,choice = int(choice),current = current)

    try :
        print("try")
        UID = login_session['user']['localId']
        print("pass1")
        current = db.child("Users").child(UID).child("current_image").get().val()
        print("pass2")
        return render_template("home.html",bg = ["static/imgs/2009.jpg","static/imgs/messi1.jpg","static/imgs/team.jpeg","static/imgs/barcelona.jpg","static/imgs/b.jpeg","static/imgs/barcelona2.jpg","static/imgs/barcelona3.jpg"],current = current)

    except :
        print("except")
        return render_template("home.html",bg = ["static/imgs/2009.jpg","static/imgs/messi1.jpg","static/imgs/team.jpeg","static/imgs/barcelona.jpg"],current = "static/imgs/barcelona.jpg")

 # @app.route('/bg')
 # def bg():  

 #     return render_template("home.html",bg = {"url(2009.jpg)","url(messi1.jpg)","url(team.jpeg)","url(barcelona.jpg)"})


@app.route('/messi')
def messi():

    return render_template("messi.html")

@app.route('/about')
def about():

    return render_template("about.html")

@app.route('/survey',methods=['GET','POST'])
def survey():
    error = ""
    if request.method == 'POST':

        Q1 = request.form['Q1']
        Q2 = request.form['Q2']
        Q3 = request.form['Q3']
        Q4 = request.form['Q4']
        Q5 = request.form['Q5']
        try:
            
            # user = {"email":db.child("Users").child("email").get().val(),
            # "password":db.child("Users").child("password").get().val(),
            # "survey":{"Q1":Q1,"Q2":Q2,"Q3":Q3,"Q4":Q4,"Q5":Q5}}
            # db.child("Users").push(user)
            UID = login_session['user']['localId']

            survey = {"Q1":Q1,"Q2":Q2,"Q3":Q3,"Q4":Q4,"Q5":Q5}
            print("YOOOOOOOOO")
            db.child("Users").child(UID).child("survey").set(survey)

        
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("survey.html")


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signup'))


if __name__ == '__main__':
    app.run(debug=True)



# #     if request.method == 'POST':

#         try:
           
#             tweet = {"Title":request.form['Title'],
#             "Text":request.form['Text'],
#             "uid": login_session['user']['localId'],
#             "Timestamp" : dt_string
#             }
#             db.child("Tweets").push(tweet)
#             return redirect(url_for('all_tweets'))
#         except:
#             error = "Authentication failed"
   
#     return render_template("add_tweet.html")