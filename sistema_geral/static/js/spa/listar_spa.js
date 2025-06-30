function toggleFilters() {
  const filtersContent = document.getElementById("filters-content");
  const toggleText = document.getElementById("filter-toggle-text");

  if (filtersContent.style.display === "none") {
    filtersContent.style.display = "block";
    toggleText.textContent = "Ocultar Filtros";
  } else {
    filtersContent.style.display = "none";
    toggleText.textContent = "Mostrar Filtros";
  }
}


document.addEventListener("DOMContentLoaded", function () {
  // Manter o estado dos filtros
  const form = document.getElementById("filtros-form");

  // Botão Limpar
  document
    .querySelector(".btn-secondary")
    .addEventListener("click", function () {
      // Resetar todos os campos
      form.reset();
      // Remover parâmetros da URL
      window.location.href = "{% url 'listar_spa' %}";
    });

  // Relação entre datas
  document
    .getElementById("data_inicio")
    .addEventListener("change", function () {
      if (this.value) {
        document.getElementById("data_fim").min = this.value;
      }
    });
});