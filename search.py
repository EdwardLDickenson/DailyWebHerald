from deps import *
from util import *
from forms import *

@app.route("/search", methods=["GET", "POST"])
def search():
    searchf = searchForm(request.form)

    username = getUsername()
    return render_template("search.html", username=username, searchf=searchf)
