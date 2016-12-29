var $ =require('jquery');

module.exports = {
    save: function(likes){
        localStorage.setItem('likes', JSON.stringify(likes));

    },
    getAll: function(){
        var likes = JSON.parse(localStorage.getItem('likes'));
        //¿¿hay que convertirlo a array??
        // var arrayLikes = likes.split(',');
        return likes;
        console.log(typeof likes);
    }

}
