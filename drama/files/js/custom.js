/*
 * Custom scripts for drama page
 * --------------------------------------------------
 */

// document ready 
$(document).ready(function () {

    // method :: re-focus
    $('.spy-enabled').click( function(){
        $('html,body').animate({scrollTop: $($(this).attr('href')).offset().top - 60}, 'slow');
    });

});

