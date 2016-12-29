var $ = require ('jquery');
var apiClient = require('./api-client.js');

module.exports = {
    load: function(){
        apiClient.list(function(response){
            $(".list-comments").html(''); //vaciamos el html
            for (var i in response) {
                var commentToGet = response[i];

                var comment_id = commentToGet.id || "";
                var name = commentToGet.name || "";
                var surname = commentToGet.surname || "";
                var email = commentToGet.email || "";
                var comment_text = commentToGet.comment || "";

                var html = '<div class="comment" comment-id="'+ comment_id +'">';
                html += '<div class="comment-text">' + comment_text + '</div>';
                html += '<div class="comment-personal-data">';
                    html += '<div class="comment-name">por ' + name + '</div>';
                    html += '<div class="comment-surname">' + surname + '</div>';
                html += '</div>';
                // html += '<div>' + email + '</div>';
                html += '</div>';
                $('.list-comments').append(html);
            }
        },
        function(response){
            console.error("ERROR", response);
        })
    }
}
