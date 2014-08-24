$(window).scroll(function () {
   if ($(window).scrollTop() == $(document).height() - $(window).height()) {
       $("footer").fadeIn();
   }
   else{
       $("footer").fadeOut();
   }
});
$(document).ready(function() {
    if ($(window).scrollTop() != $(document).height() - $(window).height()) {
       $("footer").hide();
   }
});
