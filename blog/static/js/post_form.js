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