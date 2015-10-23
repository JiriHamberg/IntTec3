/*
	Content script that receives coordinates from the extension and checks if there
	are link elements at those coordinates. Should currently only work if the browser
	is full screen, there is no console etc. open and the browser window starts from
	the top left corner of the screen.

	Author: Niko Kortström (niko.kortstrom@helsinki.fi)
*/

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

	var chromePanelHeight = window.outerHeight - window.innerHeight;

	var x = request.gazeX*screen.width;
	var y = request.gazeY*screen.height - chromePanelHeight;

	var elements = document.elementsFromPoint(x, y);

	for (var i = 0; i < elements.length; i++) {
		if (elements[i].nodeName === "A" && elements[i].hasAttribute('href')) {
				sendResponse({previewUrl: elements[i].href});
				break;
		}
	}
});