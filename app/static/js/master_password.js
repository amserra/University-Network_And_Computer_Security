window.onload = () => {
  // Access the DOM once
  let toggle_spans = document.getElementsByClassName("toggle-password");
  const master_password = toggle_spans[0];

  master_password.addEventListener("mouseenter", showPassword);
  master_password.addEventListener("mouseleave", hidePassword);
};

function showPassword(e) {
  e.relatedTarget.type = "text";
  e.target.innerHTML = "🙈";
}

function hidePassword(e) {
  e.relatedTarget.type = "password";
  e.target.innerHTML = "👁️";
}
