// --- Archivo: static/js/main_demo.js (VERSIÓN DE DIAGNÓSTICO MDN) ---

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Lógica del Theme Switcher (sin cambios) ---
    // ... tu código del theme switcher ...

    // --- Lógica del Escáner (sin cambios) ---
    // ... tu código del escáner ...

    // --- Lógica para Notificaciones Push de Demo (LÓGICA FINAL) ---
    const notifyBtn = document.getElementById('enable-notifications-btn');
    const notifyStatus = document.getElementById('notification-status');

    if (notifyBtn) {
        if (!("Notification" in window)) {
            notifyStatus.textContent = "Navegador no soporta notificaciones.";
            notifyBtn.disabled = true;
            return; // Salimos de la función si no hay soporte
        }

        // Función que dispara la simulación de alertas
        const runAlertSimulation = () => {
            notifyStatus.textContent = '¡Sistema de alertas activo! Recibirás notificaciones de prueba.';
            notifyBtn.style.display = 'none'; // Ocultamos el botón una vez activado

            const showNotification = (title, body) => {
                new Notification(title, {
                    body: body,
                    icon: "/static/img/logo_notificacion.png"
                });
            };

            // Disparamos las notificaciones de prueba
            setTimeout(() => showNotification('💰 ¡Meta de Ventas Alcanzada!', '¡Felicidades! Se ha superado la meta de ventas diarias.'), 5000);
            setTimeout(() => showNotification('⚠️ Stock Bajo', 'El producto "Pisco Portón" tiene solo 5 unidades restantes.'), 10000);
            setTimeout(() => showNotification('📦 Cierre de Caja', 'Caja 1 ha cerrado turno con un total de S/ 4,600.00.'), 15000);
        };

        // Verificamos el estado del permiso al cargar la página
        if (Notification.permission === "granted") {
            runAlertSimulation(); // Si ya tenemos permiso, corremos la simulación directamente
        } else if (Notification.permission !== "denied") {
            notifyStatus.textContent = 'Activa las notificaciones para recibir alertas en tiempo real.';
            notifyBtn.addEventListener("click", () => {
                Notification.requestPermission().then((permission) => {
                    if (permission === "granted") {
                        runAlertSimulation(); // Si nos dan permiso, corremos la simulación
                    } else {
                        notifyStatus.textContent = 'Permiso denegado.';
                    }
                });
            });
        } else {
            notifyStatus.textContent = 'Las notificaciones están bloqueadas en la configuración de tu navegador.';
            notifyBtn.disabled = true;
        }
    }
});