var gulp = require('gulp'),
less = require('gulp-less'),
watch = require('gulp-watch');

// Compile less to css
gulp.task('less', function () {
    gulp.src('public/less/app.less')
    .pipe(less()).on('error',function(e){ console.log(e); })
    .pipe(gulp.dest('public/css'));
});

// Watch on files changes
gulp.task('watch', function() {
    gulp.watch('public/less/*.less', ['less']);
});

gulp.task('default', ['watch']);