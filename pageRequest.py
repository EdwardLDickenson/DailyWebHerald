from deps import *
from util import *
from forms import *

@app.route("/pageRequest", methods=["POST", "GET"])
def pageRequest():
    appName = request.args.get("appName")
    appVersion =request.args.get("appVersion")
    userAgent = request.args.get("userAgent")
    appCodeName = request.args.get("appCodeName")
    pageUrl = request.args.get("page")
    
    ip = request.environ["REMOTE_ADDR"]
    environ = request.environ
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO pageRequests(page, ip, environ, appName, appVersion, userAgent, appCodeName) VALUES(%s, %s, %s, %s, %s, %s, %s)", [pageUrl, ip, environ, appName, appVersion, userAgent, appCodeName])
    cursor.connection.commit()
    cursor.close()
    
    return jsonify({"result": "Success"})
