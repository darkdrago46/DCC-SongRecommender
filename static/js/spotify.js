function triggerEmpty(){
    $("h3").empty();
    $("p").empty();
}

$(".is-primary").on("click", function(){
    $(this).addClass("is-loading");
    $("progress").fadeIn();
    triggerEmpty();
});

$(".is-danger").on("click",function(){
    $( "#displayEle").animate({height:"toggle"}, function() {
        // Animation complete.
        triggerEmpty();
        $("form").trigger("reset");
        window.location.href='http://127.0.0.1:9324/';
      });
});
