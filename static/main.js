window.onload = function(){init()}

subscripts = []

function init()
{
    console.log("Javascript file loaded correctly");
    console.log(navigator.appName);
    console.log(navigator.appVersion);
    console.log(navigator.userAgent);
    console.log(navigator.appCodeName);

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
            console.log("Ajax!")
            return false;
        },
        failure: function()
        {
            console.log("Not Ajax")
        },
        error: function()
        {
            console.log("Not Ajax!")
        }
    })

    runSubscript();
}

function runSubscript()
{
    console.log("Run Subscripts")
    for(var i = 0; i < subscripts.length; ++i)
    {
        console.log("Script found")
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
