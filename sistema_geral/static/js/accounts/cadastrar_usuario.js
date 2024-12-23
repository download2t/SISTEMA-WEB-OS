// Exemplo de código JavaScript para interações no formulário
document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.querySelector('form');

    form.addEventListener('submit', (event) => {
        // Aqui você pode adicionar validações personalizadas antes de enviar o formulário
        const password1 = document.getElementById('password1').value;
        const password2 = document.getElementById('password2').value;

        if (password1 !== password2) {
            event.preventDefault(); // Previne o envio do formulário
            alert('As senhas não coincidem!'); // Alerta para o usuário
        }
    });
});
