document.addEventListener('DOMContentLoaded', function () {
	var ws = new WebSocket('ws://localhost:8888')

	ws.onmessage = function (event) {
		msg = JSON.parse(event.data);

		var coordinateData = {
				gazeX: msg.x,
				gazeY: msg.y
	  	};

		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
			
	  		chrome.tabs.sendMessage(tabs[0].id, coordinateData, function(response) {

	    		if (response !== undefined && response.previewUrl !== undefined) {
					document.getElementById('previewFrame').src = response.previewUrl;
				}
	  		});
		});
	}
});