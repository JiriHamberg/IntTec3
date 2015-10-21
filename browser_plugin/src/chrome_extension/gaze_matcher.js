chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

	var elements = document.elementsFromPoint(request.gazeX * window.screen.availWidth, request.gazeY * window.screen.availHeight);

	console.log("FOUND: " + elements);

	for (var i = 0; i < elements.lengh; i++) {

		console.log("ELEMENT: " + elements[i]);

		if (elements[i].nodeName === "A" && elements[i].hasAttribute('href')) {
				sendResponse({previewUrl: elements[i].getAttribute('href')});
				break;
		}
	}
});

// TODO tsekkaa jollain vastaavilla kertolaskuilla konsolista,
// heitä sisää serverii prosentit ja kokeile