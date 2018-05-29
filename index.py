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

    return render_template("index.html", username=getUsername(), articles=prepared, pageList=list(range(count)), searchf=searchForm(request.form))

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

# def prepareArticleList(articles):
#     cursor = mysql.connection.cursor()
#     prepared = []
#
#     for i in range(len(articles)):
#         article = {}
#
#         cursor.execute("SELECT websites.url FROM websites INNER JOIN articles ON websites.id = articles.site WHERE articles.id LIKE %s", [articles[i]["id"]])
#         article["site"] = getCleanUrl(cursor.fetchall()[0]["url"])
#         article["title"] = articles[i]["title"]
#         article["date"] = articles[i]["date"]
#         article["id"] = articles[i]["id"]
#         article["summary"] = articles[i]["summary"]
#         article["content"] = articles[i]["summary"]
#
#         if article["content"] != "":
#             print(article["content"])
#             article["content"] = articles[i]["content"]
#
#         prepared.append(article)
#
#     cursor.close()
#     return prepared

@app.errorhandler(404)
def error404(e):
    return render_template("404error.html"), 404

@app.errorhandler(500)
def error404(e):
    return render_template("500error.html"), 500

#   Add 405
