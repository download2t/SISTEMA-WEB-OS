document.addEventListener("DOMContentLoaded", function () {
  const toggleFiltersBtn = document.getElementById("toggle-filters");
  const filterOptions = document.getElementById("filter-options");
  const statusOptionsContainer = document.getElementById("status-options");
  const selectedStatusContainer = document.getElementById(
    "selected-status-container"
  );
  const statusInput = document.getElementById("status-input");
  const filterToggleIcon = toggleFiltersBtn.querySelector(
    ".filter-toggle-icon"
  );

  // --- Filter Toggle Logic ---
  // Initialize filter options visibility based on current URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.toString() !== "") {
    filterOptions.classList.remove("d-none");
    toggleFiltersBtn.classList.add("active");
  }

  toggleFiltersBtn.addEventListener("click", function () {
    filterOptions.classList.toggle("d-none");
    this.classList.toggle("active");
  });

  // --- Status Filter Logic ---
  let selectedStatuses = statusInput.value ? statusInput.value.split(",") : [];

  function updateStatusInput() {
    statusInput.value = selectedStatuses.join(",");
  }

  function renderSelectedStatuses() {
    selectedStatusContainer.innerHTML = ""; // Clear existing tags

    if (selectedStatuses.length === 0) {
      // If no statuses are selected, ensure all buttons are unselected
      document.querySelectorAll(".status-option").forEach((button) => {
        button.classList.remove("selected");
      });
      return;
    }

    selectedStatuses.forEach((status) => {
      const statusTag = document.createElement("span");
      statusTag.classList.add("selected-status-tag");
      statusTag.innerHTML = `
                ${status} <button type="button" class="remove-tag-btn" data-value="${status}"><i class="fas fa-times"></i></button>
            `;
      selectedStatusContainer.appendChild(statusTag);

      // Mark the corresponding button as selected
      const correspondingButton = document.querySelector(
        `.status-option[data-value="${status}"]`
      );
      if (correspondingButton) {
        correspondingButton.classList.add("selected");
      }
    });
  }

  // Handle clicks on status option buttons
  statusOptionsContainer.addEventListener("click", function (event) {
    if (event.target.classList.contains("status-option")) {
      const value = event.target.dataset.value;
      const index = selectedStatuses.indexOf(value);

      if (index > -1) {
        // If already selected, remove it
        selectedStatuses.splice(index, 1);
        event.target.classList.remove("selected");
      } else {
        // If not selected, add it
        selectedStatuses.push(value);
        event.target.classList.add("selected");
      }
      updateStatusInput();
      renderSelectedStatuses();
    }
  });

  // Handle clicks on remove tag buttons
  selectedStatusContainer.addEventListener("click", function (event) {
    if (
      event.target.classList.contains("remove-tag-btn") ||
      event.target.closest(".remove-tag-btn")
    ) {
      const button = event.target.closest(".remove-tag-btn");
      const valueToRemove = button.dataset.value;
      selectedStatuses = selectedStatuses.filter(
        (status) => status !== valueToRemove
      );

      // Remove 'selected' class from the original status button
      const correspondingButton = document.querySelector(
        `.status-option[data-value="${valueToRemove}"]`
      );
      if (correspondingButton) {
        correspondingButton.classList.remove("selected");
      }

      updateStatusInput();
      renderSelectedStatuses();
    }
  });

  // Initial render of selected statuses on page load
  renderSelectedStatuses();
});
