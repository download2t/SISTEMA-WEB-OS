document.addEventListener("DOMContentLoaded", function () {
  // --- ELEMENTS ---
  const filtersHeader = document.getElementById("filtersHeader");
  const filtersContent = document.getElementById("filtersContent");
  const filterToggleIcon = document.getElementById("filterToggleIcon");
  const sidebarToggle = document.getElementById("sidebarToggle");
  const sidebar = document.querySelector(".sidebar"); // Assuming your sidebar has this class
  const mainContent = document.querySelector(".main-content-wrapper");

  // --- FILTER TOGGLE LOGIC ---
  function toggleFilters() {
    if (filtersContent && filtersHeader) {
      const isCollapsed = filtersContent.classList.contains("show");
      if (isCollapsed) {
        filtersContent.classList.remove("show");
        filtersHeader.classList.add("collapsed");
      } else {
        filtersContent.classList.add("show");
        filtersHeader.classList.remove("collapsed");
      }
    }
  }

  // Set initial state of filters based on screen size
  function initializeFilters() {
    if (window.innerWidth < 992) {
      // Start collapsed on mobile/tablet
      filtersContent.classList.remove("show");
      filtersHeader.classList.add("collapsed");
    } else {
      // Start open on desktop
      filtersContent.classList.add("show");
      filtersHeader.classList.remove("collapsed");
    }
  }

  if (filtersHeader) {
    filtersHeader.addEventListener("click", toggleFilters);
    initializeFilters(); // Set initial state on load
  }

  // --- SIDEBAR TOGGLE LOGIC ---
  if (sidebarToggle && sidebar && mainContent) {
    sidebarToggle.addEventListener("click", () => {
      sidebar.classList.toggle("collapsed");
      mainContent.classList.toggle("collapsed"); // You might need CSS for this class
    });
  }

  // Function to apply formatting to all phone fields
  function applyPhoneNumberFormatting() {
    const phoneFields = document.querySelectorAll(".telefone");
    phoneFields.forEach((field) => {
      // For table cells, we format the text content directly
      if (field.tagName === "TD") {
        formatPhoneNumber(field); // Pass the TD element directly
      }
      else if (field.tagName === "INPUT") {
        field.addEventListener("input", (e) => {
          formatPhoneNumber(e.target);
        });
      }
    });
  }

  applyPhoneNumberFormatting();

});
