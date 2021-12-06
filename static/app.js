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

/** Toggle Sort feedback button enabled/disabled */
const checkSortInput = (e) => {
  const sortFields = $('.sort')
  let isDisabled = false
  sortFields.each(function() {
    if ($(this).val().trim() === '') {
      isDisabled = true
      return false
    }
  })
  $('#sortBtn').prop('disabled', isDisabled)
}
$('#sortForm').on('change', checkSortInput)

/** Initialize tooltips */
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

/** Clear the recipe search form */
const clearRecipeForm = () => {
  $('#recipeForm').trigger('reset')
  $('#recipeForm').find("p").remove(".error")
  $('#recipeBtn').prop('disabled', true)
}
$('#clearBtn').on('click', clearRecipeForm)

/** Validate the recipe search form, preventing submission upon errors */
const validateRecipeForm = (e) => {
  $('#recipeForm').find("p").remove(".error")
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
  if (hasErrors) e.preventDefault()

}
$('#recipeForm').on('submit', validateRecipeForm)

/** Clear the sort feedback form */
const clearSortForm = () => {
  $('#sortForm').trigger('reset')
  $('#sortForm').find("p").remove(".error")
  $('#sortBtn').prop('disabled', true)
}

/** Validate the sort feedback form, preventing submission upon errors */
const validateSortForm = (e) => {
  $('#sortForm').find("p").remove(".error")
  let hasErrors = false
  const form = document.getElementById('sortForm')
  const formData = new FormData(form)
  if (!formData.get('sort-field')) {
    hasErrors = true
    const msg = $('<p>').addClass('error').html('<small class="text-danger">Check this entry.</small>')
    $('#sort-field').parent().append(msg)
  }
  if (!formData.get('sort-order')) {
    hasErrors = true
    const msg = $('<p>').addClass('error').html('<small class="text-danger">Check this entry.</small>')
    $('#sort-order').parent().append(msg)
  }
  if (hasErrors) {
    e.preventDefault()
  } 
}
$('#sortForm').on('submit', validateSortForm)

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

/**Process toggling like on feedbacks and udpate icons*/
$(document).on('click', '.like-btn', async function () {
  const feedbackId = $(this.dataset)[0].feedbackId
  $(this).toggleClass("btn-primary")
  const response = await toggleLike(feedbackId)
  // if toggle is not successful, update button and alert user
  if (response.status !== 200) {
    $(this).toggleClass("btn-primary")
    alert("An error occurred, please try again.")
    return
  }
  if (response.data.dislike === "deleted") {
    $(this).siblings('.dislike-btn').toggleClass("btn-danger")
  }
  const counters = response.data.counters
  $(this).children("small").text(counters.likes)
  $(this).siblings('.dislike-btn').children("small").text(counters.dislikes)
})

/**Toggles like on server/database */
async function toggleLike(feedbackId) {
  const res = await axios({
    method: "POST",
    url: `/users/feedbacks/${feedbackId}/like`
  })
  return res
}

/**Process toggling dislike on feedbacks and udpate icons*/
$(document).on('click', '.dislike-btn', async function () {
  const feedbackId = $(this.dataset)[0].feedbackId
  $(this).toggleClass("btn-danger")
  const response = await toggleDislike(feedbackId)
  // if toggle is not successful, update button and alert user
  if (response.status !== 200) {
    $(this).toggleClass("btn-danger")
    alert("An error occurred, please try again.")
    return
  }
  if (response.data.like === "deleted") {
    $(this).siblings('.like-btn').toggleClass("btn-primary")
  }
  const counters = response.data.counters
  $(this).children("small").text(counters.dislikes)
  $(this).siblings('.like-btn').children("small").text(counters.likes)
})

/**Toggles dislike on server/database */
async function toggleDislike(feedbackId) {
  const res = await axios({
    method: "POST",
    url: `/users/feedbacks/${feedbackId}/dislike`
  })
  return res
}

/** Goes back using browser history */
const goBack = () => {
  window.history.back()
}

//The scroll to the top button
const scrollButton = document.getElementById("scrollBtn")

//Add scroll event listener
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

