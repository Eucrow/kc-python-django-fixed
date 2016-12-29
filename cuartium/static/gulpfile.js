// importamos gulp
var gulp = require('gulp');
var sass = require('gulp-sass');
var notify = require('gulp-notify');
var browserSync = require('browser-sync').create();//hacemos ya una instacia del browser-sync
var browserify = require('browserify');
var tap = require('gulp-tap');
var buffer = require('gulp-buffer');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var postcss = require('gulp-postcss');
var autoprefixer = require('autoprefixer');
var cssnano = require('cssnano');
var imagemin = require('gulp-imagemin');
var spritesmith = require('gulp.spritesmith');
var responsive = require('gulp-responsive-images');

//variables d epatrones de archivos
var jsFiles =["src/js/*.js/", "src/js/**/*.js"];
var spriteDir = ["src/img/sprites/*.png", "src/img/sprites/*.jpg", "src/img/sprites/*.gif", "src/img/sprites/*.svg"];
var uploadedImages = ["uploads/*.png", "uploads/*.jpg", "uploads/*.gif", "uploads/*.svg"];
var imageDir = ["./img/*"]

// definimos tarea por defecto
gulp.task("default", ["concat-js", "compile-sass", "spritesheet"], function(){
    //iniciamos browserSync
    browserSync.init({
        //server: "./",//levanta el servidor web en la carpeta actual
        proxy: "127.0.0.1:8000",    // actúa como proxy enviado las peticiones a
                                    //sparrest que está en el puerto 8000
        browser: "chrome"
    });
    // observa cambios en archivos SASS y ejecuta la tarea de compilación
    gulp.watch("src/scss/*.scss", ["compile-sass"]);

    // observa cambio en archivos HTML y recarga el navegador
    gulp.watch("*.html").on("change", browserSync.reload);

    //observar cambios en archivos js
    gulp.watch(jsFiles, ["concat-js"]);

    //observar cambios en los assets para optimzarlos
    gulp.watch(spriteDir, ["spritesheet"]);

    gulp.watch()
});

// definimos la tarea para compilar SASS
gulp.task("compile-sass", function(){
    gulp.src("./src/scss/style.scss") // cargamos el archivo
    .pipe(sourcemaps.init()) // comenzamos la captura de sourcemaps
    .pipe(sass().on('error', sass.logError)) // compilamos el archivo SASS
                                            //y gestionamos los errores
    .pipe(postcss([
        autoprefixer(), //autoprefija automáticamente el css
        //cssnano() //minifica el css
     ]))
    .pipe(sourcemaps.write('./')) // escribimos los sourcemaps
    .pipe(gulp.dest("./dist/css/")) // guardamos el archivo en dist/css
    .pipe(notify({
        title: "SASS compiled",
        message: "ok"
    }))
    .pipe(browserSync.stream());
});

// definimos la tarea para concatenar JS
gulp.task("concat-js", function(){
    gulp.src("src/js/app.js")
    //.pipe(concat("app.js"))
    .pipe(sourcemaps.init()) // comenzamos la captura de sourcemaps
    .pipe(tap(function(file){ // tap nos permite ejecutar un código por cada fichero seleccionado en el paso anterior
        file.contents = browserify(file.path).bundle(); //pasamoso el archivo por browserify para importar los require
    }))
    .pipe(buffer())//convierte cada archivo en un stream ¿¿¿¿que qué????
    .pipe(uglify()) // minifica el javascript
    .pipe(sourcemaps.write('./')) // escribimos los sourcemaps
    .pipe(gulp.dest("./dist/js/"))
    .pipe(notify({
        title: "JS concatenated",
        message: "ok"
    }))
    .pipe(browserSync.stream());
});

// optimizacion de assets assest: crea un spritesheet con todos los assets
gulp.task("spritesheet", function(){
   var spriteData = gulp.src('./src/img/sprites/*')
   .pipe(spritesmith({
       imgName: 'sprite.png',
       cssName: '_sprite.scss',
       imgPath:'../img/sprite.png'
   }));

   spriteData.img.pipe(buffer()).pipe(imagemin()).pipe(gulp.dest('./dist/img/'));
   spriteData.css.pipe(gulp.dest('./src/scss/'));
});

// optimización de imágenes de usuario
// esto en teoría lo debería hacer el backend, no es lo mejor en un sistema de producción
// lo hacemos así para ver como se utiliza
gulp.task("uploaded-images-optimization", function(){
   gulp.src(uploadedImages)
   .pipe(imagemin())
   .pipe(gulp.dest(uploadedImages));
});

// optimización de imágenes de usuario para responsive
// se debería hacer en el backend
gulp.task("responsive", function(){
    gulp.src('./uploads/*.jpg')
    .pipe(responsive({
        '*.jpg':[
            { width: 1280, suffix: "_1280"},
            { width: 800, suffix: "_800"},
            { width: 400, suffix: "_400"}
        ]
    }))
    .pipe(gulp.dest('./dist/uploads/'))
});
