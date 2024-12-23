document.addEventListener('DOMContentLoaded', function () {
    const toggles = document.querySelectorAll('.toggle-status');

    toggles.forEach(function(toggle) {
        toggle.addEventListener('change', function() {
            const userId = this.getAttribute('data-id');
            const isActive = this.checked;

            // Envia a requisição para atualizar o status
            fetch(`/usuarios/${userId}/alterar_status/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ is_active: isActive })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Status atualizado');
                } else {
                    // Se houver um erro, revert o estado do checkbox
                    alert('Erro ao atualizar o status.');
                    this.checked = !isActive;
                }
            })
            .catch(error => {
                alert('Erro ao atualizar o status.');
                this.checked = !isActive;
            });
        });
    });
});
