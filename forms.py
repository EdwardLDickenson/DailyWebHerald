from deps import *

#   Bad naming of this class
class registerForm(Form):
    username = StringField("Name", [validators.Length(min=1, max=256)])
    password = PasswordField("Password", [validators.Length(min=6, max=64), validators.DataRequired(), validators.EqualTo("confirm", "Passwords must match")])
    confirm = PasswordField("Comfirm Password")
    email = StringField("Email", [validators.Length(min=6, max=128), validators.Optional()])

class smallSearchForm(Form):
    searchStr = StringField("Str", [validators.Length(min=1, max=128)])

class searchForm(Form):
    searchStr = StringField("Str", [validators.Length(min=1), validators.Optional()])
    publishDate = DateField("Date", [validators.Optional()])
    startDate = DateField("Date", [validators.Optional()])
    endDate = DateField("Date", [validators.Optional()])
    views = IntegerField("Views", [validators.Optional()])
    maxViews = IntegerField("Views", [validators.Optional()])
    minViews = IntegerField("Views", [validators.Optional()])
    publisher = StringField("Publisher", [validators.Optional()])
    website = StringField("Site", [validators.Optional()])
    title = StringField("Title", [validators.Optional()])

class subscribeForm(Form):
    url = StringField("Url", [validators.Optional()])

class loginForm(Form):
    username = StringField("Name", [validators.Length(min=1, max=256)])
    password = PasswordField("Password", [validators.Length(min=6, max=64), validators.DataRequired(), validators.EqualTo("confirm", "Passwords must match")])

class contactForm(Form):
    message = TextAreaField("Message", [validators.Length(min=4), validators.Required()])
    email = EmailField("Email", [validators.Length(min=1), validators.Required()])
    sender = StringField("Sender", [validators.Length(min=1), validators.Required()])
    subject = StringField("Subject", [validators.Length(min=1)])
