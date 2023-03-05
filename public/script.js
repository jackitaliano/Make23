function addHeader(){
    var div = document.getElementById("note-area");
    var candidate = document.getElementById("header-candidate");
    if (candidate.value.length != 0){
        var header = document.createElement("h3");
        var ul = document.createElement("ul");

        header.setAttribute('id', candidate.value);
        ul.setAttribute('id', "sublist-" + candidate.value);

        header.innerHTML = candidate.value;
        div.appendChild(header);
        div.appendChild(ul);
    }
}

function addSubHeader(){
    var sublistCandidate = document.getElementById("header-candidate")
    var contentCandidate = document.getElementById("sublist-candidate");
    if (contentCandidate.value.length != 0){
        var li = document.createElement("li");
        var ul = document.getElementById("sublist-" + sublistCandidate.value);

        li.setAttribute('id', contentCandidate.value);
        li.innerHTML = contentCandidate.value;
        ul.appendChild(li);
    }
}

function addImageToRow(){
}