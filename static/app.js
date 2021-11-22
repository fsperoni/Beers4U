/** Toggle Beer search button enabled/disabled. */
const checkBeerInput = (e) => {
  $('#beerBtn').prop('disabled', (e) => {
    return $("#beerInput").val().trim() === ''
  })
}
$(document).on('change', '#beerInput', checkBeerInput);

/** Toggle Food search button enabled/disabled */
const checkFoodInput = (e) => {
  $('#foodBtn').prop('disabled', (e) => {
    return $("#foodInput").val().trim() === ''
  })
}
$(document).on('change', '#foodInput', checkFoodInput);

/** Toggle Recipe search button enabled/disabled */
const checkRecipeInput = (e) => {
  const inputIds = $('.recipe')
  let isDisabled = true
  inputIds.each(function() {
    if ($(this).val().trim() !== '') {
      isDisabled = false
      console.log(isDisabled)
      console.log($(this).val().trim())
      return false
    }
  })
  $('#recipeBtn').prop('disabled', isDisabled)
}
$('#recipeForm').on('change', checkRecipeInput)

/** Initialize tooltips */
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

/** Clear the recipe search form */
const clearForm = (e) => {
  e.preventDefault()
  $('#recipeForm').trigger('reset')
  $('#recipeBtn').prop('disabled', true)
}
$('#clearBtn').on('click', clearForm)


//Get the button:
const scrollButton = document.getElementById("scrollBtn")

// window.onscroll = function() {toggleShowButton()}

/** Shows the button only when user scrolls down 20px from the top of the document*/
function toggleShowButton() {
  if (document.documentElement.scrollTop > 20) {
    scrollButton.style.display = "block"
  } else {
    scrollButton.style.display = "none"
  }
}

/**  Scroll to the top of the document */
function scrollToTop() {
  document.documentElement.scrollTop = 0 
}