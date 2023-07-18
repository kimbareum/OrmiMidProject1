const back_button = document.querySelector('.btn-back')
const top_button = document.querySelector('.top-button')

if (back_button) {
  back_button.addEventListener('click', (event) => {
    event.preventDefault();
    window.history.back()
  })
}

if (top_button) {
  top_button.addEventListener('click', (event) => {
    window.scrollTo({top: 0, behavior:'smooth'});
  })
}