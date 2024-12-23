// Validação de formulário (exemplo)
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    const assuntoInput = document.querySelector('#assunto');
    const descricaoInput = document.querySelector('#descricao');
    const setorInput = document.querySelector('#setor');
    
    form.addEventListener('submit', function(event) {
        // Validações simples
        if (assuntoInput.value.trim() === '') {
            alert("Por favor, insira um assunto.");
            event.preventDefault();
            return;
        }
        if (descricaoInput.value.trim() === '') {
            alert("Por favor, insira uma descrição.");
            event.preventDefault();
            return;
        }
        if (setorInput.value === '') {
            alert("Por favor, selecione um setor de atendimento.");
            event.preventDefault();
            return;
        }
    });
});
