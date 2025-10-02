(function () {
  'use strict';

  // Config: URL del endpoint Django; puede sobreescribirse poniendo window.REGISTRO_API_URL
  const API_URL = window.REGISTRO_API_URL || '/registrar_usuario/';

  // Utilidad: obtener CSRF desde cookie (Django)
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  }

  // Separa nombre completo en nombre y apellidos
  function splitNombreCompleto(nombreCompleto) {
    const limpio = (nombreCompleto || '').trim().replace(/\s+/g, ' ');
    if (!limpio) return { nombre: '', apellidos: '' };
    const partes = limpio.split(' ');
    if (partes.length === 1) return { nombre: partes[0], apellidos: '' };
    const nombre = partes.shift();
    const apellidos = partes.join(' ');
    return { nombre, apellidos };
  }

  // Mensajería mínima
  function showMessage(type, text) {
    // type: 'success' | 'error' | 'info'
    // Simple y directo para esta tarea
    alert(text);
  }

  document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('formRegistro');
    if (!form) return; // No hay formulario en esta página

    const inputNombre = document.getElementById('nombre');
    const inputEmail = document.getElementById('email');
    const inputPassword = document.getElementById('password');
    const inputConfirm = document.getElementById('confirmPassword');

    form.addEventListener('submit', async (ev) => {
      ev.preventDefault();

      // Validación mínima en cliente
      const nombreCompleto = inputNombre?.value?.trim() || '';
      const email = inputEmail?.value?.trim() || '';
      const password = inputPassword?.value || '';
      const confirm = inputConfirm?.value || '';

      if (!nombreCompleto) {
        inputNombre?.focus();
        return showMessage('error', 'Ingrese su nombre completo.');
      }
      if (!email) {
        inputEmail?.focus();
        return showMessage('error', 'Ingrese su correo.');
      }
      if (!password) {
        inputPassword?.focus();
        return showMessage('error', 'Ingrese una contraseña.');
      }
      if (password !== confirm) {
        inputConfirm?.focus();
        return showMessage('error', 'Las contraseñas no coinciden.');
      }

      const { nombre, apellidos } = splitNombreCompleto(nombreCompleto);

  
      const payload = {
        nombre: nombre,
        apellidos: apellidos,
        correo: email,
        rol: 'usuario',

        'contraseña': password,
        'contraeña': password,
        clave: password
      };

      const csrftoken = getCookie('csrftoken');

      try {
        const resp = await fetch(API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(csrftoken ? { 'X-CSRFToken': csrftoken } : {})
          },
          credentials: 'same-origin',
          body: JSON.stringify(payload)
        });

    
        let data = null;
        try {
          data = await resp.json();
        } catch (_) {
        
        }

        if (!resp.ok) {
          const msg = (data && (data.error || data.message)) || `Error ${resp.status}`;
          return showMessage('error', msg);
        }

        if (data && data.success) {
          showMessage('success', data.message || 'Registro exitoso.');
          return;
        } else {
          const msg = (data && (data.error || data.message)) || 'No se pudo completar el registro.';
          return showMessage('error', msg);
        }
      } catch (err) {
        console.error('Fallo al registrar:', err);
        return showMessage('error', 'No se pudo contactar con el servidor. Intente nuevamente.');
      }
    });
  });
})();
