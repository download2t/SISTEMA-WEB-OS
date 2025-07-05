document.addEventListener('DOMContentLoaded', function () {
    // Script para botão de mensagens (toggle-order-btn)
    const toggleOrderBtn = document.getElementById('toggle-order-btn');
    const listaMensagens = document.getElementById('mensagens-list');

    if (toggleOrderBtn && listaMensagens) {
        toggleOrderBtn.addEventListener('click', function () {
            const mensagens = Array.from(listaMensagens.children);
            mensagens.reverse();
            listaMensagens.innerHTML = ''; // Limpa a lista
            mensagens.forEach(mensagem => listaMensagens.appendChild(mensagem)); // Re-adiciona na nova ordem

            const btnIcon = this.querySelector('i');
            if (btnIcon.classList.contains('fa-sort-amount-down-alt')) {
                btnIcon.classList.remove('fa-sort-amount-down-alt');
                btnIcon.classList.add('fa-sort-amount-up-alt');
                this.childNodes[this.childNodes.length - 1].nodeValue = ' Antigas Primeiro'; // Atualiza o texto do botão
            } else {
                btnIcon.classList.remove('fa-sort-amount-up-alt');
                btnIcon.classList.add('fa-sort-amount-down-alt');
                this.childNodes[this.childNodes.length - 1].nodeValue = ' Recentes Primeiro'; // Atualiza o texto do botão
            }
        });
    }

    // Script para botão de evidencias (toggle-evidencias-btn)
    const toggleEvidenciasBtn = document.getElementById('toggle-evidencias-btn');
    const evidenciasContainer = document.getElementById('evidencias-container');

    if (toggleEvidenciasBtn && evidenciasContainer) {
        // Inicialmente, as evidências podem estar visíveis ou ocultas por CSS.
        // Ocultar por padrão e permitir o toggle.
        // Se quiser começar oculto, você pode adicionar 'd-none' no HTML ou usar:
        // evidenciasContainer.classList.add('d-none'); // Isso ocultaria no carregamento.
        // E ajustar o ícone inicial:
        // toggleEvidenciasBtn.querySelector('i').classList.add('fa-chevron-down');


        toggleEvidenciasBtn.addEventListener('click', function() {
            evidenciasContainer.classList.toggle('d-none'); // Alterna a classe d-none (display: none !important do Bootstrap)
            const btnIcon = this.querySelector('i');
            btnIcon.classList.toggle('fa-chevron-down');
            btnIcon.classList.toggle('fa-chevron-up');
            
            // Atualiza o texto do botão
            const btnTextNode = this.childNodes[this.childNodes.length - 1]; // O textNode está fora do <i>
            if (evidenciasContainer.classList.contains('d-none')) {
                btnTextNode.nodeValue = ' Mostrar/Ocultar';
            } else {
                btnTextNode.nodeValue = ' Mostrar/Ocultar';
            }
        });
    }


    // Função para exibir ou ocultar o campo do número do ticket
    const statusSelect = document.getElementById('status');
    const numeroTicketContainer = document.getElementById('numero-ticket-container');
    const numeroTicketInput = document.getElementById('numero_ticket');

    const toggleNumeroTicket = () => {
        if (statusSelect && numeroTicketContainer && numeroTicketInput) {
            if (statusSelect.value === 'Encaminhado a TOTVS') {
                numeroTicketContainer.style.display = 'block'; // Usando inline style para sobrescrever o "display: none" inicial
                numeroTicketInput.setAttribute('required', 'required');
            } else {
                numeroTicketContainer.style.display = 'none';
                numeroTicketInput.removeAttribute('required');
                // Limpa o valor do campo quando ele é ocultado
                numeroTicketInput.value = ''; 
            }
        }
    };

    if (statusSelect) {
        statusSelect.addEventListener('change', toggleNumeroTicket);
        // Chama a função uma vez para definir o estado inicial com base no valor atual
        toggleNumeroTicket(); 
    }
});