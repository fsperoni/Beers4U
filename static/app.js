//Get the button:
const mybutton = document.getElementById("myBtn")

window.onscroll = function() {toggleShowButton()}

/** Shows the button only when user scrolls down 20px from the top of the document*/
function toggleShowButton() {
  if (document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block"
  } else {
    mybutton.style.display = "none"
  }
}

/**  Scroll to the top of the document */
function scrollToTop() {
  document.documentElement.scrollTop = 0 
}