window.onload = () => {
  // Access the DOM once
  let toggle_spans = document.getElementsByClassName("toggle-password");
  const old_password = toggle_spans[0];
  const new_password = toggle_spans[1];
  const confirm_new_password = toggle_spans[2];

  old_password.addEventListener("mouseenter", showPassword);
  old_password.addEventListener("mouseleave", hidePassword);

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
