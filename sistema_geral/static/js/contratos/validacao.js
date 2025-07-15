// static/js/contratos/validacao.js

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contractForm");
  
  const fileInput = document.getElementById("id_arquivo_contrato");
  const maxUploadMb = parseFloat("{{ max_upload_mb }}"); // Passe max_upload_mb do contexto para o JS
  const maxSizeBytes = maxUploadMb * 1024 * 1024;
  const allowedTypes = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/jpeg",
    "image/png",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  ];

  
  if (fileInput) {
    fileInput.addEventListener("change", function (event) {
      const file = event.target.files[0];
      const fileUploadText = document.querySelector(".file-upload-text");

      if (file) {
        fileUploadText.textContent = file.name;
        clearError(fileInput); // Limpa erro anterior

        if (file.size > maxSizeBytes) {
          displayError(
            fileInput,
            `O arquivo excede o tamanho máximo permitido de ${maxUploadMb} MB.`
          );
          event.target.value = ""; // Limpa o input se for muito grande
          fileUploadText.textContent = "Selecione um arquivo";
        } else if (!allowedTypes.includes(file.type)) {
          displayError(
            fileInput,
            "Tipo de arquivo não permitido. Permtidos: PDF, DOCX, JPG, PNG, XLS, XLSX."
          );
          event.target.value = ""; // Limpa o input se o tipo for inválido
          fileUploadText.textContent = "Selecione um arquivo";
        }
      } else {
        fileUploadText.textContent = "Selecione um arquivo";
      }
    });
  }

  if (form) {
    form.addEventListener("submit", function (event) {
      let isValid = true;

      // Exemplo de validação simples para documento (apenas números)
      const documentoInput = document.getElementById("id_documento");
      if (documentoInput) {
        const rawDoc = documentoInput.value.replace(/\D/g, ""); // Remove não-dígitos
        if (rawDoc.length !== 11 && rawDoc.length !== 14) {
          displayError(
            documentoInput,
            "Documento deve ter 11 (CPF) ou 14 (CNPJ) dígitos."
          );
          isValid = false;
        } else {
          clearError(documentoInput);
        }
      }

      // Exemplo de validação para data de validade (não ser anterior à data de assinatura)
      const dataAssinaturaInput = document.getElementById("id_data_assinatura");
      const dataValidadeInput = document.getElementById("id_data_validade");
      if (dataAssinaturaInput && dataValidadeInput) {
        const dataAssinatura = new Date(dataAssinaturaInput.value);
        const dataValidade = new Date(dataValidadeInput.value);

        if (dataValidade < dataAssinatura) {
          displayError(
            dataValidadeInput,
            "A data de validade não pode ser anterior à data de assinatura."
          );
          isValid = false;
        } else {
          clearError(dataValidadeInput);
        }
      }

      // Se alguma validação falhar, impede a submissão
      if (!isValid) {
        event.preventDefault(); // Impede a submissão do formulário
        console.log("Validação client-side falhou. Formulário não submetido.");
      }
    });
  }

  // Funções auxiliares para mostrar/limpar erros
  function displayError(inputElement, message) {
    let errorDiv = inputElement.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains("error-message")) {
      errorDiv = document.createElement("div");
      errorDiv.classList.add("error-message");
      inputElement.parentNode.insertBefore(errorDiv, inputElement.nextSibling);
    }
    errorDiv.textContent = message;
    inputElement.classList.add("is-invalid"); // Adiciona classe para estilização
  }

  function clearError(inputElement) {
    const errorDiv = inputElement.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains("error-message")) {
      errorDiv.remove();
    }
    inputElement.classList.remove("is-invalid");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("id_arquivo_contrato");
  const fileLabel = document.querySelector(".file-upload-text");

  if (fileInput && fileLabel) {
    fileInput.addEventListener("change", function () {
      if (this.files.length > 0) {
        fileLabel.textContent = this.files[0].name;
      } else {
        fileLabel.textContent = "Selecione um arquivo";
      }
    });
  }
});
