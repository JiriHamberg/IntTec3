// TODO coordinates are currently count by using the percentage of whole screen and size of the browsers view, need to move coordinate starting point to browser view starting point

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

	var elements = document.elementsFromPoint(request.gazeX * window.screen.availWidth, request.gazeY * window.screen.availHeight);

	for (var i = 0; i < elements.length; i++) {
		if (elements[i].nodeName === "A" && elements[i].hasAttribute('href')) {
				sendResponse({previewUrl: elements[i].href});
				break;
		}
	}
});