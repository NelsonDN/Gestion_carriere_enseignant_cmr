document.addEventListener('DOMContentLoaded', function() {
    const isCenseurSelect = document.querySelector('#id_is_censeur');
    const matiereField = document.querySelector('.field-matiere');

    function toggleMatiereField() {
        if (isCenseurSelect.value === 'true') {
            matiereField.style.display = '';
            console.log('OKKKKKKK');

        } else {
            matiereField.style.display = 'none';
            console.log('AAA');

        }
    }

    isCenseurSelect.addEventListener('change', toggleMatiereField);

    // Initial call to set the correct state on page load
    toggleMatiereField();
});
