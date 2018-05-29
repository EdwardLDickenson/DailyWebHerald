from deps import *
from util import *
from forms import *

@app.route("/article/")
def defaultArticle():
    return render_template("defaultArticle.html")

@app.route("/article/<int:num>")
def article(num):

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM articles WHERE id LIKE %s", [num])
    article = cursor.fetchall()[0]
    article = prepareArticle(article)

    cursor.execute("UPDATE articles SET views = views + 1 WHERE id LIKE %s", [num])
    mysql.connection.commit()

    searchf = searchForm(request.form)
    cursor.close()
    return render_template("article.html", num=num, username=getUsername(), article=article, site=getCleanUrl(article["url"]), searchf=searchf)
