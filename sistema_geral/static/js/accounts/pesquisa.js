document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const statusSelect = document.getElementById('status-select');

    searchInput.addEventListener('input', function() {
        const searchQuery = this.value;
        const status = statusSelect.value;

        fetch(`/accounts/pesquisar_usuarios/?status=${status}&search=${searchQuery}`)
            .then(response => response.text())
            .then(data => {
                document.getElementById('user-list').innerHTML = data;
            })
            .catch(error => console.error('Erro:', error));
    });
});
