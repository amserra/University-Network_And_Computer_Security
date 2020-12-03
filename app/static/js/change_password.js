window.onload = () => {
  // Access the DOM once
  let toggle_spans = document.getElementsByClassName("toggle-password");
  const new_password = toggle_spans[0];
  const confirm_new_password = toggle_spans[1];

  new_password.addEventListener("mouseenter", showPassword);
  new_password.addEventListener("mouseleave", hidePassword);

  confirm_new_password.addEventListener("mouseenter", showPassword);
  confirm_new_password.addEventListener("mouseleave", hidePassword);
};

function showPassword(e) {
  e.relatedTarget.type = "text";
  e.target.innerHTML = "🙈";
}

function hidePassword(e) {
  e.relatedTarget.type = "password";
  e.target.innerHTML = "👁️";
}
