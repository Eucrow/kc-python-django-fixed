var $ =require('jquery');

//adaptado de: https://codepen.io/g13nn/pen/eHGEF

$( ".close" ).hide();

// $( ".menu" ).hide();

$( ".open" ).click(function() {
    $( ".menu" ).slideToggle( "150", function() {
        $( ".open" ).hide();
        $( ".close" ).show();
        });
});

$( ".close" ).click(function() {
    $( ".menu" ).slideToggle( "250", function() {
        $( ".close" ).hide();
        $( ".open" ).show();
        $( ".menu" ).removeAttr("style");
    });
});

// esto parece una chapucilla:
// $( window ).resize(function() {
//     if ($("window").width>736){
//         $( ".menu" ).removeAttr("style");
//     }
//
// });
