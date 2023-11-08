from flask import (Flask, request, session, 
    send_file, render_template, send_from_directory, 
    abort, redirect)
import hashlib
import datetime
import db
import finder

def genSession(username):
    sessionid = hashlib.sha256( (username+str(datetime.datetime.now())).encode() ).hexdigest()
    return sessionid

app = Flask(__name__)
app.secret_key = "spartans"

DB = db.MainDatabase()

@app.route("/")
def index():
    username = "-1"
    if "id" in session:
        username = DB.loadSession(session["id"])
    return render_template("index.html", username = username)


@app.route("/static/<path:path>")
def _static(path):
    try:
        return send_file("/static/"+path)
    except:
        return abort(404)
    

@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if DB.usernameTaken(username):
            return render_template("signin.html", msg = "Username Already Taken!")

        sid = genSession(username)
        session["id"] = sid
        
        id = DB.addUser(username, password, sid)
        DB.saveSession(username, sid)
        return redirect("/")
    
    return render_template("signin.html", msg=None)

@app.route("/login", methods=["POST", "GET"])
def loginin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not DB.usernameTaken(username):
            return render_template("login.html", msg=None)

        id = DB.getUser(username)[0]
        
        if not DB.matchPassword(username, password):
            return render_template("login.html", msg="Wrong Password!")
        
        sid = genSession(username)
        DB.saveSession(username, sid)
        session["id"] = sid
        return redirect("/")
    
    return render_template("login.html", msg=None)


@app.route("/finder", methods = ["POST", "GET"])
def _finder():
    if "id" not in session:
        return  redirect("/login")
    if request.method == "POST":
        email = request.form.get("email")
        sid = session["id"]
        username = DB.loadSession(sid)
        if username == "":
            return "Invalid Session"
        
        res = finder.findEmailContacts(sid, email)
        return render_template("finder.html", res = res, email = email, msg = None)

    return render_template("finder.html", res = None, email = None, msg = None)

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()