from deps import *
from util import *
from forms import *

def failedLoginsByTime(username, minutes=5, attempts=5, unit="MINUTE"):
    cursor = mysql.connection.cursor()
    #   Unit should go into this query
    cursor.execute("SELECT TIMESTAMPDIFF(MINUTE, time, CURRENT_TIMESTAMP) FROM loginAttempts INNER JOIN users ON users.id = loginAttempts.user WHERE users.name LIKE %s ORDER BY loginAttempts.id DESC LIMIT %s", [username, attempts])

    results = cursor.fetchall()
    badAttemptCount = 0

    for i in range(len(results)):
        #   Unit should go into this query
        if results[i]["TIMESTAMPDIFF(MINUTE, time, CURRENT_TIMESTAMP)"] <= minutes:
            badAttemptCount = badAttemptCount + 1

    cursor.close()
    return badAttemptCount >= attempts

def getLastTimestamp():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT loginAttempts.id, time FROM loginAttempts INNER JOIN users ON users.id = loginAttempts.user ORDER BY time DESC LIMIT 1")


    cursor.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm(request.form)
    context = {"form": form}
    cursor = mysql.connection.cursor()

    #   Some of these conditions probably can be collapsed or delegated
    if request.method == "POST":
        username = form.username.data
        passwordAtt = form.password.data
        result = cursor.execute("SELECT * FROM users WHERE name = %s", [username])

        if result > 0:
            data = cursor.fetchone()
            password = data["password"]
            salt = data["salt"]

            #   I'm not certain if comparing to an integer or
            if failedLoginsByTime(username):
                context["failed"] = username
                context["reason"] = "Too many login attempts"
                context["timestamp"] = ""

            elif password == crypt.crypt(passwordAtt, "$6$" + salt  + "$"):
                setSessionUsername(username)
                context["success"] = username

            else:
                cursor.execute("INSERT INTO loginAttempts(user) VALUES(%s)", [data["id"]])
                context["failed"] = username
                context["reason"] = "Bad username or password"


    mysql.connection.commit()
    cursor.close()

    #   Having a "result" variable might be better than having the two returns
    if "success" in context.keys() or loggedIn():
        return redirect("")

    return render_template("login.html", context=context)



#   TODO:
#   Since non-existant user names are not recorded, and IP blocking is not
#   implmented at this time, it is possible to find usernames combinatorially.
#   But the password seems relatively secure at this time.  In the future,
#   it might be a good idea to log the IP along with the login attempt
#
#
