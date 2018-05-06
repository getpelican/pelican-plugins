window.addEventListener("load", function() {
  document.querySelector(".wiki-nav-button").addEventListener('click', function(event) {
    document.querySelector(".wiki-links").classList.toggle('nodisplay');
    event.target.text = event.target.text == "Expand Menu" ? "Collapse Menu" : "Expand Menu";
  }, false);
  var expanders = document.querySelectorAll(".wiki-dir-expander");
  for (i = 0; i < expanders.length; ++i) {
    expanders[i].addEventListener('click', function(event) {
      event.target.parentElement.nextSibling.nextSibling.classList.toggle("nodisplay");
      event.target.text = event.target.text == "+" ? "-" : "+";
    }, false);
  };
}, false);
