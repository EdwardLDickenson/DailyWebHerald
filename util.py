from deps import *

def getUsername():
    result = None
    if "username" in session.keys():
        result = session["username"]

    return result

def loggedIn():
    if getUsername():
        return True

    return False

def randomString(length):
    result = ""

    for i in range(length):
        result = result + random.choice(string.ascii_letters)

    return result

#   Too hard to implement without using Regex
def getCleanUrl(dirtyUrl):
    cleanUrl = dirtyUrl
    if dirtyUrl.find("http") != -1:   #   http or https
        cleanUrl = dirtyUrl[dirtyUrl.find("//") + 2:len(dirtyUrl)]

    #cleanUrl = cleanUrl[0:cleanUrl.rfind("/")]

    #   New
    if "www." in cleanUrl:
        cleanUrl = cleanUrl[cleanUrl.find("www.") + 4:]

    #print(cleanUrl[cleanUrl.find("."):])

    return cleanUrl

def getSubscriptions(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT site FROM subscriptions INNER JOIN users ON subscriptions.user = users.id AND name LIKE %s", [username])
    subscriptions = cursor.fetchall()

    cursor.close()
    return subscriptions

def saveArticle(feed, siteNum):
    cursor = mysql.connection.cursor()
    #cursor.execute("INSERT INTO rawFeeds(feed) VALUES(%s)", [feed])
    for j in range(len(feed["entries"])):
        try:
            entry = feed["entries"][j]
            cursor.execute("SELECT * FROM articles WHERE url LIKE %s", [entry["link"]])

            if cursor.fetchone() == None:
                print(entry.keys())

                author = ""
                summary = ""
                content = ""
                title = ""

                link = entry["link"]
                if "title" in entry.keys():
                    #title = unicodedata.normalize("NFKD", entry["title"]).encode("ascii", "replace")
                    title = entry["title"]
                if "author" in entry.keys():
                    #author = unicodedata.normalize("NFKD", entry["author"]).encode("ascii", "replace")
                    author = entry["author"]
                if "content" in entry.keys():
                    #content = unicodedata.normalize("NFKD", entry["content"][0]["value"]).encode("ascii", "replace")
                    content = entry["content"][0]["value"]
                if "summary" in entry.keys():
                    #summary = unicodedata.normalize("NFKD", entry["summary"]).encode("ascii", "replace")
                    summary = entry["summary"]

                    cursor.execute("INSERT INTO articles(url, title, site, content, publisher, summary) VALUES(%s, %s, %s, %s, %s, %s)", [link, title, siteNum, content, author, summary])
        except:
            print("Formatting Error?")
    cursor.execute("UPDATE websites SET updateTime = %s WHERE id LIKE %s", [datetime.now(), siteNum])

    mysql.connection.commit()
    cursor.close()

def getArticlesByUser(username, page=0, pageSize=10):
    if username == None:
        return []

    subData = getSubscriptions(username)
    cursor = mysql.connection.cursor()
    articles = []

    #   This shold be rolled into another application
    cursor.execute("SELECT url, id FROM websites WHERE NOW() - updateTime > 3600")
    websites = cursor.fetchall()

    for i in range(len(websites)):
        feed = feedparser.parse(websites[i]["url"])
        saveArticle(dict(feed), websites[i]["id"])

    #   This is a very complex query
    cursor.execute("SELECT * FROM articles INNER JOIN subscriptions ON\
    articles.site = subscriptions.site INNER JOIN users ON subscriptions.user =\
    users.id WHERE name LIKE %s ORDER BY date DESC LIMIT %s, %s",
    [username, pageSize*page, pageSize])

    articles = (cursor.fetchall())

    mysql.connection.commit()
    cursor.close()
    return articles

    # for i in subData:
    #     cursor.execute("SELECT * FROM websites WHERE id LIKE %s", [i["site"]])
    #     site = cursor.fetchall()[0]
    #     websiteUrl = site["url"]
    #
    #     #   Check for new articles
    #     timediff = datetime.now() - site["updateTime"]
    #     if timediff > timedelta(hours=1):
    #         feed = feedparser.parse(websiteUrl)
    #         saveArticle(dict(feed), str(i["site"]))
    #
    #     #   Serve the articles
    #     cursor.execute("SELECT * FROM articles WHERE site LIKE %s ORDER BY date DESC LIMIT %s, %s", [i["site"], pageSize*page, pageSize])
    #     results = cursor.fetchall()
    #
    #     cursor.execute("SELECT url FROM websites WHERE id LIKE %s", [i["site"]])
    #     sitename = getCleanUrl(cursor.fetchall()[0]["url"])
    #
    #     for j in range(len(results)):
    #         results[j]["sitename"] = sitename
    #         articles.append(results[j])

    #cursor.close()
    #return articles

def getArticleCount(username):
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM articles INNER JOIN subscriptions ON subscriptions.site = articles.site INNER JOIN users ON users.id = subscriptions.user WHERE users.name LIKE %s", [username])
    result = cursor.fetchone()["COUNT(*)"]

    cursor.close()
    return result

def prepareArticle(article):
    result = {}

    result["title"] = article["title"]
    result["date"] = str(article["date"])[0:10]
    result["id"] = article["id"]
    result["summary"] = article["summary"]
    result["content"] = article["summary"]
    result["url"] = article["url"]
    result["views"] = article["views"]

    if article["content"] != "":
        result["content"] = article["content"]

    return result

def prepareArticleList(articles):
    cursor = mysql.connection.cursor()
    prepared = []

    for i in range(len(articles)):
        article = prepareArticle(articles[i])

        cursor.execute("SELECT websites.url FROM websites INNER JOIN articles ON websites.id = articles.site WHERE articles.id LIKE %s", [articles[i]["id"]])
        article["site"] = getCleanUrl(cursor.fetchall()[0]["url"])

        if article["content"] != "":
            article["content"] = articles[i]["content"]

        prepared.append(article)

    cursor.close()
    return prepared


#   TODO:
#
#   Some of the queries can probably be cleaned up with a few inner joins
#
#
#
