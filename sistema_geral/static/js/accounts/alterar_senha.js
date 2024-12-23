    // Validação de formulário (opcional, mas recomendado para melhorar a UX)
    (function () {
        'use strict';
        window.addEventListener('load', function () {
            var form = document.getElementsByClassName('needs-validation');
            Array.prototype.filter.call(form, function (form) {
                form.addEventListener('submit', function (event) {
                    if (form.checkValidity() === false) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }, false);
            });
        }, false);
    })();