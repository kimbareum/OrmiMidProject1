const category_btns = document.querySelectorAll(".categories a");
const sort_btns = document.querySelectorAll(".sort-options a");
const page_btns = document.querySelectorAll(".search-page")
const activate_link = () => {
  location.href = `/blog/?category=${category}&&sort=${sort_option}&&page=${page}`;
}

category_btns.forEach(btn => {
  btn.addEventListener('click', (event) => {
    event.preventDefault();
    const link_text = event.target.href.split('/');
    category = link_text[link_text.length-1];
    page = 1
    activate_link();
  })
})

sort_btns.forEach(btn => {
  btn.addEventListener('click', (event) => {
    event.preventDefault();
    const link_text = event.target.href.split('/');
    sort_option = link_text[link_text.length-1];
    page = 1
    activate_link();
  })
})

if (page_btns) {
  page_btns.forEach(btn => {
    btn.addEventListener('click', (event) => {
      event.preventDefault();
      const link_text = event.target.href.split('/');
      page = link_text[link_text.length-1];
      activate_link();
    })
  })
}