function selectMic(option) {
    // Entferne die ausgewählte Klasse von allen Optionen
    document.querySelectorAll('.dropdown-options div').forEach(div => {
        div.classList.remove('selected');
    });

    // Markiere das geklickte Element als ausgewählt
    option.classList.add('selected');

    // Aktualisiere die Anzeige im Dropdown
    document.getElementById('selected-mic').querySelector('span').textContent = option.textContent;
}
