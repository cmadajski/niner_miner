const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navLinks.classList.toggle("active");
})

document.querySelectorAll(".nav-links li a").forEach(n => n.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navLinks.classList.remove("active");
}))

$(document).ready(function() {
    $(".select-category").change(function(){
        $("#widthTempOption").html($('.select-category option:selected').text());
        $(this).width($("#selectTagWidth").width()+31);
        $("#search").width("600px");
        $("#search").width($("#search").width()-$(this).width()+56)
    });
});