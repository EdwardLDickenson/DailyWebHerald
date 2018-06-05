function initLoad()
{
    console.log("Login script loaded correctly");

    var reason = $("#main\\.center\\.report\\.reason").text()
    console.log(reason)
}

//  Incl;Included in the other file
registerSubscript(initLoad)
