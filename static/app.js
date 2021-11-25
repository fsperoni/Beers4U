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
const clearForm = () => {
  $('#recipeForm').trigger('reset');
  $('#recipeBtn').prop('disabled', true);
}
$('#clearBtn').on('click', clearForm)

/** Validate the recipe search form, preventing submission upon errors */
const validateForm = (e) => {
  $("p").remove(".error")
  let hasErrors = false
  const form = document.getElementById('recipeForm')
  const formData = new FormData(form)
  if (parseInt(formData.get('abv_gt')) > parseInt(formData.get('abv_lt'))) {
    const msg = $('<p>').addClass('error').html('<small class="text-danger">Check this entry.</small>')
    $('#formABV').append(msg)
    hasErrors = true
  }
  if (parseInt(formData.get('ibu_gt')) > parseInt(formData.get('ibu_lt'))) {
    const msg = $('<p>').addClass('error').html('<small class="text-danger">Check this entry.</small>')
    $('#formIBU').append(msg)
    hasErrors = true
  }
  if (parseInt(formData.get('ebc_gt')) > parseInt(formData.get('ebc_lt'))) {
    const msg = $('<p>').addClass('error').html('<small class="text-danger">Check this entry.</small>')
    $('#formEBC').append(msg)
    hasErrors = true
  }
  if (hasErrors) {
    e.preventDefault()
  } else {
    clearForm()
  }
}
$('#recipeForm').on('submit', validateForm)

/** Toggle favorite icon on pages that display recipes or pairings */
const toggleFavoriteIcon = () => {
  $('#favPairBtn').toggleClass("btn-danger")
  $('#favPairBtn').toggleClass("btn-secondary")
}
$('#favPairing').on('submit', toggleFavoriteIcon)

// ABOVE NEEDS TO BE ADJUSTED, CAN'T USE FORM ID.... USE DATA-REC-ID (DATA ATTRIBUTE)? OR THIS WITH DELEGATION?
// TOGGLE FAVORITE NEEDS JQUERY FOR FRONT-END AND AXIOS TO PROCESS BACKEND.

const goBack = (e) => {
  window.history.back()
}
//Get the button:
const scrollButton = document.getElementById("scrollBtn")

window.onscroll = function() {toggleShowButton()}

/** Shows the button only when user scrolls down 20px from the top of the document*/
const toggleShowButton = () => {
  if (document.documentElement.scrollTop > 20) {
    scrollButton.style.display = "block"
  } else {
    scrollButton.style.display = "none"
  }
}

/**  Scroll to the top of the document */
const scrollToTop = () => {
  document.documentElement.scrollTop = 0 
}

