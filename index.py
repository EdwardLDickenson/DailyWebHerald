from deps import *
from util import *
from forms import *

@app.route('/')
def index():
    print("Index")
    username = getUsername()
    pageSize = 20
    count = getArticleCount(username)
    count = int(count / pageSize)

    if count % pageSize != 0:
        count = count + 1

    articles = getArticlesByUser(username=username, pageSize=pageSize)
    prepared = prepareArticleList(articles)

    return render_template("index.html", username=getUsername(), articles=prepared, pageList=list(range(count)))

@app.route('/<int:page>')
def pagedIndex(page):
    username = getUsername()

    pageSize = 20
    count = getArticleCount(username)
    count = int(count / pageSize)

    if count % pageSize != 0:
        count = count + 1

    articles = getArticlesByUser(username=username, page=page, pageSize=pageSize)
    prepared = prepareArticleList(articles)

    return render_template("index.html", username=getUsername(), articles=prepared, pageList=list(range(count)))


#   TODO:
#
#   The NTSB RSS feed does not work for some reason. Possibly because of the use of special characters
#
#   Intermittent unsubscribe bug 
#
#


