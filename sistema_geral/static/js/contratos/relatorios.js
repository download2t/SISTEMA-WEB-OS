// Relatórios JavaScript Moderno

class RelatoriosManager {
  constructor() {
    this.initializeElements();
    this.bindEvents();
    this.setupFilters();
  }

  initializeElements() {
    this.filterToggle = document.getElementById("toggle-filters");
    this.filtersSection = document.querySelector(".filters-section");
    this.tableContainer = document.querySelector(".table-container");
    this.table = document.querySelector(".modern-table");
    this.filterInputs = {
      razaoSocial: document.querySelector('input[name="razao_social"]'),
      grupo: document.querySelector('select[name="grupo"]'),
      dataInicio: document.querySelector('input[name="data_inicio"]'),
    };
  }

  bindEvents() {
    // Toggle dos filtros
    this.filterToggle?.addEventListener("click", () => this.toggleFilters());

    // Filtros em tempo real
    Object.values(this.filterInputs).forEach((input) => {
      if (input) {
        input.addEventListener("input", () =>
          this.debounce(this.applyFilters.bind(this), 300)()
        );
      }
    });

    // Botões de ação
    document
      .querySelector(".btn-apply")
      ?.addEventListener("click", () => this.applyFilters());
    document
      .querySelector(".btn-clear")
      ?.addEventListener("click", () => this.clearFilters());

    // Responsividade da sidebar
    this.handleSidebarToggle();
  }

  setupFilters() {
    // Criar os elementos dos filtros se não existirem
    if (!this.filtersSection) {
      this.createFiltersSection();
    }

    // Inicializar valores dos filtros
    this.loadFilterValues();
  }

  createFiltersSection() {
    const filtersHTML = `
            <div class="filters-section" id="filter-options">
                <div class="filters-grid">
                    <div class="filter-group">
                        <label class="filter-label">Razão Social</label>
                        <input type="text" name="razao_social" class="filter-input" placeholder="Digite a razão social...">
                    </div>
                    <div class="filter-group">
                        <label class="filter-label">Grupo</label>
                        <select name="grupo" class="filter-select">
                            <option value="">Todos os grupos</option>
                            <!-- Opções serão carregadas dinamicamente -->
                        </select>
                    </div>
                    <div class="filter-group">
                        <label class="filter-label">Data Início</label>
                        <input type="date" name="data_inicio" class="filter-input">
                    </div>
                    <div class="filter-group">
                        <label class="filter-label">Data Fim</label>
                        <input type="date" name="data_fim" class="filter-input">
                    </div>
                    <div class="filter-group">
                        <label class="filter-label">Status</label>
                        <select name="status" class="filter-select">
                            <option value="">Todos</option>
                            <option value="ativo">Ativo</option>
                            <option value="inativo">Inativo</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label class="filter-label">Valor Mínimo</label>
                        <input type="number" name="valor_min" class="filter-input" placeholder="0,00" step="0.01">
                    </div>
                </div>
                <div class="filter-actions">
                    <button type="button" class="btn-clear">
                        <i class="fas fa-times"></i> Limpar
                    </button>
                    <button type="button" class="btn-apply">
                        <i class="fas fa-check"></i> Aplicar
                    </button>
                </div>
            </div>
        `;

    // Inserir após o botão de filtros
    this.filterToggle.insertAdjacentHTML("afterend", filtersHTML);
    this.filtersSection = document.querySelector(".filters-section");
    this.initializeElements(); // Reinicializar elementos
  }

  toggleFilters() {
    if (!this.filtersSection) return;

    const isVisible = this.filtersSection.classList.contains("show");

    if (isVisible) {
      this.filtersSection.classList.remove("show");
      this.filterToggle.innerHTML =
        '<i class="fas fa-filter"></i> Filtrar Relatórios';
      this.filterToggle.setAttribute("aria-expanded", "false");
    } else {
      this.filtersSection.classList.add("show");
      this.filterToggle.innerHTML =
        '<i class="fas fa-filter-circle-xmark"></i> Ocultar Filtros';
      this.filterToggle.setAttribute("aria-expanded", "true");
    }
  }

  applyFilters() {
    if (!this.table) return;

    const filters = this.getFilterValues();
    const rows = this.table.querySelectorAll("tbody tr");
    let visibleCount = 0;

    rows.forEach((row) => {
      if (row.querySelector("td[colspan]")) return; // Pular linha "nenhum contrato"

      const isVisible = this.matchesFilters(row, filters);
      row.style.display = isVisible ? "" : "none";

      if (isVisible) {
        visibleCount++;
      }
    });

    // Atualizar contador
    this.updateTableInfo(visibleCount);

    // Mostrar/ocultar mensagem de "nenhum resultado"
    this.toggleEmptyState(visibleCount === 0);
  }

