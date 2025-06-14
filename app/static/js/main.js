// js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // --- ELEMENTOS DEL DOM ---
    const body = document.body;
    const content = document.getElementById('ebook-content');
    
    // Botones de control
    const themeLightBtn = document.getElementById('theme-light');
    const themeDarkBtn = document.getElementById('theme-dark');
    const themeFeminineBtn = document.getElementById('theme-feminine');
    const increaseFontBtn = document.getElementById('increase-font');
    const decreaseFontBtn = document.getElementById('decrease-font');
    const readAloudBtn = document.getElementById('read-aloud');
    const readAloudIcon = readAloudBtn.querySelector('i');

    // --- LÓGICA DE TEMAS ---
    const availableThemes = ['theme-light', 'theme-dark', 'theme-feminine'];
    
    function setTheme(themeName) {
        // Quita todas las clases de tema del body
        availableThemes.forEach(t => body.classList.remove(t));
        // Añade la clase del tema seleccionado
        body.classList.add(themeName);
        // Guarda la preferencia en el localStorage
        localStorage.setItem('ebook_theme', themeName);
    }
    
    themeLightBtn.addEventListener('click', () => setTheme('theme-light'));
    themeDarkBtn.addEventListener('click', () => setTheme('theme-dark'));
    themeFeminineBtn.addEventListener('click', () => setTheme('theme-feminine'));

    // Cargar tema guardado al iniciar
    const savedTheme = localStorage.getItem('ebook_theme') || 'theme-dark'; // Oscuro por defecto
    setTheme(savedTheme);

    // --- LÓGICA DE TAMAÑO DE FUENTE ---
    function changeFontSize(direction) {
        const currentSize = parseFloat(window.getComputedStyle(content, null).getPropertyValue('font-size'));
        const newSize = direction === 'increase' ? currentSize + 1 : currentSize - 1;

        // Limites para el tamaño de la fuente
        if (newSize >= 12 && newSize <= 28) {
            content.style.fontSize = `${newSize}px`;
        }
    }

    increaseFontBtn.addEventListener('click', () => changeFontSize('increase'));
    decreaseFontBtn.addEventListener('click', () => changeFontSize('decrease'));

    // --- LÓGICA DE LECTURA EN VOZ ALTA (WEB SPEECH API) ---
    let isReading = false;
    const synth = window.speechSynthesis;

    function toggleReadAloud() {
        if (!synth) {
            alert('Tu navegador no soporta la lectura en voz alta.');
            return;
        }

        if (isReading) {
            synth.cancel(); // Detiene la lectura
            isReading = false;
            readAloudBtn.classList.remove('active');
            readAloudIcon.classList.remove('fa-stop');
            readAloudIcon.classList.add('fa-volume-high');
        } else {
            const textToRead = content.querySelector('article').innerText;
            const utterance = new SpeechSynthesisUtterance(textToRead);
            utterance.lang = 'es-PE'; // Especifica el idioma para mejor pronunciación

            utterance.onstart = () => {
                isReading = true;
                readAloudBtn.classList.add('active');
                readAloudIcon.classList.remove('fa-volume-high');
                readAloudIcon.classList.add('fa-stop');
            };

            utterance.onend = () => {
                isReading = false;
                readAloudBtn.classList.remove('active');
                readAloudIcon.classList.remove('fa-stop');
                readAloudIcon.classList.add('fa-volume-high');
            };
            
            utterance.onerror = (event) => {
                console.error('SpeechSynthesisUtterance.onerror', event);
                isReading = false;
                readAloudBtn.classList.remove('active');
                 readAloudIcon.classList.remove('fa-stop');
                readAloudIcon.classList.add('fa-volume-high');
            };

            synth.speak(utterance);
        }
    }
    
    // Asegurarse de que si se cierra la ventana, se detiene la lectura
    window.addEventListener('beforeunload', () => {
        if(isReading) synth.cancel();
    });

    readAloudBtn.addEventListener('click', toggleReadAloud);
});