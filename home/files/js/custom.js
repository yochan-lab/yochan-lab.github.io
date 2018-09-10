/*
 * Custom scripts for Demo page
 * --------------------------------------------------
 */

// slow-scroll on active anchor tags

$(function() {
$('a[href*="#"]:not([href="#"])').click(function() {
if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
var target = $(this.hash);
target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
if (target.length) {
$('html, body').animate({
scrollTop: target.offset().top
}, 1000);
return false;
}
}
});


$("#sarath-img").hover(function(){
    $(this).attr("src", "files/images/sarath2.jpg");
}, function() {
    $(this).attr("src", "files/images/sarath1.jpg");
});

$("#sachin-img").hover(function(){
    $(this).attr("src", "files/images/sachin2.gif");
}, function() {
    $(this).attr("src", "files/images/sachin1.jpg");
});

});

