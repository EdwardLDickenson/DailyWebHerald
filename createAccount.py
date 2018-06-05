from deps import *
from util import *
from forms import *

@app.route("/create", methods=["GET", "POST"])
def createAccount():
    form = registerForm(request.form)
    
    if loggedIn():
        return redirect(url_for("logout"))
    
    if request.method == "POST" and form.validate():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        salt = randomString(64)
        safePassword = crypt.crypt(password, "$6$" + salt  + "$")
        
        cursor = mysql.connection.cursor()
        exists = cursor.execute("SELECT * FROM users WHERE name = %s", [name])
        
        if exists < 1:
            cursor.execute("INSERT INTO users(name, email, password, salt) VALUES(%s, %s, %s, %s)", (name, email, safePassword, salt))
            mysql.connection.commit()
            setSessionUsername(name)
            
        else:
            cursor.close()
            error="Sorry, that username was taken"
            return render_template("create.html", error=error)
            
        cursor.close()
        return render_template("create.html", success=name)

    return render_template("create.html", form=form)
