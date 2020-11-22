window.onload = () => {
    // Access the DOM once
    const button = document.getElementsByClassName("btn-confirm-code")[0];
    const code_2FA = document.getElementsByName("code_2FA")[0];
  
    code_2FA.addEventListener("input", () => checkButtton(button, code_2FA));
  
  };
  

  function checkButtton(button, code_2FA) {
    console.log(code_2FA);
    if (code_2FA.value.length) button.disabled = false;
    else button.disabled = true;
  }
  