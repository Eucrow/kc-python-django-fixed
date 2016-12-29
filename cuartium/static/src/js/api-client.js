var $ =require('jquery');

module.exports = {
    save: function(commentToAdd, successCallback, errorCallback){ //acepta 3 param: el
        // comentario que quiero guardar, 2 una función que se va a ejecutar
        // cuando se guarde correctamente la canción y 3 una fucnión que se va a
        // ejecutar cuando algo falle al guardar la canción

        var formData = new FormData();
        formData.append("name", commentToAdd.name);
        formData.append("surname", commentToAdd.surname);
        formData.append("email", commentToAdd.email);
        formData.append("comment", commentToAdd.comment);
// console.log(formData);
        $.ajax({
            url:"/api/comments/", //url donde vamos a hacer la peticion (donde va a guardar los datos)
            method: "post", // método post porque queremos crear un comentario
            data: formData,
            processData: false, //para enviarlo por ajax, esto no se que es
            contentType: false, //para enviarlo por ajax, esto no se que es
            success: successCallback,
            error: errorCallback
        });
    },

    list: function(successCallback, errorCallback){
        $.ajax({
            url:"/api/comments/", //url donde vamos a hacer la peticion (donde va a guardar los datos)
            method: "get", 
            success: successCallback,
            error: errorCallback
        });
    },
}
