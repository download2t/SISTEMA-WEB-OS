document.addEventListener("DOMContentLoaded", function () {
  function formatarTelefone(numero) {
    let apenasNumeros = numero.replace(/\D/g, "");
    if (apenasNumeros.length === 10) {
      return `(${apenasNumeros.substring(0, 2)}) ${apenasNumeros.substring(
        2,
        6
      )}-${apenasNumeros.substring(6)}`;
    } else if (apenasNumeros.length === 11) {
      return `(${apenasNumeros.substring(0, 2)}) ${apenasNumeros.substring(
        2,
        7
      )}-${apenasNumeros.substring(7)}`;
    } else if (apenasNumeros.length === 8) {
      return `${apenasNumeros.substring(0, 4)}-${apenasNumeros.substring(4)}`;
    } else if (apenasNumeros.length === 9) {
      return `${apenasNumeros.substring(0, 5)}-${apenasNumeros.substring(5)}`;
    }
    return numero;
  }

  document.querySelectorAll(".telefone").forEach((td) => {
    if (td.textContent.trim()) {
      td.textContent = formatarTelefone(td.textContent.trim());
    }
  });

  // Sidebar Toggle Logic (should ideally be in base.js or a common script)
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebar-toggle-btn");
  const sidebarOverlay = document.getElementById("sidebar-overlay");

  if (sidebarToggle && sidebar && sidebarOverlay) {
    sidebarToggle.addEventListener("click", function () {
      sidebar.classList.toggle("active");
      sidebarOverlay.classList.toggle("active");
      document.body.classList.toggle("no-scroll");
    });

    sidebarOverlay.addEventListener("click", function () {
      sidebar.classList.remove("active");
      sidebarOverlay.classList.remove("active");
      document.body.classList.remove("no-scroll");
    });
  }

  // Toggle Filters Logic - COPIADO DO listar_chamados.js
  const filtersContent = document.getElementById("filtersContent");
  const filterToggleIcon = document.getElementById("filterToggleIcon");

  // Initialize filter state
  // If you want the filters to be collapsed by default, add 'd-none' to filtersContent in HTML
  // Otherwise, they will be open by default.
  if (filtersContent) {
    // Check if there are any active filters from the URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    let hasFilters = false;
    for (const [key, value] of urlParams.entries()) {
      if (value && key !== "page") {
        // Ignore empty values and pagination
        hasFilters = true;
        break;
      }
    }

    // If there are no filters, collapse by default
    if (!hasFilters) {
      filtersContent.classList.add("d-none"); // Hide filter content
      if (filterToggleIcon) {
        filterToggleIcon.classList.remove("fa-chevron-down");
        filterToggleIcon.classList.add("fa-chevron-up");
      }
    } else {
      // If filters are present, ensure content is visible and icon is correct
      filtersContent.classList.remove("d-none");
      if (filterToggleIcon) {
        filterToggleIcon.classList.remove("fa-chevron-up");
        filterToggleIcon.classList.add("fa-chevron-down");
      }
    }
  }

  window.toggleFilters = function () {
    if (filtersContent) {
      filtersContent.classList.toggle("d-none");
      if (filterToggleIcon) {
        if (filtersContent.classList.contains("d-none")) {
          filterToggleIcon.classList.remove("fa-chevron-down");
          filterToggleIcon.classList.add("fa-chevron-up");
        } else {
          filterToggleIcon.classList.remove("fa-chevron-up");
          filterToggleIcon.classList.add("fa-chevron-down");
        }
      }
    }
  };
});
