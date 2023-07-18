const recomment_btns = document.querySelectorAll('.btn-recomment')

recomment_btns.forEach(btn => {
  const recomment_wrap = btn.nextElementSibling
  btn.addEventListener("click", (event) => {
    recomment_wrap.setAttribute('style', 'display:block;')
  })

  const recomment_cancle_button = recomment_wrap.firstElementChild.lastElementChild
  recomment_cancle_button.addEventListener("click", (event) => {
    recomment_wrap.setAttribute('style', 'display:none')
  })
});
