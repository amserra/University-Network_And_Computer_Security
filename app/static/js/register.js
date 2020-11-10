window.onload = () => {
  // Access the DOM once
  const toggle_span = document.getElementsByClassName("toggle-password")[0];
  const button = document.getElementsByClassName("btn-register")[0];
  const bars = document.getElementsByClassName("bar");
  const validation = document.getElementById("validation-links");
  const name = document.getElementsByName("name")[0];
  const email = document.getElementsByName("email")[0];
  const password = document.getElementsByName("password")[0];

  password.addEventListener("input", (e) =>
    validatePassword(e, button, bars, validation, name, email)
  );
  name.addEventListener("input", () => checkButtton(button, name, email));
  email.addEventListener("input", () => checkButtton(button, name, email));

  toggle_span.addEventListener("mouseenter", (e) => showPassword(e, password));
  toggle_span.addEventListener("mouseleave", (e) => hidePassword(e, password));
};

var strength = 0;
var prevStrength = 0;
var validations = [];

function showPassword(e, password) {
  password.type = "text";
  e.target.innerHTML = "🙈";
}

function hidePassword(e, password) {
  password.type = "password";
  e.target.innerHTML = "👁️";
}

function checkButtton(button, name, email) {
  if (strength < 4 || !name.validity.valid || !email.validity.valid) button.disabled = true;
  else button.disabled = false;
}

function validatePassword(e, button, bars, validation, name, email) {
  const password = e.target.value;

  validations = [
    password.length >= 8,
    password.search(/[A-Z]/) > -1,
    password.search(/[0-9]/) > -1,
    password.search(/[$&+,:;=?@#!]/) > -1,
  ];

  strength = validations.reduce((acc, cur) => acc + cur, 0);

  checkButtton(button, name, email);

  if (strength > prevStrength) {
    addClass(bars[prevStrength]);
  } else if (strength < prevStrength) {
    removeClass(bars[strength]);
  }

  prevStrength = strength;

  updateValidationLinks(validation.children);
}

function updateValidationLinks(list) {
  list[0].innerHTML = (validations[0] ? "✔️" : "❌") + list[0].innerHTML.substr(1, list[0].length);
  list[1].innerHTML = (validations[1] ? "✔️" : "❌") + list[1].innerHTML.substr(1, list[0].length);
  list[2].innerHTML = (validations[2] ? "✔️" : "❌") + list[2].innerHTML.substr(1, list[0].length);
  list[3].innerHTML = (validations[3] ? "✔️" : "❌") + list[3].innerHTML.substr(1, list[0].length);
}

function addClass(element) {
  if (!element.className.includes(" bar-show")) element.className += " bar-show";
}

function removeClass(element) {
  element.className = element.className.replace(" bar-show", "");
}
