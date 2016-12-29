var $ = require ('jquery');

var commentsList    = require('./comments-list.js');
var apiClient       = require('./api-client.js');

module.exports = {
    load: function(){
        $(document).ready(function() {
            $(window).scroll(function() {
                if ($('body').height() <= ($(window).height() + $(window).scrollTop())) {
                    if (!$.trim($(".list-comments").html())){ //$.trim elimina caracteres en blanco y saltos de línea
                        // cargamos la lista de comentarios
                        commentsList.load();
                        // y mostramos el formulario que se mantenía oculto
                        $(".new-comment-form").css("display", "block");
                    }
                }
            });
        });
    },
    count: function(){
        apiClient.list(function(response){
            if (response == 0){
                var html = "No comments yet";
            } else {
                var html = response.length + " comentarios";
            }

            $(".number-of-comments").append(html);
        },
        function(response){
            console.error("ERROR", response);
        })
    }
}
