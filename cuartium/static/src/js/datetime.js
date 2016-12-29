var $ = require ('jquery');

// SEGUNDO INTENTO
var moment = require('moment');
moment().format();

//moment.locale('cs'); //no funciona por un bug: http://momentjs.com/docs/#/use-it/browserify/
require('moment/locale/es');    // con esto si funciona

// Round relative time evaluation down
moment.relativeTimeRounding(Math.floor);

// cambio de configuración del redondeo a minutos
moment.relativeTimeThreshold('s', 60);
// cambio de configuración del redondeo a horas
moment.relativeTimeThreshold('m', 60);

//cambiar la forma en la que muestra los segundos (por defecto no indica el número de segundos)
moment.updateLocale('es', {
    relativeTime : {s: "%d segundos"}
});

//cambiar la forma en que representa el am y el pm
moment.updateLocale('es', {
  meridiem: function(hour, minute, isLowerCase) {
    if (hour < 12) {
      return 'a.m.';
    } else {
      return 'p.m.';
    }
  }
});

moment.updateLocale('es', {
    monthsShort : [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"
    ]
});

(function datetime(){
    var times =  $(".article-social-fecha").find("time");
    for (var i=0; i<times.length; i++) {
        time = $(times[i]);
        refresh(time);
    }

    function refresh(time){
        // publicationTime = moment($(time).attr("datetime"), "YYYY-MM-DD HH:mm:ss");
        publicationTime = moment($(time).attr("datetime"), "MMM. D, YYYY, h:mm a ");
        console.log(publicationTime);
        nowTime = moment();
        timeToNow = nowTime.diff(publicationTime, 'seconds'); // tiempo que hay
        // entre que se publica el artículo hasta el momento en que se refresca la pantalla

        // Función para actualizar y refrescar el tiempo transcurrido
        // Sólo vale para algunos casos... :(
        function updateAndRefresh(timeToRefresh){
            $(time).text(publicationTime.fromNow());
            setTimeout(datetime, timeToRefresh);
        }

        // According to the time elapsed from the publication of the article
        if (timeToNow < 60){ // less than a minute
            updateAndRefresh(1000); // refresh every second
        } else if (timeToNow < (60*60)) { // less than a hour
            updateAndRefresh(60000); // refresh every minute
        } else if (timeToNow < (60*60*24)){ // less than a day:
            // In case of days, better if refresh at 1 hour from the publication:
                minutePublication =  moment(publicationTime).minutes();
                minuteNow =  moment(nowTime).minutes();
                timeToRefresh = 0;
                if (minutePublication <= minuteNow) {
                    timeToRefresh = 60 - (minuteNow - minutePublication);
                } else if (minutePublication > minuteNow) {
                    timeToRefresh = minutePublication - minuteNow;
                }
            updateAndRefresh( timeToRefresh*60*1000 );
        } else if (timeToNow < (60*60*24*7)) { // less than a week
            // In case of weeks, refresh with the change of the days.
                // Next day (add(1,'d')) at 0 hours and 0 minutes:
                timeRefresh = moment().add(1, 'd').hours(0).minutes(0);
                // milliseconds to the next day:
                timeToRefresh = moment(timeRefresh).diff(moment());
            var to_append = "el " + moment(publicationTime).format('dddd');
            $(time).text(to_append);
            setTimeout(datetime, timeToRefresh);
        } else if (timeToNow > (60*60*24*7)) { // more than a week
            $(time).text(publicationTime.format('LLL'));
        }

    }
})();
