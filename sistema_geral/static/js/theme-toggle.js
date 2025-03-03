// static/js/theme-toggle.js

document.addEventListener("DOMContentLoaded", function () {
  const themeToggleBtn = document.getElementById("theme-toggle");
  const themeIcon = document.getElementById("theme-icon");
  const themeStylesheet = document.getElementById("theme-stylesheet");
  const body = document.body;

  // Verificar a preferência do usuário no localStorage
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    body.classList.remove("light-mode");
    body.classList.add("dark-mode");
    themeStylesheet.setAttribute("href", "/static/css/dark-theme.css");
    themeIcon.classList.remove("fa-sun");
    themeIcon.classList.add("fa-moon");
  }

  // Alternar entre os temas quando o botão for clicado
  themeToggleBtn.addEventListener("click", function () {
    if (body.classList.contains("light-mode")) {
      body.classList.remove("light-mode");
      body.classList.add("dark-mode");
      themeStylesheet.setAttribute("href", "/static/css/dark-theme.css");
      themeIcon.classList.remove("fa-sun");
      themeIcon.classList.add("fa-moon");
      localStorage.setItem("theme", "dark"); // Salvar a preferência no localStorage
    } else {
      body.classList.remove("dark-mode");
      body.classList.add("light-mode");
      themeStylesheet.setAttribute("href", "/static/css/light-theme.css");
      themeIcon.classList.remove("fa-moon");
      themeIcon.classList.add("fa-sun");
      localStorage.setItem("theme", "light"); // Salvar a preferência no localStorage
    }
  });
});
