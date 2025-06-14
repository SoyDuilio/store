// app/static/script.js
function changeTheme(themeClass) {
    const classList = document.body.classList;
    while (classList.length > 0) {
        classList.remove(classList.item(0));
    }
    const baseClasses = "font-size-normal font-family-default".split(" ");
    document.body.classList.add(themeClass, ...baseClasses);
}

function changeFontSize(sizeClass) {
    document.body.className = document.body.className.replace(/font-size-\w+/g, '');
    document.body.classList.add(sizeClass);
}

function changeFontFamily(familyClass) {
    document.body.className = document.body.className.replace(/font-family-\w+/g, '');
    document.body.classList.add(familyClass);
}

const synth = window.speechSynthesis;
let currentUtterance = null;

function speak(textToRead, buttonElement) {
    if (synth.speaking) {
        synth.cancel();
        if (currentUtterance && currentUtterance.text.length === textToRead.length) {
            currentUtterance = null; return;
        }
    }
    const utterance = new SpeechSynthesisUtterance(textToRead);
    utterance.lang = 'es-ES';
    utterance.rate = 0.9;
    currentUtterance = utterance;

    document.querySelectorAll('.speak-btn').forEach(btn => btn.classList.remove('speaking'));
    if (buttonElement) buttonElement.classList.add('speaking');
    
    utterance.onend = () => {
        if (buttonElement) buttonElement.classList.remove('speaking');
        currentUtterance = null;
    };
    utterance.onerror = (event) => {
        console.error('Error en la síntesis de voz:', event.error);
        if (buttonElement) buttonElement.classList.remove('speaking');
    };
    synth.speak(utterance);
}

document.addEventListener('DOMContentLoaded', () => {
    const mainSpeakButton = document.getElementById('speak-all-btn');
    if (mainSpeakButton) {
        mainSpeakButton.addEventListener('click', () => {
            const content = document.getElementById('ebook-content').innerText;
            speak(content.replace(/(\r\n|\n|\r)/gm, " ").replace(/\s+/g, ' '), mainSpeakButton);
        });
    }
});