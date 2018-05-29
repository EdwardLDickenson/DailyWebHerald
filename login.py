from deps import *
from util import *
from forms import *

@app.route("/login", methods=["GET", "POST"])
def login():
    if loggedIn():
        return redirect("")
    
    form = loginForm(request.form)
    
    if request.method == "POST":
        username = form.username.data
        passwordAtt = form.password.data
        
        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM users WHERE name = %s", [username])
        if result > 0:
            data = cursor.fetchone()
            password = data["password"]
            
            cur = mysql.connection.cursor()
            cur.execute("SELECT salt FROM users WHERE name like %s", [username])
            salt = cur.fetchall()[0]["salt"]
            
            if password == crypt.crypt(passwordAtt, "$6$" + salt  + "$"):
                session["username"] = username
                return render_template("login.html", username=username)
            
            cur.close()
            
        cursor.close()
        return render_template("login.html", failed=username)
    
    return render_template("login.html", form=form)
