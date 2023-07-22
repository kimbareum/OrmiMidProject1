const Editor = toastui.Editor;
const editor = new Editor({
    el: document.querySelector("#editor"),
    height: "600px",
    initialEditType: "wysiwyg",
    previewStyle: "vertical",
    initialValue: post_content || ""
});

const write_form = document.querySelector('#write-form');
const form_content = document.querySelector('#form-content')
const form_thumbnail = document.querySelector('#form-thumbnail')

write_form.addEventListener("submit", (e) => {
  e.preventDefault()
  form_content.value = editor.getHTML();
  const thumbnail = form_content.value.match(/<img[^>]+src="?([^"\s]+)"?\s*[^>]*>/);
  if (thumbnail) {
    form_thumbnail.value = thumbnail[1];
  }
  else {
    form_thumbnail.value = `/static/images/post-img${Math.floor(Math.random() * 6) + 1}.jpg`
  }
  write_form.submit()
})

const select_wrap = document.querySelector('.select-wrap');
const selects = select_wrap.querySelectorAll("input");
const selected_category_list = []
const selected_category = document.querySelector('.selected-category');
const select_button = document.querySelector('.btn-select');

for (const tag_wrap of selected_category.querySelectorAll('dd')){
  selected_category_list.push(tag_wrap.innerText)
}

selects.forEach((select) => {
  select.addEventListener(("click"), (event) => {
    if (event.target.checked) {
      selected_category_list.push(event.target.value)
    }
    else {
      const value = event.target.value
      for (const index in selected_category_list) {
        if (selected_category_list[index] === value) {
          selected_category_list.splice(index , 1);
        }
      }
    }
    renderSelectCategory()
  })
})

renderSelectCategory = () => {
  if (selected_category_list.length > 0) {
    let result = "<dl class='category'><dt class='a11y-hidden'>선택된 카테고리</dt>"
    for (const category of selected_category_list) {
      result += `<dd>${category}</dd>`
    }
    result += "</dl>"
    selected_category.innerHTML = result
  }
  else {
    selected_category.innerHTML = '카테고리 선택'
  }
}

select_button.addEventListener("click", (event) => {
  select_wrap.classList.toggle("no-display")
})