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

  // --- PHONE NUMBER MASKING (UX Improvement) ---
  function formatPhoneNumber(input) {
    // Strips all non-numeric characters from the input
    let numericInput = input.value.replace(/\D/g, "");

    // Apply mask based on length
    if (numericInput.length > 10) {
      // (XX) XXXXX-XXXX for cell phones
      numericInput = numericInput.replace(
        /^(\d\d)(\d{5})(\d{4}).*/,
        "($1) $2-$3"
      );
    } else if (numericInput.length > 6) {
      // (XX) XXXX-XXXX for landlines
      numericInput = numericInput.replace(
        /^(\d\d)(\d{4})(\d{0,4}).*/,
        "($1) $2-$3"
      );
    } else if (numericInput.length > 2) {
      numericInput = numericInput.replace(/^(\d\d)(\d{0,5}).*/, "($1) $2");
    } else {
      numericInput = numericInput.replace(/^(\d*)/, "($1");
    }
    input.value = numericInput;
  }

  // Apply the mask to all elements with the class 'telefone'
  const phoneFields = document.querySelectorAll(".telefone");
  phoneFields.forEach((field) => {
    // For table cells, we format the text content directly
    if (field.tagName === "TD") {
      const tempInput = document.createElement("input");
      tempInput.value = field.textContent;
      formatPhoneNumber(tempInput);
      field.textContent = tempInput.value;
    }
    // If it's an actual input field, add an event listener
    else if (field.tagName === "INPUT") {
      field.addEventListener("input", (e) => {
        formatPhoneNumber(e.target);
      });
    }
  });
});
