document.addEventListener('DOMContentLoaded', function () {
    const statusSelect = document.getElementById('status');
    const ticketContainer = document.getElementById('numero-ticket-container');

    // Função para mostrar/ocultar o campo do número do ticket
    function toggleTicketField() {
        if (statusSelect.value === 'Encaminhado a TOTVS') {
            ticketContainer.style.display = 'block';
        } else {
            ticketContainer.style.display = 'none';
        }
    }

    // Evento de mudança no campo de status
    statusSelect.addEventListener('change', toggleTicketField);

    // Inicializar o estado do campo no carregamento
    toggleTicketField();
});