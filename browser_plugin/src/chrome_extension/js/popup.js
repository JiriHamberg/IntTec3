/*
	Receives coordinates from backend and forwards them to content scripts. Content
	scripts respond with some information that is then used to display information
	on the popup window.

	Author: Niko Kortström (niko.kortstrom@helsinki.fi)
*/

document.addEventListener('DOMContentLoaded', function () {
	var ws = new WebSocket('ws://localhost:8888')

	ws.onmessage = function (event) {
		msg = JSON.parse(event.data);

		/*var coordinateData = {
				gazeX: msg.x,
				gazeY: msg.y
	  	};*/
	  	//using the format specified in the xml_parser.py
	  	var coordinateData = {
	  		gazeX: msg.fixation.x,
	  		gazeY: msg.fixation.y
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