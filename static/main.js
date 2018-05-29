window.onload = function(){init()}

function init(){
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
        //url: window.location.href,
        url: '/pageRequest',
        type: "GET",
        data: {
                "appName": appName,
                "appVersion": appVersion,
                "userAgent": userAgent,
                "appCodeName": appCodeName,
                "page": page
        },
        
        success: function(result){
            console.log("Ajax!")
            return false;
        },
        
        failure: function(){
            console.log("Not Ajax")
        },
        
        error: function(){
            console.log("Not Ajax!")
        }
    })
}



//  TODO:
//
//
//


