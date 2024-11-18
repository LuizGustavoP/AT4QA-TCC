var prevScrollpos = window.scrollY;
var headerDiv = document.getElementById("subHeaderGlossary");

window.onscroll = function() {
  var currentScrollPos = window.scrollY;

  if (prevScrollpos < currentScrollPos)
    headerDiv.style.top = "-8vh";
  else
    headerDiv.style.top = "0";

  prevScrollpos = currentScrollPos;
}