chrome.runtime.onConnect.addListener(function (port) {
	port.onMessage.addListener(function (msg) {
		if (msg !== undefined) {
			
		} else {
			// TODO ERROR HANDLING
		}
	});
});