window.onload = function(){init()}

subscripts = []

function init()
{
    console.log("Javascript file loaded correctly");

    var appName = navigator.appName;
    var appVersion = navigator.appVersion;
    var userAgent = navigator.userAgent;
    var appCodeName = navigator.appCodeName;
    var page = window.location.href

    $.ajax({
        url: '/pageRequest',
        type: "GET",
        data:
        {
                "appName": appName,
                "appVersion": appVersion,
                "userAgent": userAgent,
                "appCodeName": appCodeName,
                "page": page
        },
        success: function(result)
        {
            return false;
        },
        failure: function()
        {
            //console.log("Not Ajax")
        },
        error: function()
        {
            //console.log("Not Ajax!")
        }
    })

    runSubscript();
}

function runSubscript()
{
    for(var i = 0; i < subscripts.length; ++i)
    {
        subscripts[i]();
    }
}

function registerSubscript(func)
{
    subscripts.push(func);
}

//  TODO:
//
//
//
