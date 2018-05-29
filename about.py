from deps import *
from util import *
from forms import *

@app.route("/about")
def about():
    return render_template("about.html", username=getUsername())

