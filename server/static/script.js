btn = document.getElementById('gen_btn');
let book_title = document.getElementById('book_title');
let book_genres = document.getElementById('book_genres');
let book_rating = document.getElementById('book_rating');
let book_plot = document.getElementById('book_plot');
let cover = document.getElementById('cover');

let current = 0;

btn.onclick = async function() {

    fetch("http://localhost:80/").then((Response) => {
        return Response.json()
    }).then((data) => {
        current = data["book_id"]
        book_title.textContent = data["title"];
        book_genres.textContent = data["genres"];
        book_rating.textContent = data["rating"];
        book_plot.textContent = data["plot"];
        cover.src = data['cover'];
    });
};


let add = document.getElementById('add');

add.onclick = async function(){

    fetch("http://localhost:3001/?id=" + current.toString(), {
    method: "POST"
    })
    .then((response) => response.json())
    .then((json) => console.log(json));
};