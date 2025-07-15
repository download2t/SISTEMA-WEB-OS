document.addEventListener("DOMContentLoaded", function () {
  // Máscara para CNPJ/CPF
  const documentoInput = document.getElementById("id_documento");
  if (documentoInput) {
    documentoInput.addEventListener("input", function () {
      this.value = this.value.replace(/\D/g, "");

      // Aplica máscara de CPF ou CNPJ conforme o tamanho
      if (this.value.length <= 11) {
        this.value = this.value.replace(/(\d{3})(\d)/, "$1.$2");
        this.value = this.value.replace(/(\d{3})(\d)/, "$1.$2");
        this.value = this.value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
      } else {
        this.value = this.value.replace(/^(\d{2})(\d)/, "$1.$2");
        this.value = this.value.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
        this.value = this.value.replace(/\.(\d{3})(\d)/, ".$1/$2");
        this.value = this.value.replace(/(\d{4})(\d)/, "$1-$2");
      }
    });
  }

  // Máscara para telefone
  const telefoneInput = document.getElementById("id_telefone");
  if (telefoneInput) {
    telefoneInput.addEventListener("input", function () {
      this.value = this.value.replace(/\D/g, "");

      if (this.value.length > 11) {
        this.value = this.value.substring(0, 11);
      }

      // Aplica máscara (00) 00000-0000
      if (this.value.length > 10) {
        this.value = this.value.replace(
          /^(\d{2})(\d{5})(\d{4})$/,
          "($1) $2-$3"
        );
      } else if (this.value.length > 6) {
        this.value = this.value.replace(
          /^(\d{2})(\d{4})(\d{0,4})$/,
          "($1) $2-$3"
        );
      } else if (this.value.length > 2) {
        this.value = this.value.replace(/^(\d{2})(\d{0,5})$/, "($1) $2");
      } else if (this.value.length > 0) {
        this.value = this.value.replace(/^(\d{0,2})$/, "($1");
      }
    });
  }

  // Máscara para valor monetário
  const valorInput = document.getElementById("id_valor");
  if (valorInput) {
    valorInput.addEventListener("input", function () {
      this.value = this.value.replace(/\D/g, "");

      if (this.value.length === 0) {
        this.value = "";
        return;
      }

      // Formata como valor monetário (0,00)
      const valor = parseInt(this.value) / 100;
      this.value = valor.toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
    });
  }
});
