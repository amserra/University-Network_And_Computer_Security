window.onload = () => {
  // Access the DOM once
  const toggle_span1 = document.getElementsByClassName("toggle-password")[0];
  const toggle_span2 = document.getElementsByClassName("toggle-password")[1];
  const bars = document.getElementsByClassName("bar");
  const validation = document.getElementById("validation-links");
  const password = document.getElementsByName("password")[0];
  const confirmPassword = document.getElementsByName("confirmPassword")[0];
  password.setCustomValidity(" ");
  confirmPassword.setCustomValidity(" ");

  password.addEventListener("input", (e) => validatePassword(e, bars, validation, confirmPassword));
  confirmPassword.addEventListener("input", (e) => checkPasswordMatch(password, confirmPassword));

  toggle_span1.addEventListener("mouseenter", (e) => showPassword(e, password));
  toggle_span2.addEventListener("mouseenter", (e) => showPassword(e, confirmPassword));
  toggle_span1.addEventListener("mouseleave", (e) => hidePassword(e, password));
  toggle_span2.addEventListener("mouseleave", (e) => hidePassword(e, confirmPassword));
};

var strength = 0;
var prevStrength = 0;
var validations = [];

function showPassword(e, field) {
  field.type = "text";
  e.target.innerHTML = "🙈";
}

function hidePassword(e, field) {
  field.type = "password";
  e.target.innerHTML = "👁️";
}

function checkPasswordMatch(password, confirmPassword) {
  // customValidity = " " => red; customValidity = "" => green

  if (password.value == confirmPassword.value) {
    if (strength >= 4) {
      // Both match & Password passes validation
      password.setCustomValidity("");
      confirmPassword.setCustomValidity("");
    } else {
      // Both match & Password fails validation
      password.setCustomValidity(" ");
      confirmPassword.setCustomValidity("");
    }
  } else {
    if (strength >= 4) {
      // Don't match & Password passes validation
      password.setCustomValidity("");
      confirmPassword.setCustomValidity(" ");
    } else {
      // Don't match & Password fails validation
      password.setCustomValidity(" ");
      confirmPassword.setCustomValidity(" ");
    }
  }
}

function reassessBars(bars) {
  if (strength == 0) {
    removeClass(bars[0]);
    removeClass(bars[1]);
    removeClass(bars[2]);
    removeClass(bars[3]);
  } else if (strength == 1) {
    addClass(bars[0]);
    removeClass(bars[1]);
    removeClass(bars[2]);
    removeClass(bars[3]);
  } else if (strength == 2) {
    addClass(bars[0]);
    addClass(bars[1]);
    removeClass(bars[2]);
    removeClass(bars[3]);
  } else if (strength == 3) {
    addClass(bars[0]);
    addClass(bars[1]);
    addClass(bars[2]);
    removeClass(bars[3]);
  } else if (strength >= 4) {
    addClass(bars[0]);
    addClass(bars[1]);
    addClass(bars[2]);
    addClass(bars[3]);
  }
}

function validatePassword(e, bars, validation, confirmPassword) {
  const password = e.target.value;

  validations = [
    password.length >= 8,
    password.search(/[A-Z]/) > -1,
    password.search(/[0-9]/) > -1,
    password.search(/[$&+,:;=?@#!]/) > -1,
  ];

  strength = validations.reduce((acc, cur) => acc + cur, 0);

  if (strength == prevStrength + 1) {
    addClass(bars[prevStrength]);
  } else if (strength == prevStrength - 1) {
    removeClass(bars[strength]);
  } else {
    // When user deletes multiple characters with one input (e.g.: ctrl+x)
    reassessBars(bars);
  }

  prevStrength = strength;

  updateValidationLinks(validation.children);

  checkPasswordMatch(e.target, confirmPassword);
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
