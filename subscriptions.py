from deps import *
from util import *
from forms import *

@app.route("/subscriptions", methods=["POST", "GET"])
def subscriptionsPage():
    form = subscribeForm(request.form)
    websites = []
    
    username = getUsername()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE name LIKE %s", [username])
    userId = cursor.fetchall()[0]["id"]    
    url = form.url.data
    
    if url != None:
        url = url.strip()
    
    unsubs = request.form.getlist("sub")

    for i in range(len(unsubs)):
        #cursor.execute("SELECT id FROM websites WHERE url LIKE %s", ["%" + unsubs[i] + "%"])
        #siteId = cursor.fetchone()["id"]
        #cursor.execute("DELETE FROM subscriptions WHERE user LIKE %s and site LIKE %s", [userId, siteId])
        
        
        mysql.connection.commit()
    
    if url != None:        
        cursor.execute("SELECT COUNT(*) FROM websites WHERE url LIKE %s", [url])
        exists = cursor.fetchall()[0]["COUNT(*)"]
        
        if exists == 0: #   if not exists?
            cursor.execute("INSERT INTO websites(url) VALUES(%s)", [url])
            mysql.connection.commit()
        
        cursor.execute("SELECT * FROM subscriptions INNER JOIN websites ON subscriptions.site = websites.id  INNER JOIN users ON subscriptions.user = users.id WHERE url LIKE %s", [url])
        subscriptions = cursor.fetchall()    #   Fetchall/fetchone?
        
        if len(subscriptions) == 0 and url != "":
            cursor.execute("SELECT id FROM websites WHERE url LIKE %s", [url])
            siteId = cursor.fetchall()[0]["id"]
            cursor.execute("INSERT INTO subscriptions(user, site) VALUES(%s, %s)", [userId, siteId])
            mysql.connection.commit()
    
    cursor.execute("SELECT * FROM websites INNER JOIN subscriptions ON subscriptions.site = websites.id INNER JOIN users ON users.id LIKE subscriptions.user WHERE name LIKE %s", [username])
    results = cursor.fetchall()
    
    for i in range(len(results)):
        websites.append(getCleanUrl(results[i]["url"]))
        
    cursor.close()        
    return render_template("subscriptions.html", username=getUsername(), newForm=form, websites=websites)
