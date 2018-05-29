from deps import *
from util import *
from forms import *

@app.route("/contact", methods=["POST", "GET"])
def contact():

    if request.method == "POST":
        cursor = mysql.connection.cursor()
        respond = False
        if len(request.form.getlist("respond")) == 1:
            respond = True

        form = contactForm(request.form)
        cursor.execute("INSERT INTO contactMessages(message, email, sender, subject, respond) VALUES(%s, %s, %s, %s, %s)", [form.message.data, form.email.data, form.sender.data, form.subject.data, respond])
        mysql.connection.commit()

        cursor.close()

    form = contactForm()
    searchf = searchForm(request.form)
    return render_template("contact.html", username=getUsername(), form=form, searchf=searchf)
