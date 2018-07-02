from deps import *
from util import *
from forms import *

def failedLoginsByTime(username, minutes=5, attempts=5, unit="MINUTE"):
    cursor = mysql.connection.cursor()
    #cursor.execute("SELECT TIMESTAMPDIFF(MINUTE, time, CURRENT_TIMESTAMP) FROM loginAttempts INNER JOIN users ON users.id = loginAttempts.user WHERE users.name LIKE %s ORDER BY loginAttempts.id DESC LIMIT %s", [username, attempts])
    cursor.execute("SELECT COUNT(*) FROM loginAttempts INNER JOIN users ON users.id = loginAttempts.user WHERE users.name LIKE %s AND TIMESTAMPDIFF(MINUTE, time, CURRENT_TIMESTAMP) < %s", [username, attempts])

    results = cursor.fetchone()
    #badAttemptCount = 0

    #for i in range(len(results)):
        #   Unit should go into this query
    #    if results[i]["TIMESTAMPDIFF(" + unit + ", time, CURRENT_TIMESTAMP)"] <= minutes:
    #        badAttemptCount = badAttemptCount + 1

    badAttemptCount = results["COUNT(*)"]

    cursor.close()
    return badAttemptCount >= attempts

def getLastTimestamp(username):
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT time FROM loginAttempts INNER JOIN users ON users.id = loginAttempts.user WHERE users.name LIKE %s ORDER BY time DESC LIMIT 1", [username])
    result = cursor.fetchone()

    cursor.close()

    return result

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
                context["reason"] = "Too many login attempts. Last attempt on: "
                context["timestamp"] = str(getLastTimestamp(username))

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

    #print(context)
    return render_template("login.html", context=context)



#   TODO:
#   Since non-existant user names are not recorded, and IP blocking is not
#   implmented at this time, it is possible to find usernames combinatorially.
#   But the password seems relatively secure at this time.  In the future,
#   it might be a good idea to log the IP along with the login attempt
#
#
