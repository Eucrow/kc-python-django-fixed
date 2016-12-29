var $ = require('jquery');

var apiClientLikes = require('./api-client-likes.js');

// var likes = [];
var likes = apiClientLikes.getAll();
// console.log(likes);
 // console.log(typeof(likes));

function heartLike(idToChange){
    var imageToChange = $(".container-article").find("[data-id='" + idToChange + "']");
    imageToChange.removeClass("icon-heart");
    imageToChange.addClass("icon-heart-blue");
}

function heartDislike(idToChange){
    var imageToChange = $(".container-article").find("[data-id='" + idToChange + "']");
    imageToChange.removeClass("icon-heart-blue");
    imageToChange.addClass("icon-heart");
}

$( document ).ready(function() {
    for (like in likes){
        // console.log(likes[like]);
        idToChange = likes[like];

        // imageToChange.toggleClass("icon-hearth-white", "icon-hearth");
        heartLike(idToChange);
        // imageToChange.removeClass("icon-heart");
        // imageToChange.addClass("icon-heart-white");
        // console.log($(imageToChange));
    }
});


// $( document ).ready(function() {
//
//     console.log(localStorage.getItem());
//     //
//     // articles =$(".container-article");
//     // // console.log(articles);
//     // for (i=0; i<articles.length; i++){
//     //     // console.log(articles[i].id);
//     //     var key = articles[i].id;
//     //     existLike = apiClientLikes.exist(key);
//     //     if (existLike == "like") {
//     //         console.log($("articles[i] .icon-heart"));
//     //         $("articles[i] .icon-heart").html('hulap');
//     //     }
//     //
//     // }
// });

// $(".article-social-likes").on("click", function(){
//     var articleId = $(this).data("id");
//     apiClientLikes.save(articleId, "like");
// });

$(".article-social-likes").on("click", function(){
    var articleId = $(this).data("id");
    if (likes == null){
        likes= [articleId];
        heartLike(articleId);
    } else {
        var index = likes.indexOf(articleId);
            if (index == -1){
                likes.push($(this).data("id"));
                heartLike(articleId);
            } else {
                likes.splice(index, 1);
                heartDislike(articleId);
            }
    }
    apiClientLikes.save(likes);
});
