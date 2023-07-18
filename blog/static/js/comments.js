const recomment_btns = document.querySelectorAll('.recomment')

recomment_btns.forEach(btn => {
  const comment_form = btn.nextElementSibling
  btn.addEventListener("click", (event) => {
    comment_form.classList.toggle("no-display")
  })

  const recomment_cancle_button = comment_form.lastElementChild
  recomment_cancle_button.addEventListener("click", (event) => {
    comment_form.classList.toggle("no-display")
  })
});
