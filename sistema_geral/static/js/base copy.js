// Elementos do DOM
const sidebarToggle = document.getElementById("sidebarToggle");
const mobileMenuToggle = document.getElementById("mobileMenuToggle");
const themeToggle = document.getElementById("theme-toggle");
const sidebar = document.getElementById("sidebar");
const headerNav = document.getElementById("headerNav");
const overlay = document.getElementById("overlay");
const themeIcon = document.getElementById("theme-icon");

// Estados
let sidebarOpen = false;
let menuOpen = false;

// Controla o sidebar
function toggleSidebar() {
  if (isMobile()) {
    sidebarOpen = !sidebarOpen;
    sidebar.classList.toggle("active", sidebarOpen);
    overlay.classList.toggle("active", sidebarOpen);
    document.body.style.overflow = sidebarOpen ? "hidden" : "";
  }
}

// Fecha todos os menus
function closeAllMenus() {
  sidebarOpen = false;
  menuOpen = false;

  if (sidebar) sidebar.classList.remove("active");
  if (headerNav) headerNav.classList.remove("active");
  if (overlay) overlay.classList.remove("active");

  document.body.style.overflow = "";
}

// Event Listeners
if (sidebarToggle) sidebarToggle.addEventListener("click", toggleSidebar);

// Fecha ao clicar em links
document
  .querySelectorAll("#headerNav a[href], #sidebar a[href]")
  .forEach((link) => {
    link.addEventListener("click", () => {
      if (isMobile()) closeAllMenus();
    });
  });

document.getElementById("theme-toggle").addEventListener("click", function () {
  const body = document.body;
  const icon = document.getElementById("theme-icon");
  const isDark = body.classList.toggle("dark-mode");
  icon.className = isDark ? "fas fa-moon" : "fas fa-sun";
  document.cookie = `theme=${
    isDark ? "dark-mode" : "light-mode"
  };path=/;max-age=31536000`;
  document.getElementById("theme-stylesheet").href = isDark
    ? '{% static "css/dark-theme.css" %}'
    : '{% static "css/light-theme.css" %}';
});

document.addEventListener("DOMContentLoaded", function () {
  // Fechar mensagens ao clicar no botão ×
  document.querySelectorAll(".close-btn").forEach(function (button) {
    button.addEventListener("click", function () {
      this.parentElement.style.opacity = "0";
      setTimeout(() => {
        this.parentElement.remove();
      }, 300); // Tempo para a animação de fadeOut
    });
  });

  // Fechar mensagens automaticamente após 5 segundos
  document.querySelectorAll(".alert").forEach(function (alert) {
    setTimeout(() => {
      alert.style.opacity = "0";
      setTimeout(() => {
        alert.remove();
      }, 300); // Tempo para a animação de fadeOut
    }, 5000); // 5 segundos
  });
});
