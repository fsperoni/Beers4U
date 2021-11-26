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

/**Process toggling favorite recipes and udpates icon*/
$(document).on('click', '.fav-btn', async function () {
  const recId = $(this.dataset)[0].recId
  $(this).toggleClass("btn-danger")
  $(this).toggleClass("btn-secondary")
  const response = await toggleFav(recId)
  // if toggle is not successful, update button and alert user
  if (response.status !== 200) {
    $(this).toggleClass("btn-danger")
    $(this).toggleClass("btn-secondary")
    alert("An error occurred, please try again.")
  }
})

/**Toggles favorite on server/database */
async function toggleFav(recId) {
  const res = await axios({
    method: "POST",
    url: `/users/favorites/${recId}`
  })
  return res
}

/** Goes back using browser history */
const goBack = (e) => {
  window.history.back()
}

//Get the button:
const scrollButton = document.getElementById("scrollBtn")

window.onscroll = () => {toggleShowButton()}

/** Shows the button only when user scrolls down 100px from the top of the document*/
const toggleShowButton = () => {
  if (document.documentElement.scrollTop > 100) {
    scrollButton.style.display = "block"
  } else {
    scrollButton.style.display = "none"
  }
}

/**  Scroll to the top of the document */
const scrollToTop = () => {
  document.documentElement.scrollTop = 0 
}

