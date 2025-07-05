// Validação de formulário (mantido)
(function () {
  "use strict";
  window.addEventListener(
    "load",
    function () {
      var forms = document.getElementsByClassName("needs-validation");
      Array.prototype.filter.call(forms, function (form) {
        form.addEventListener(
          "submit",
          function (event) {
            if (form.checkValidity() === false) {
              event.preventDefault();
              event.stopPropagation();
            }
            form.classList.add("was-validated");
          },
          false
        );
      });

      // Lógica para alternar visibilidade da senha
      document.querySelectorAll(".toggle-password").forEach((button) => {
        button.addEventListener("click", function () {
          const targetId = this.dataset.target;
          const passwordInput = document.getElementById(targetId);
          const icon = this.querySelector("i");

          if (passwordInput.type === "password") {
            passwordInput.type = "text";
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
          } else {
            passwordInput.type = "password";
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
          }
        });
      });
    },
    false
  );
})();
