/*Script para botão de mensagens*/
document.getElementById('toggle-order-btn').addEventListener('click', function () {
    const listaMensagens = document.getElementById('mensagens-list');
    const mensagens = Array.from(listaMensagens.children);
    mensagens.reverse();
    listaMensagens.innerHTML = '';
    mensagens.forEach(mensagem => listaMensagens.appendChild(mensagem));

    const btnText = this.innerText;
    this.innerText = btnText === 'Exibir Mais Recentes Primeiro' 
                        ? 'Exibir Mais Antigas Primeiro' 
                        : 'Exibir Mais Recentes Primeiro';
});

/* Script para botão de evidencias*/
document.addEventListener('DOMContentLoaded', function() {
    const toggleEvidenciasBtn = document.getElementById('toggle-evidencias-btn');
    const evidenciasContainer = document.getElementById('evidencias-container');
    toggleEvidenciasBtn.addEventListener('click', function() {
        evidenciasContainer.classList.toggle('d-none');
        toggleEvidenciasBtn.querySelector('i').classList.toggle('fa-chevron-down');
        toggleEvidenciasBtn.querySelector('i').classList.toggle('fa-chevron-up');
    });
});
