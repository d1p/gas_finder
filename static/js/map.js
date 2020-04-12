$(document).ready(function(){
    var height = $('.map-content').innerHeight();
    console.log(height);
    $('.side-bar-location').css('height', height);
    
    var screen_width = $(window).width();
    console.log(screen_width);
    
    if(screen_width > 1905){
        height = height + 66;
        resizeHeight(height)
    }

    function resizeHeight(h){
        $('.side-bar-location').css('height', h);
    }
});