document
  .getElementById("recoveryForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const submitBtn = document.getElementById("submitBtn");
    const successMessage = document.getElementById("successMessage");
    const emailInput = document.getElementById("email");
    const csrftoken = getCookie("csrftoken"); // Captura o token CSRF

    // Reset mensagem anterior
    successMessage.style.display = "none";

    // Estado de carregamento
    submitBtn.classList.add("loading");
    submitBtn.textContent = "Enviando...";

    try {
      const response = await fetch("/password_reset/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrftoken,
        },
        body: new URLSearchParams({
          email: emailInput.value,
        }),
      });

      if (response.ok) {
        submitBtn.classList.remove("loading");
        submitBtn.textContent = "Enviar Link de Recuperação";
        emailInput.value = "";

        successMessage.style.display = "flex";

        setTimeout(() => {
          successMessage.style.display = "none";
        }, 5000);
      } else {
        submitBtn.textContent = "Erro ao Enviar";
        submitBtn.classList.remove("loading");
        console.error("Erro ao enviar: ", await response.text());
      }
    } catch (err) {
      console.error("Erro de rede:", err);
      submitBtn.textContent = "Erro na Rede";
      submitBtn.classList.remove("loading");
    }
  });

// Função utilitária para obter o CSRF do cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Verifica se o cookie começa com o nome procurado
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Efeitos visuais adicionais (sem alteração)
document.querySelectorAll(".form-control").forEach((input) => {
  input.addEventListener("focus", function () {
    this.parentNode.style.transform = "translateY(-2px)";
  });

  input.addEventListener("blur", function () {
    this.parentNode.style.transform = "translateY(0)";
  });
});

document.querySelector(".btn-submit").addEventListener("click", function (e) {
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
  `;

  this.appendChild(ripple);

  setTimeout(() => {
    ripple.remove();
  }, 600);
});

// CSS da animação
const style = document.createElement("style");
style.textContent = `
  @keyframes rippleEffect {
    to {
      transform: scale(2);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);


document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const loginBtn = document.getElementById("loginBtn");

  if (loginForm && loginBtn) {
    loginForm.addEventListener("submit", function () {
      // Adiciona estado de carregando
      loginBtn.classList.add("loading");
      loginBtn.disabled = true;
      loginBtn.textContent = "Entrando...";

      // Adiciona ripple visual no clique
      const ripple = document.createElement("span");
      const rect = loginBtn.getBoundingClientRect();
      ripple.style.cssText = `
                position: absolute;
                width: 100px;
                height: 100px;
                top: 50%;
                left: 50%;
                background: rgba(255,255,255,0.3);
                border-radius: 50%;
                transform: translate(-50%, -50%) scale(0);
                animation: rippleEffect 0.6s ease-out;
                pointer-events: none;
                z-index: 1;
            `;
      loginBtn.style.position = "relative";
      loginBtn.appendChild(ripple);

      setTimeout(() => ripple.remove(), 600);
    });
  }

  // Ripple animation
  const style = document.createElement("style");
  style.textContent = `
        @keyframes rippleEffect {
            to {
                transform: translate(-50%, -50%) scale(2);
                opacity: 0;
            }
        }
    `;
  document.head.appendChild(style);
});
