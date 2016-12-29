/**
 * Created by MarcoAntonio on 21/10/2016.
 */
var $ = require ('jquery');

var moment = require('moment');


// function to convert to YYYY-MM-DD format if it is in DD-MM-YYYY format
function convert_date(date){
    if (moment(date, "DD-MM-YYYY").isValid()){
        var momentDate = moment(date, "DD-MM-YYYY");
        correct_date = momentDate.format("YYYY-MM-DD");
        return (correct_date);
    } else if (moment(date, "YYYY-MM-DD").isValid()){
        //alert (date);
        return (moment(date, "YYYY-MM-DD"));
    } else {
        return ("ERROR");
    }
}

//event listener al botón de enviar formulario
$('.new-post-form').on("submit", function(){
    var inputs = $('.new-post-form').find("input, textarea, select");

    for (var i= 0; i<inputs.length; i++){
        var input = inputs[i];
        if (input.checkValidity() == false){
            alert(input.validationMessage);
            input.focus();
            return false;
        }
    }

    // validate date
    var dateField = $('#publication_date');
    correct_date = convert_date(dateField.val());
    if (correct_date == "ERROR") {
        //no se por qué la siguiente línea no funciona:
        //date_field.setCustomValidity("fecha incorrecta");
        alert ("fecha incorrecta");
        dateField.focus();
        return false;

    } else {
        //alert("fecha correcta:" + correct_date);
        document.getElementById('publication_date').value = correct_date;
    }
})
