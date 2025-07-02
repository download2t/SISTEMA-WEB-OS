document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    document.querySelectorAll(".messages-container .alert").forEach((msg) => {
      msg.style.opacity = "0";
      setTimeout(() => (msg.style.display = "none"), 300); // espera a transição
    });
  }, 10000);
});


document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const loginBtn = document.getElementById("loginBtn");
  const successMessage = document.getElementById("successMessage");
  const errorMessage = document.getElementById("errorMessage");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");

  if (loginForm && loginBtn) {
    loginForm.addEventListener("submit", async function (e) {
      e.preventDefault(); // Impede o envio padrão do formulário

      // Oculta mensagens anteriores
      successMessage.style.display = "none";
      errorMessage.style.display = "none";

      // Estado de carregamento
      loginBtn.classList.add("loading");
      loginBtn.disabled = true;
      loginBtn.textContent = "Entrando...";

      const csrftoken = getCookie("csrftoken"); // Pega o token CSRF

      try {
        const response = await fetch(loginForm.action, {
          // Usa a action do formulário
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrftoken,
          },
          body: new URLSearchParams({
            username: usernameInput.value,
            password: passwordInput.value,
          }).toString(),
        });

        const data = await response.json(); // Analisa a resposta JSON

        if (response.ok) {
          // Verifica se a resposta HTTP é 2xx (sucesso)
          successMessage.style.display = "flex";
          // Limpa os campos
          usernameInput.value = "";
          passwordInput.value = "";

          // Redireciona após um pequeno atraso para a mensagem ser vista
          setTimeout(() => {
            window.location.href = data.redirect_url;
          }, 2000); // 2 segundos
        } else {
          // Exibe a mensagem de erro da resposta JSON
          errorMessage.querySelector("span").textContent =
            data.message || "Ocorreu um erro desconhecido.";
          errorMessage.style.display = "flex";

          // Oculta a mensagem de erro após um tempo
          setTimeout(() => {
            errorMessage.style.display = "none";
          }, 5000); // 5 segundos
        }
      } catch (err) {
        console.error("Erro de rede ou na requisição:", err);
        errorMessage.querySelector("span").textContent =
          "Erro de conexão. Tente novamente.";
        errorMessage.style.display = "flex";

        setTimeout(() => {
          errorMessage.style.display = "none";
        }, 5000);
      } finally {
        // Remove o estado de carregamento, independentemente do sucesso/erro
        loginBtn.classList.remove("loading");
        loginBtn.disabled = false;
        loginBtn.textContent = "Entrar";
      }
    });
  }

  // Função utilitária para obter o CSRF do cookie (já tinha no seu código)
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Efeitos visuais adicionais (mantidos do seu código original)
  document.querySelectorAll(".form-control").forEach((input) => {
    input.addEventListener("focus", function () {
      this.closest(".mb-3, .mb-4").style.transform = "translateY(-2px)";
    });

    input.addEventListener("blur", function () {
      this.closest(".mb-3, .mb-4").style.transform = "translateY(0)";
    });
  });

  // Ripple effect no botão de login (mantido do seu código original)
  loginBtn.addEventListener("click", function (e) {
    if (loginBtn.classList.contains("loading")) return; // Não adiciona ripple se já estiver carregando

    const ripple = document.createElement("span");
    const rect = this.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: rippleEffect 0.6s ease-out;
            pointer-events: none;
            z-index: 1;
        `;

    this.appendChild(ripple);

    setTimeout(() => {
      ripple.remove();
    }, 600);
  });

});

// Toggle de visibilidade da senha
const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");

togglePassword.addEventListener("click", function () {
  const type =
    passwordInput.getAttribute("type") === "password" ? "text" : "password";
  passwordInput.setAttribute("type", type);
  this.classList.toggle("fa-eye");
  this.classList.toggle("fa-eye-slash");
});