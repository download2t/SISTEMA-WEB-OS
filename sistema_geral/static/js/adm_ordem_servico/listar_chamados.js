// listar_chamados.js

// Função para exibir alerta quando um filtro for aplicado
document.addEventListener('DOMContentLoaded', function () {
    const statusSelect = document.getElementById('status');
    const searchInput = document.querySelector('input[name="search"]');
    const submitButton = document.querySelector('button[type="submit"]');

    // Verifica se algum filtro foi aplicado (status ou busca)
    if (statusSelect.value !== 'todos' || searchInput.value.trim() !== '') {
        // Exibe um alerta para informar o filtro ativo
        const alertMessage = `Filtros aplicados: 
                              Status: ${statusSelect.options[statusSelect.selectedIndex].text} | 
                              Busca: ${searchInput.value}`;
        alertUser(alertMessage);
    }

    // Função para mostrar uma mensagem de alerta
    function alertUser(message) {
        const alertBox = document.createElement('div');
        alertBox.classList.add('alert', 'alert-info');
        alertBox.textContent = message;
        document.body.appendChild(alertBox);

        setTimeout(() => {
            alertBox.remove();
        }, 5000); // Remove o alerta após 5 segundos
    }




    // Função para destacar a linha de um chamado quando o mouse passar sobre ela
    const chamadoItems = document.querySelectorAll('.list-group-item');
    chamadoItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            item.classList.add('shadow-lg');
        });
        item.addEventListener('mouseleave', function() {
            item.classList.remove('shadow-lg');
        });
    });

    // Filtro de status e campo de busca com ações de submit
    submitButton.addEventListener('click', function () {
        // Ações do filtro podem ser feitas aqui, como envio de formulários ou manipulação adicional de dados.
        console.log("Filtros aplicados - Status: " + statusSelect.value + ", Busca: " + searchInput.value);
    });
});
