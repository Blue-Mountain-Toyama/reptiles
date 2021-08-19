"use strict";

var gulp = require("gulp");
var sass = require("gulp-sass");
var sassGlob = require('gulp-sass-glob');

sass.compiler = require("node-sass");

gulp.task("sass", function () {
  return gulp
    .src("./src/style/style.scss")
    .pipe(sassGlob())
    .pipe(sass().on("error", sass.logError))
    .pipe(sass({ outputStyle: "expanded" }))
    .pipe(gulp.dest('./src/static/css/'));
});

gulp.task("sass:watch", function () {
  gulp.watch("./src/style/*.scss", gulp.task("sass"));
  gulp.watch("./src/style/*/*.scss", gulp.task("sass"));
});