  matchesFilters(row, filters) {
    const cells = row.querySelectorAll("td");

    // Extrair dados da linha
    const rowData = {
      razaoSocial: cells[0]?.textContent.toLowerCase() || "",
      nomeFantasia: cells[1]?.textContent.toLowerCase() || "",
      documento: cells[2]?.textContent || "",
      telefone: cells[3]?.textContent || "",
      email: cells[4]?.textContent.toLowerCase() || "",
      dataAssinatura: cells[5]?.textContent || "",
      dataValidade: cells[6]?.textContent || "",
      grupo: cells[7]?.textContent.toLowerCase() || "",
      valor: this.parseValue(cells[8]?.textContent || "0"),
      status: cells[9]?.textContent.toLowerCase().includes("sim")
        ? "ativo"
        : "inativo",
    };

    // Aplicar filtros
    if (
      filters.razaoSocial &&
      !rowData.razaoSocial.includes(filters.razaoSocial.toLowerCase())
    ) {
      return false;
    }

    if (filters.grupo && !rowData.grupo.includes(filters.grupo.toLowerCase())) {
      return false;
    }

    if (filters.status && rowData.status !== filters.status) {
      return false;
    }

    if (filters.valorMin && rowData.valor < filters.valorMin) {
      return false;
    }

    if (
      filters.dataInicio &&
      !this.isDateAfter(rowData.dataAssinatura, filters.dataInicio)
    ) {
      return false;
    }

    if (
      filters.dataFim &&
      !this.isDateBefore(rowData.dataAssinatura, filters.dataFim)
    ) {
      return false;
    }

    return true;
  }

  getFilterValues() {
    return {
      razaoSocial: this.filterInputs.razaoSocial?.value || "",
      grupo: this.filterInputs.grupo?.value || "",
      dataInicio: this.filterInputs.dataInicio?.value || "",
      dataFim: document.querySelector('input[name="data_fim"]')?.value || "",
      status: document.querySelector('select[name="status"]')?.value || "",
      valorMin: parseFloat(
        document.querySelector('input[name="valor_min"]')?.value || "0"
      ),
    };
  }

  clearFilters() {
    // Limpar todos os inputs
    Object.values(this.filterInputs).forEach((input) => {
      if (input) {
        input.value = "";
      }
    });

    // Limpar filtros adicionais
    const additionalFilters = document.querySelectorAll(
      'input[name="data_fim"], select[name="status"], input[name="valor_min"]'
    );
    additionalFilters.forEach((input) => {
      input.value = "";
    });

    // Reaplicar filtros (vai mostrar todos)
    this.applyFilters();
  }

  loadFilterValues() {
    // Carregar grupos únicos da tabela
    const grupoSelect = document.querySelector('select[name="grupo"]');
    if (grupoSelect && this.table) {
      const grupos = new Set();
      const rows = this.table.querySelectorAll("tbody tr");

      rows.forEach((row) => {
        const grupoCell = row.querySelector("td:nth-child(8)");
        if (grupoCell && !row.querySelector("td[colspan]")) {
          grupos.add(grupoCell.textContent.trim());
        }
      });

      // Adicionar opções ao select
      grupos.forEach((grupo) => {
        const option = document.createElement("option");
        option.value = grupo;
        option.textContent = grupo;
        grupoSelect.appendChild(option);
      });
    }
  }

  updateTableInfo(count) {
    let infoElement = document.querySelector(".table-info");
    if (!infoElement) {
      const header = document.querySelector(".table-header");
      if (header) {
        infoElement = document.createElement("div");
        infoElement.className = "table-info";
        header.appendChild(infoElement);
      }
    }

    if (infoElement) {
      infoElement.textContent = `${count} contrato${
        count !== 1 ? "s" : ""
      } encontrado${count !== 1 ? "s" : ""}`;
    }
  }

  toggleEmptyState(show) {
    let emptyState = document.querySelector(".empty-state");

    if (show && !emptyState) {
      emptyState = document.createElement("div");
      emptyState.className = "empty-state";
      emptyState.innerHTML = `
                <i class="fas fa-search"></i>
                <h3>Nenhum resultado encontrado</h3>
                <p>Tente ajustar os filtros para encontrar o que você procura.</p>
            `;
      this.table.style.display = "none";
      this.tableContainer.appendChild(emptyState);
    } else if (!show && emptyState) {
      emptyState.remove();
      this.table.style.display = "";
    }
  }

  handleSidebarToggle() {
    const sidebarToggle = document.getElementById("sidebarToggle");
    const mainContent = document.querySelector(".main-content-wrapper");

    if (sidebarToggle && mainContent) {
      sidebarToggle.addEventListener("click", () => {
        document.body.classList.toggle("sidebar-collapsed");
      });
    }
  }

  // Utilitários
  parseValue(valueString) {
    return (
      parseFloat(valueString.replace(/[^\d,.-]/g, "").replace(",", ".")) || 0
    );
  }

  isDateAfter(dateString, compareDate) {
    const date = this.parseDate(dateString);
    const compare = new Date(compareDate);
    return date >= compare;
  }

  isDateBefore(dateString, compareDate) {
    const date = this.parseDate(dateString);
    const compare = new Date(compareDate);
    return date <= compare;
  }

  parseDate(dateString) {
    // Assumindo formato dd/mm/yyyy
    const parts = dateString.split("/");
    if (parts.length === 3) {
      return new Date(parts[2], parts[1] - 1, parts[0]);
    }
    return new Date(dateString);
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener("DOMContentLoaded", () => {
  new RelatoriosManager();
});

// Utilitários globais para formatação
window.formatCurrency = (value) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
};

window.formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("pt-BR");
};
