document.addEventListener("DOMContentLoaded", function () {

  // --- Lógica do Toggle de Filtros ---
  const filtersContent = document.getElementById("filters-content");
  const filterToggleText = document.getElementById("filter-toggle-text");
  const toggleFiltersButton = document.querySelector(".toggle-filters"); // Seleciona o botão de toggle

  if (toggleFiltersButton && filtersContent && filterToggleText) {
    // Inicializa o texto do botão com base no estado inicial do filtro (se hidden por CSS)
    // Isso assume que 'hidden' é definida no CSS para o estado padrão oculto,
    // ou você pode definir um estado inicial aqui.
    if (filtersContent.classList.contains("hidden")) {
      filterToggleText.textContent = "Mostrar Filtros";
    } else {
      filterToggleText.textContent = "Ocultar Filtros";
    }

    toggleFiltersButton.addEventListener("click", function () {
      filtersContent.classList.toggle("hidden"); // Alterna a classe 'hidden'
      if (filtersContent.classList.contains("hidden")) {
        filterToggleText.textContent = "Mostrar Filtros";
      } else {
        filterToggleText.textContent = "Ocultar Filtros";
      }
    });
  }

  // --- Lógica do Botão "Concluir" com confirmação ---
  const completeButtons = document.querySelectorAll(".confirm-complete");

  completeButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault(); // Impede o envio padrão do formulário

      const appointmentName = this.dataset.appointmentName;
      const appointmentDate = this.dataset.appointmentDate;
      const appointmentTime = this.dataset.appointmentTime;

      const confirmation = confirm(
        `Tem certeza que deseja CONCLUIR o serviço de ${appointmentName} ` +
          `agendado para ${appointmentDate} às ${appointmentTime}?`
      );

      if (confirmation) {
        this.closest("form").submit(); // Envia o formulário se confirmado
      }
    });
  });

  // --- Lógica para Validação de Datas no Filtro ---
  const dataInicioInput = document.getElementById("data_inicio");
  const dataFimInput = document.getElementById("data_fim");
  const filtrosForm = document.querySelector(".filters-form"); // Seleciona o formulário de filtros pela classe ou ID

  if (dataInicioInput && dataFimInput) {
    dataInicioInput.addEventListener("change", function () {
      if (this.value) {
        dataFimInput.min = this.value; // Garante que data_fim não seja anterior a data_inicio
        // Se data_fim atual for menor que nova data_inicio, reseta data_fim
        if (dataFimInput.value && dataFimInput.value < this.value) {
          dataFimInput.value = this.value;
        }
      } else {
        // Se data_inicio for limpa, remove a restrição de min da data_fim
        dataFimInput.removeAttribute("min");
      }
    });
  }

  // --- Manter Estado dos Filtros após recarregar (opcional, se não for handled pelo Django) ---
  // Se o Django já preenche os campos com request.GET.nome etc., esta parte é menos crítica.
  // Se você usa o sessionStorage para persistir o estado de exibição do filtro:
  const filtersHiddenState = sessionStorage.getItem("filtersHidden");
  if (filtersHiddenState === "true") {
    filtersContent.classList.add("hidden");
    filterToggleText.textContent = "Mostrar Filtros";
  } else {
    filtersContent.classList.remove("hidden");
    filterToggleText.textContent = "Ocultar Filtros";
  }

  if (toggleFiltersButton) {
    toggleFiltersButton.addEventListener("click", function () {
      // Salva o estado atual no sessionStorage
      sessionStorage.setItem(
        "filtersHidden",
        filtersContent.classList.contains("hidden")
      );
    });
  }
});

