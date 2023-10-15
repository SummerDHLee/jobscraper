const btn = document.querySelector("button");
const options = document.querySelectorAll('input[type="radio"]');

function handleButtonClicked(event) {
  btn.setAttribute("aria-busy", "true");
  //   event.preventDefault();
}

function handleWindowLoad() {
  btn.removeAttribute("aria-busy");
}

function handleOptionSelected() {
  const summary = document.querySelector("summary");
  summary.innerText = this.id;
}

btn.addEventListener("click", handleButtonClicked);

window.addEventListener("load", handleWindowLoad);

for (let i = 0; i < options.length; i++) {
  options[i].addEventListener("click", handleOptionSelected);
}
