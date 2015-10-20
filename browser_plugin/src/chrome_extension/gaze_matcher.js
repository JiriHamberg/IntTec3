chrome.runtime.onConnect.addListener(function (port) {

	port.onMessage.addListener(function (msg) {
		if (msg.gazeX !== undefined && msg.gazeY !== undefined) {
			var elem = document.elementFromPoint(msg.gazeX * window.screen.availHeight, msg.gazeY * window.screen.availHeight);
			if (elem.nodeName === "A" && elem.hasAttribute('href')) {
				
				chrome.runtime.sendMessage({previewUrl: elem.getAttribute('href')});
			}
		} else {
			// TODO ERROR HANDLING
		}
	});
});