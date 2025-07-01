document.addEventListener("DOMContentLoaded", function () {
  // Menu Toggle (se necessário)
  const menuToggle = document.getElementById("menu-toggle");
  if (menuToggle) {
    const sidebar = document.getElementById("sidebar-container");
    const mainContent = document.querySelector("main");
    menuToggle.addEventListener("click", function () {
      sidebar.classList.toggle("collapsed");
      if (mainContent) {
        mainContent.classList.toggle("full-width");
      }
      document.body.classList.toggle("menu-open");
    });
  }

  // Toggle dos Filtros Avançados
  function toggleFilters() {
    const filtersContent = document.getElementById("filtersContent");
    const filterToggleIcon = document.getElementById("filterToggleIcon");

    if (filtersContent && filterToggleIcon) {
      filtersContent.classList.toggle("show");

      if (filtersContent.classList.contains("show")) {
        filterToggleIcon.classList.remove("fa-chevron-down");
        filterToggleIcon.classList.add("fa-chevron-up");
      } else {
        filterToggleIcon.classList.remove("fa-chevron-up");
        filterToggleIcon.classList.add("fa-chevron-down");
      }
    }
  }

  // Adiciona o evento ao cabeçalho dos filtros
  const filtersHeader = document.querySelector(".filters-header");
  if (filtersHeader) {
    filtersHeader.addEventListener("click", toggleFilters);
  }

  // Filtro de Status
  const statusButtons = document.querySelectorAll(
    ".status-buttons .status-btn"
  );
  const selectedStatusContainer = document.getElementById(
    "selected-status-container"
  );
  const statusInput = document.getElementById("status-input");
  let selectedStatus =
    statusInput && statusInput.value ? statusInput.value.split(",") : [];

  function updateSelectedStatus() {
    if (!selectedStatusContainer) return;

    selectedStatusContainer.innerHTML = "";

    selectedStatus.forEach((status) => {
      const chip = document.createElement("div");
      chip.className =
        "badge bg-primary text-white d-flex align-items-center gap-2 me-2 mb-2";
      chip.innerHTML = `
                <span>${status}</span>
                <button type="button" class="btn-close btn-close-white" aria-label="Remove"></button>
            `;

      chip.querySelector("button").addEventListener("click", () => {
        selectedStatus = selectedStatus.filter((s) => s !== status);
        updateSelectedStatus();
        updateStatusButtons();
      });

      selectedStatusContainer.appendChild(chip);
    });

    if (statusInput) {
      statusInput.value = selectedStatus.join(",");
    }
  }

  function updateStatusButtons() {
    statusButtons.forEach((button) => {
      const status = button.getAttribute("data-status");
      if (selectedStatus.includes(status)) {
        button.classList.add("active");
      } else {
        button.classList.remove("active");
      }
    });
  }

  if (statusButtons.length > 0) {
    statusButtons.forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault();
        const status = this.getAttribute("data-status");

        if (selectedStatus.includes(status)) {
          selectedStatus = selectedStatus.filter((s) => s !== status);
        } else {
          selectedStatus.push(status);
        }

        updateSelectedStatus();
        updateStatusButtons();
      });
    });

    // Inicializa os botões de status
    updateStatusButtons();
  }

  // Ordenação
  function changeSort(sortOption) {
    const url = new URL(window.location.href);
    url.searchParams.set("sort", sortOption);
    window.location.href = url.toString();
  }

  // Exportação (exemplo - implementação real depende do backend)
  function exportToExcel() {
    const url = new URL(window.location.href);
    url.searchParams.set("export", "excel");
    window.location.href = url.toString();
  }

  function exportToPDF() {
    const url = new URL(window.location.href);
    url.searchParams.set("export", "pdf");
    window.location.href = url.toString();
  }

  // Adiciona eventos aos botões de ordenação e exportação
  document.querySelectorAll('[onclick^="changeSort"]').forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const sortOption = this.getAttribute("onclick").match(/'([^']+)'/)[1];
      changeSort(sortOption);
    });
  });

  document.querySelectorAll('[onclick^="exportTo"]').forEach((btn) => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const exportType = this.getAttribute("onclick")
        .match(/(Excel|PDF)/)[0]
        .toLowerCase();
      if (exportType === "excel") {
        exportToExcel();
      } else {
        exportToPDF();
      }
    });
  });

  // AJAX para atualização dos chamados (se necessário)
  const menuLinks = document.querySelectorAll(".menu-filter");
  if (menuLinks.length > 0) {
    menuLinks.forEach((link) => {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        const action = this.getAttribute("data-action");

        fetch(`/chamados/${action}/`, {
          method: "GET",
          headers: { "X-Requested-With": "XMLHttpRequest" },
        })
          .then((response) => response.json())
          .then((data) => {
            document.getElementById("serviceCards").innerHTML = data.html;

            const sidebar = document.getElementById("sidebar-container");
            if (
              sidebar &&
              !sidebar.classList.contains("collapsed") &&
              window.innerWidth < 992
            ) {
              sidebar.classList.add("collapsed");
              document.body.classList.remove("menu-open");
            }
          })
          .catch((error) =>
            console.error("Erro ao carregar os chamados:", error)
          );
      });
    });
  }
});
