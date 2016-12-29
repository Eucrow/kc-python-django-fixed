var $ = require ('jquery');
var apiClient       = require('./api-client.js');
var commentsList    = require('./comments-list.js');


var newCommentFormButton = $('.new-comment-form button')
var inputs = $(".new-comment-form").find("input, textarea");

function setLoading(){ // antes de enviar, pero despues de dar un click al botón
    $(inputs).attr("disabled", true);// desabilito todos los imputs
    newCommentFormButton.text("Grabando comentario...").attr("disabled", true); // sobre un mismo objeto, se ejecuta un método.
                                                                    // cambio el texto del botón y lo desabilito
}
function unsetLoading(){ //se ejecuta cuando la petición acaba, haya acabado bien o mal
    $(inputs).attr("disabled", false);// habilito todos los imputs
    newCommentFormButton.text("Envía tu comentario").attr("disabled", false);
}

//event listener al botón de enviar formulario
$('.new-comment-form').on("submit", function(){

    var inputs = $(".new-comment-form").find("input, textarea");
    for (var i= 0; i<inputs.length; i++){
        var input = inputs[i];
        if (input.checkValidity() == false){
            alert(input.validationMessage);
            input.focus();
            return false;
        }
    }

    var inputTextarea = $('textarea');
    if (inputTextarea.val().split(' ').length > 120){
            alert("Máximo 120 palabras en el mensaje");
            textareaComment.focus();
            return false;
    }

    //comentario que quiero añadir
    var commentToAdd = {
        name: $("#name").val(), // = document.getElementById("name").value
        surname: $("#surname").val(),
        email: $("#email").val(),
        comment: $("#comment").val()
    };

    setLoading(); // desabilito el formulario

    apiClient.save(
        commentToAdd,
        function(response) { //función que se ejecuta cuando la petición sea válida
            console.log($("form")[0]);
                $("#add-new-comment")[0].reset(); // borra todos los campos de formulario
                                        // como jquery devuelve un array al pedir el form, hay que acceder a él con el [0]
                $("#name").focus(); // pone el foco en el campo name
                commentsList.load();
                unsetLoading();
        },
        function() {
            console.error("ERROR", arguments);
            unsetLoading();
        }
        )

    return false; // == e.preventDefault(); en jquery
});
