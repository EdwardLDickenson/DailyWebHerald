from deps import *
from util import *
from forms import *

@app.errorhandler(404)
def error404(e):
    return render_template("404error.html"), 404

@app.errorhandler(405)
def error405(e):
    return render_template("405error.html"), 405

@app.errorhandler(500)
def error404(e):
    return render_template("500error.html"), 500
