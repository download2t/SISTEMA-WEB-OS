document.addEventListener('DOMContentLoaded', function () {
    const statusOptions = document.querySelectorAll('.status-option');
    const selectedStatusContainer = document.getElementById('selected-status-container');
    const statusInput = document.getElementById('status-input');

    // Lista para armazenar os status selecionados
    let selectedStatus = [];

    // Função para atualizar o status selecionado no frontend e no input escondido
    function updateSelectedStatus() {
        // Limpa o container visual
        selectedStatusContainer.innerHTML = '';

        // Adiciona um "chip" para cada status selecionado
        selectedStatus.forEach((status) => {
            const chip = document.createElement('div');
            chip.className = 'badge bg-primary text-white d-flex align-items-center gap-2';
            chip.innerHTML = `
                <span>${status}</span>
                <button type="button" class="btn-close btn-close-white" aria-label="Remove"></button>
            `;

            // Remove o status ao clicar no botão "x"
            chip.querySelector('button').addEventListener('click', () => {
                selectedStatus = selectedStatus.filter((s) => s !== status);
                updateSelectedStatus();
            });

            selectedStatusContainer.appendChild(chip);
        });

        // Atualiza o campo escondido com os status selecionados (em formato CSV)
        statusInput.value = selectedStatus.join(',');
    }

    // Adiciona um status à lista quando um botão é clicado
    statusOptions.forEach((button) => {
        button.addEventListener('click', () => {
            const status = button.getAttribute('data-value');
            if (!selectedStatus.includes(status)) {
                selectedStatus.push(status);
            }
            updateSelectedStatus();
        });
    });
});
