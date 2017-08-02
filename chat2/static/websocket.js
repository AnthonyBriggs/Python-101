function start(ws_url, username) {
    ws = new WebSocket(ws_url);
    
    // js/regexp considers @ to not be a word boundary,
    // so only check the trailing one
    var my_username = new RegExp("@"+username+"\\b", "gi");
    
    ws.onmessage = function(evt) {
        // see if we're mentioned...
        if (evt.data.match(my_username)) {
            // document.getElementById("notify").play();
            
            // playing sound seems to kill the ws event loop (in chrome),
            // so push out to another function
            setTimeout(function() { notify(); }, 100);
        }
        
        var para = document.createElement("p");
        messageBody = document.getElementById("messages");
        messageBody.insertBefore(para, null);
        
        /* Chrome (and others?) do not like setting outerHTML without a parent */
        para.outerHTML = evt.data;
    };
    
    ws.onclose = function() {
        //try to reconnect in 2 seconds
        setTimeout(function() { start(ws_url); }, 2000);
    };
}

function notify() {
    document.getElementById("notify").play();
}

function sendMessage(msg_text) {
    if (ws.readyState == 1) {
        ws.send(msg_text);
    } else {
        // ws is restarting - try in a couple of seconds
        setTimeout(function() { sendMessage(msg_text); }, 2500);
    }
    return false;
}
