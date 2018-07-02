function getCount(seconds, timestamp)
{
    var startSeconds = Math.trunc(timestamp.getTime() / 1000);
    var minuteCounter = 0;
    var secondCounter = 0;

    var current = new Date();
    var now = Math.trunc(current.getTime() / 1000);

    $("#main\\.center\\.login\\.username").focus();

    if(startSeconds + seconds - now <= 0)
    {
        $("#main\\.center\\.report\\.timestamp").text("You may login now");

        return 1;
    }

    secondCounter = (startSeconds + seconds - now) % 60;
    minuteCounter = Math.trunc(((startSeconds + seconds - now) / 60));

    //console.log(minuteCounter + " Minutes and " + secondCounter + " Seconds");
    $("#main\\.center\\.report\\.timestamp").text(minuteCounter + "m and " + secondCounter + "s Remaining");
    secondCounter = now - startSeconds;

    return 0;
}

function countDown(seconds, timestamp)
{
    var startSeconds = Math.trunc(timestamp.getTime() / 1000);
    var minuteCounter = 0;
    var secondCounter = 0;

    getCount(seconds, timestamp)
    setInterval(function()
    {
        if(getCount(seconds, timestamp) == 1)
        {
            clearInterval();
        }
    }, 1000)
}

function initLoad()
{
    console.log("Login script loaded correctly");

    var timestampStr = $("#main\\.center\\.report\\.timestamp").text();

    if(timestampStr != "")
    {
        //  This is unfortunately very closely tied to the format of the datetime timestamp from the server
        var timestamp = timestampStr.substring(timestampStr.indexOf("(") + 1, timestampStr.indexOf(")"));
        var tmp = timestamp;
        var year = tmp.substring(0, tmp.indexOf(","));
        tmp = tmp.substring(tmp.indexOf(",") + 1, tmp.length);
        var month = tmp.substring(0, tmp.indexOf(","));
        tmp = tmp.substring(tmp.indexOf(",") + 1, tmp.length);
        var day = tmp.substring(0, tmp.indexOf(","));
        tmp = tmp.substring(tmp.indexOf(",") + 1, tmp.length);
        var hour = tmp.substring(0, tmp.indexOf(","));
        tmp = tmp.substring(tmp.indexOf(",") + 1, tmp.length);
        var minute = tmp.substring(0, tmp.indexOf(","));
        tmp = tmp.substring(tmp.indexOf(",") + 1, tmp.length);
        var second = tmp;
        var lastLogin = new Date(year, month - 1, day, hour, minute, second);   //  Python datetime does not seem to be zero index when accessing the month.

        $("#main\\.center\\.report\\.timestamp").text("5m and 0s Remaining");

        var seconds = 60 * 5;

        countDown(seconds, lastLogin);
    }
}

//  This function must be included in the main.js file
registerSubscript(initLoad)



//  TODO:
//
//
//
