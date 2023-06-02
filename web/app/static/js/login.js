window.onload = () => {
  // Access the DOM once
  const toggle_span = document.getElementsByClassName("toggle-password")[0];
  const button = document.getElementsByClassName("btn-login")[0];
  const email = document.getElementsByName("email")[0];
  const password = document.getElementsByName("password")[0];

  email.addEventListener("input", () => checkButtton(button, email, password));
  password.addEventListener("input", () => checkButtton(button, email, password));

  toggle_span.addEventListener("mouseenter", showPassword);
  toggle_span.addEventListener("mouseleave", hidePassword);
};

function showPassword(e) {
  e.relatedTarget.type = "text";
  e.target.innerHTML = "🙈";
}

function hidePassword(e) {
  e.relatedTarget.type = "password";
  e.target.innerHTML = "👁️";
}

function checkButtton(button, email, password) {
  if (email.value.length && password.value.length) button.disabled = false;
  else button.disabled = true;
}
