document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll(".toggle-status");

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const userId = this.getAttribute("data-id");
            const isActive = this.checked;

            // Enviar a requisição AJAX dependendo de estar ativando ou desativando
            const url = isActive ? `/accounts/${userId}/ativar_usuario/` : `/accounts/${userId}/desativar_usuario/`;

            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken // Incluindo o CSRF token aqui
                },
                body: JSON.stringify({})  // Corpo vazio, já que não precisamos enviar 'is_active'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Status alterado com sucesso!");
                } else {
                    console.log("Erro ao alterar o status: " + data.message);
                }
            })
            .catch(error => {
                console.error("Erro:", error);
            });
        });
    });
});
