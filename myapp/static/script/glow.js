$(function() {  
    var glower = $('#myGlower');
    window.setInterval(function() {  
        glower.toggleClass('active');
    }, 1000);
});