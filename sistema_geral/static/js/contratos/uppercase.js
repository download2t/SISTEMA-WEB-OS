
document.addEventListener("DOMContentLoaded", function () {
  const uppercaseFields = [
    document.getElementById("id_razao_social"),
    document.getElementById("id_nome_fantasia"),
    document.getElementById("id_descricao"),
  ];

  uppercaseFields.forEach((field) => {
    if (field) {
      field.addEventListener("input", function () {
        this.value = this.value.toUpperCase();
      });
    }
  });
});
