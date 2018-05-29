from deps import *
from util import *
from forms import *

@app.route("/logout", methods=["GET", "POST"])
#   Decorators are probably better for this, but eh
def logout():
    if not loggedIn():
        return redirect("login")
    
    if request.method == "POST":
        session.clear()
    
    username = getUsername()
    
    return render_template("logout.html", username=username)
