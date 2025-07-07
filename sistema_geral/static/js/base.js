// static/js/base.js

document.addEventListener("DOMContentLoaded", function () {
  // --- DOM Elements (Consolidated) ---
  const body = document.body;
  const sidebarToggle = document.getElementById("sidebarToggle");
  // const mobileMenuToggle = document.getElementById("mobileMenuToggle"); // Not found in your base.html, keeping commented
  const themeToggleBtn = document.getElementById("theme-toggle"); // Renamed for clarity
  const themeIcon = document.getElementById("theme-icon");
  const sidebar = document.getElementById("sidebar"); // Assuming #sidebar exists for your sidebar logic
  const sidebarOverlay = document.getElementById("sidebarOverlay"); // Renamed overlay for clarity with sidebar
  // const headerNav = document.getElementById("headerNav"); // If this is your main navbar collapse, it's #navbarNav in your base.html

  // --- State Variables (kept from old code) ---
  let sidebarOpen = false;
  // let menuOpen = false; // Not explicitly used with mobileMenuToggle in provided snippets

  // --- Helper Function (from old code, assuming it exists elsewhere or needs to be defined) ---
  function isMobile() {
    // You need to define this function based on your criteria (e.g., screen width)
    // Example: return window.innerWidth <= 992; // Bootstrap's 'lg' breakpoint
    return window.matchMedia("(max-width: 991.98px)").matches;
  }

  // --- Sidebar Control (from old code) ---
  function toggleSidebar() {
    // Ensure sidebar and overlay exist before attempting to toggle
    if (sidebar && sidebarOverlay) {
      // Your original logic for mobile
      if (isMobile()) {
        sidebarOpen = !sidebarOpen;
        sidebar.classList.toggle("active", sidebarOpen);
        sidebarOverlay.classList.toggle("active", sidebarOpen);
        document.body.style.overflow = sidebarOpen ? "hidden" : "";
      }
      // If you also have a desktop sidebar toggle, you might add logic here
      // For now, it only triggers on mobile based on your old code
    }
  }

  // --- Close All Menus (from old code, adapted) ---
  function closeAllMenus() {
    sidebarOpen = false;
    // menuOpen = false; // Not explicitly used

    if (sidebar) sidebar.classList.remove("active");
    // if (headerNav) headerNav.classList.remove("active"); // Adapt if #navbarNav is what you mean
    if (sidebarOverlay) sidebarOverlay.classList.remove("active"); // Use sidebarOverlay

    document.body.style.overflow = "";
  }

  // --- Light/Dark Theme Toggling (Combined New & Old Logic, using localStorage) ---
  function setLightDarkMode(mode) {
    body.classList.remove("light-mode", "dark-mode");
    body.classList.add(mode);
    localStorage.setItem("selected-color-mode", mode); // Persist using localStorage

    // Update icon based on mode
    if (themeIcon) {
      themeIcon.className = mode === "dark-mode" ? "fas fa-moon" : "fas fa-sun";
    }

    // Removed: document.cookie logic for theme and switching CSS files,
    // as we are now using CSS variables and localStorage for persistence.
  }

  // Load saved light/dark mode preference on initial page load
  const savedColorMode = localStorage.getItem("selected-color-mode");
  if (savedColorMode) {
    setLightDarkMode(savedColorMode);
  } else {
    // Default to light-mode if no preference is found
    setLightDarkMode("light-mode");
  }

  // Event Listener for Light/Dark Toggle Button
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", function () {
      if (body.classList.contains("light-mode")) {
        setLightDarkMode("dark-mode");
      } else {
        setLightDarkMode("light-mode");
      }
    });
  }

  // --- Dynamic Color Theme Selection ---
  const colorThemeButtons = document.querySelectorAll("[data-theme]");

  // Define all possible theme classes
  const allThemeClasses = [
    "theme-default",
    "theme-modern-blue",
    "theme-muted-green",
    "theme-cool-grey",
    "theme-classic-brown",
    "theme-emerald-forest",
    "theme-ocean-breeze",
    "theme-royal-purple",
    "theme-sunset-orange",
    "theme-midnight-blue",
    "theme-forest-green",
    "theme-deep-red",
    "theme-sunny-yellow",
    "theme-aqua-blue",
    "theme-charcoal-grey",
  ];

  function applyColorScheme(themeName) {
    // Remove all existing color theme classes from body
    allThemeClasses.forEach((themeClass) => {
      body.classList.remove(themeClass);
    });

    // Add the selected theme class
    body.classList.add(themeName);
    // Save the chosen color scheme to local storage
    localStorage.setItem("selected-color-scheme", themeName);
  }

  // Event listeners for color theme buttons
  colorThemeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const themeName = this.dataset.theme;
      applyColorScheme(themeName);
    });
  });

  // Apply saved color scheme on page load
  const savedColorScheme = localStorage.getItem("selected-color-scheme");
  if (savedColorScheme && allThemeClasses.includes(savedColorScheme)) {
    // Validate saved theme
    applyColorScheme(savedColorScheme);
  } else {
    // Set a default color theme if none is saved or if saved theme is invalid
    applyColorScheme("theme-default");
  }

  // --- Event Listeners from Old Code ---
  // Sidebar Toggle
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", toggleSidebar);
  }

  // Close sidebar/menus when clicking overlay
  if (sidebarOverlay) {
    sidebarOverlay.addEventListener("click", closeAllMenus);
  }

  // Close on link click (for both sidebar and potentially navbar)
  document
    .querySelectorAll("#sidebar a[href], .navbar-nav a[href]")
    .forEach((link) => {
      // Adjusted selector for navbar
      link.addEventListener("click", () => {
        if (isMobile()) closeAllMenus();
      });
    });

  // --- Message Dismissal (from old code) ---
  // Close messages on "×" button click
  document
    .querySelectorAll(".messages-container .close-btn")
    .forEach(function (button) {
      button.addEventListener("click", function () {
        this.closest(".alert").style.opacity = "0"; // Use closest for robustness
        setTimeout(() => {
          this.closest(".alert").remove();
        }, 300);
      });
    });

  // Auto-dismiss messages after 5 seconds
  document
    .querySelectorAll(".messages-container .alert")
    .forEach(function (alert) {
      setTimeout(() => {
        alert.style.opacity = "0";
        setTimeout(() => {
          alert.remove();
        }, 300);
      }, 5000);
    });
});
