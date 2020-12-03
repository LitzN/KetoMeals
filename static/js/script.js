  $(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $('.collapsible').collapsible();

    $(".open-main").click(function(){
    $(".mains").removeClass("hide");
    $(".snacks").addClass("hide");
    $(".desserts").addClass("hide")
})

    $(".open-snack").click(function(){
    $(".snacks").removeClass("hide");
    $(".mains").addClass("hide");
    $(".desserts").addClass("hide")
})

$(".open-dessert").click(function(){
    $(".desserts").removeClass("hide");
    $(".mains").addClass("hide");
    $(".snack").addClass("hide")
})
})

