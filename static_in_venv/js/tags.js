function bodyFormatter(body) {
    let tempBody = body.split(' ');
    let mainBody = [];
    for (let i = 0; i < tempBody.length; i++) {
        const element = tempBody[i];
        if (element[0] === '#') {
            mainBody.push(`<a href="">${element}</a>`);
        }
        else {
            mainBody.push(element);
        }
    }
    return mainBody.join(' ');
}

function formatTags() {
	const elements = document.getElementsByClassName('body');
	for (let i = 0; i < elements.length; i++) {
		let bodyText = elements[i].children[0].innerText;

		let words = bodyText
        console.log(words);

        elements[i].innerHTML = bodyFormatter(words)
	}
}

formatTags();