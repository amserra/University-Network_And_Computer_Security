window.onload = () => {
  // Access the DOM once
  const toggle_span = document.getElementsByClassName("toggle-password")[0];
  const button = document.getElementsByClassName("btn-login")[0];
  const email = document.getElementsByName("email")[0];
  const password = document.getElementsByName("password")[0];

  email.addEventListener("input", () => checkButtton(button, email, password));
  password.addEventListener("input", () => checkButtton(button, email, password));

  toggle_span.addEventListener("mouseenter", (e) => showPassword(e, password));
  toggle_span.addEventListener("mouseleave", (e) => hidePassword(e, password));
};

function showPassword(e, password) {
  password.type = "text";
  e.target.innerHTML = "🙈";
}

function hidePassword(e, password) {
  password.type = "password";
  e.target.innerHTML = "👁️";
}

function checkButtton(button, email, password) {
  if (email.value.length && password.value.length) button.disabled = false;
  else button.disabled = true;
}
