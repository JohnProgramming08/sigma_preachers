const formBtn = document.getElementById("display-form-btn");
const form = document.querySelector("form");

function displayForm() {
    form.classList.remove("d-none");
    formBtn.classList.add("d-none");
}