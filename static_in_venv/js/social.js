function commentReplyToggle(parent_id) {

    const row = document.querySelector(parent_id);

    if (row.classList.contains('d-none')) {
        row.classList.remove('d-none');
    } 
    else {
        row.classList.add('d-none');
    }

}

function rePostToggle(parent_id) {

    const row = document.querySelector(parent_id);

    if (row.classList.contains('d-none')) {
        row.classList.remove('d-none');
    } 
    else {
        row.classList.add('d-none');
    }

}

console.log("Hi");
console.log("Hi");