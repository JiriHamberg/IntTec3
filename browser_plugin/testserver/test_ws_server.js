/*
    - start the test server
    - manually load the extension to chrome
    - open extension's popup window
    - extension will get the element at that location and if it contains a link, it is displayed on the extension's popup window
    - coordinates will be sent 10 times with 10sec intervals (scroll down -> a different page should be displayed if there is a link)
*/

var server = require('websocket').server, http = require('http');

var socket = new server({
    httpServer: http.createServer().listen(8888)
});

socket.on('request', function(request) {
    var connection = request.accept(null, request.origin);

    var coordinateObject = {
            x: 0.21,
            y: 0.29
    }
    sendCoordinate(connection, 10, JSON.stringify(coordinateObject));

    connection.on('close', function(connection) {
        console.log('connection closed');
    });
});

function sendCoordinate(connection, times, msg) {
    if (times < 1) {
        return;
    }

    setTimeout(function() {
        connection.send(msg)
        sendCoordinate(connection, times-1, msg);
    }, 10000);
}