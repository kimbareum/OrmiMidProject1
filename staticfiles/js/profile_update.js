const form = document.querySelector(".profile")
const get_image = form.querySelector("#get_image")
const profile_thumbnail = form.querySelector(".profile-thumbnail")

let result = ""
get_image.onchange = (event) => {
  const reader = new FileReader();
  const file = get_image.files[0]
  if (file) {
    reader.readAsDataURL(file);
    reader.onload = function(e) {
      result = e.target.result
      profile_thumbnail.src = result;
    }
  }
  else {
    profile_thumbnail.src = form.image.value
  }
}

form.addEventListener("submit", (event)=>{
  event.preventDefault()
  if (result) {
    event.target.image.value = result
  }
  form.submit()
})