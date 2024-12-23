
console.log('JS carregado'); // Verificação
document.addEventListener('DOMContentLoaded', function () {
    function moveOptions(fromSelect, toSelect) {
        const selectedOptions = Array.from(fromSelect.selectedOptions);
        selectedOptions.forEach(option => {
            toSelect.appendChild(option);
            option.selected = false;
        });
    }

    document.getElementById('add_group').addEventListener('click', function () {
        const availableGroups = document.getElementById('available_groups');
        const assignedGroups = document.getElementById('assigned_groups');
        moveOptions(availableGroups, assignedGroups);
    });

    document.getElementById('remove_group').addEventListener('click', function () {
        const availableGroups = document.getElementById('available_groups');
        const assignedGroups = document.getElementById('assigned_groups');
        moveOptions(assignedGroups, availableGroups);
    });

    // Garantir que os grupos escolhidos sejam enviados no submit
    document.querySelector('form').addEventListener('submit', function () {
        const assignedGroups = document.getElementById('assigned_groups');
        Array.from(assignedGroups.options).forEach(option => {
            option.selected = true; // Marca todos os grupos para envio
        });
    });
});
