from flask import Flask,render_template,request,session
import pymysql as sql

app = Flask(__name__)
app.secret_key = "adfbhfjeifbfwjncawdhuwefdjnvjsdbvbi"

@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/our-services/")
def ourservices():
    return render_template("ourservices.html")

@app.route("/certifications/")
def certification():
    return render_template("certification.html")

@app.route("/practice/")
def practice():
    return render_template("practice.html")

@app.route("/contact-us/")
def contactus():
    return render_template("contact.html")

@app.route("/signup/")
def signup():
    if session:
        return render_template("afterlogin.html")
    return render_template("signup.html")

@app.route("/login/")
def login():
    if session:
        return render_template("afterlogin.html")
    return render_template("login.html")

@app.route("/after-signup/",methods=["POST","GET"])
def aftersignup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password") 
        cpassword = request.form.get("cpassword")
        if password == cpassword:
            try:
                db = sql.connect(host = "localhost",port = 3306,user = "root",password = "",database = "celebal")
            except:
                error = "connectiviity problem...."
                return render_template("signup.html",error = error)
            else:
                cur = db.cursor()
                cmd = f"select * from userinfo where username = '{username}'"
                cur.execute(cmd)
                data = cur.fetchone()
                if data:
                    error = "user already exist"
                    return render_template("signup.html",error = error)
                else:
                    cmd = f"insert into userinfo values('{username}','{email}','{password}')"
                    cur.execute(cmd)
                    db.commit()
                    return render_template("login.html")
        else:
            error = "password doesn't match"
            return render_template("signup.html",error = error)
    else:
        return render_template("signup.html")

@app.route("/after-login/", methods = ["GET","POST"])
def afterlogin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            db = sql.connect(host = "localhost",port = 3306,user = "root",password = "",database = "celebal")
        except Exception as e:
            return e
        else:
            cmd = f"select * from userinfo where username = '{username}'"
            cur = db.cursor()
            cur.execute(cmd)
            data = cur.fetchall()
            if data:
                if password == data[0][2]:
                    session["username"] = username
                    session["islogin"] = "true"
                    return render_template("afterlogin.html")
                else:
                    error = "Invalid Password!!"
                    return render_template("login.html",error = error)

            else:
                error = "Invalid Username"
                return render_template("login.html",error = error)
            
        return render_template("signup.html") 
  
  

@app.route("/logout/")
def logout():
    keys=dict(session)
    for item in keys.keys():
        session.pop(item)
    return render_template("home.html")


app.run(host="localhost",port=5000,debug =True)

