// js/admin.js
(function(){
  'use strict';

  const USERS_KEY = 'usuarios';
  const CURRENT_USER_KEY = 'usuarioActual';
  const PRODUCTS_KEY = 'productos';

  function handleLogout() {
    localStorage.removeItem(CURRENT_USER_KEY);
    location.href = 'login.html';
    }

  // Semillas (para ver datos al entrar) 
  function seedProducts(){
    if(!localStorage.getItem(PRODUCTS_KEY)){
      const sample = [
        {id: 1, nombre: 'Elden Ring',     categoria: 'Acción',   precio: 59990, stock: 10, imagen: 'img/elden-ring.jpg'},
        {id: 2, nombre: 'Cyberpunk 2077', categoria: 'Acción',   precio: 24990, stock: 25, imagen: 'img/cyberpunk.jpg'},
        {id: 3, nombre: 'EA FC 25',       categoria: 'Deportes', precio: 54990, stock: 30, imagen: 'img/eafc25.jpg'}
      ];
      localStorage.setItem(PRODUCTS_KEY, JSON.stringify(sample));
    }
  }
  function seedUsers(){
    if(!localStorage.getItem(USERS_KEY)){
      const sampleUsers = [
        {id: 1, nombre: 'Admin',       email: 'admin@pixelplay.com', rol: 'administrador', password: 'Admin123!'},
        {id: 2, nombre: 'Juan Pérez',  email: 'juan@example.com',     rol: 'cliente',       password: 'Cliente123!'},
        {id: 3, nombre: 'María López', email: 'maria@example.com',    rol: 'cliente',       password: 'Cliente123!'}
      ];
      localStorage.setItem(USERS_KEY, JSON.stringify(sampleUsers));
    }
  }

  //  Helpers 
  const getUsers     = () => JSON.parse(localStorage.getItem(USERS_KEY)    || '[]');
  const setUsers     = (v) => localStorage.setItem(USERS_KEY, JSON.stringify(v));
  const getProducts  = () => JSON.parse(localStorage.getItem(PRODUCTS_KEY) || '[]');
  const setProducts  = (v) => localStorage.setItem(PRODUCTS_KEY, JSON.stringify(v));
  const fmtCLP       = (n) => new Intl.NumberFormat('es-CL',{style:'currency',currency:'CLP',maximumFractionDigits:0}).format(n||0);
  const nextId       = (list) => list.reduce((m,x)=>Math.max(m, Number(x.id)||0),0) + 1;

  //  El render 
  function renderUsers(){
    const tbody = document.querySelector('#tablaUsuarios tbody');
    if(!tbody) return;
    tbody.innerHTML = '';
    getUsers().forEach(u => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${u.id}</td>
        <td>${u.nombre}</td>
        <td>${u.email}</td>
        <td><span class="badge ${u.rol==='administrador'?'bg-danger':'bg-secondary'}">${u.rol}</span></td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-primary me-1" data-action="editar-usuario" data-id="${u.id}">Editar</button>
          <button class="btn btn-sm btn-outline-danger" data-action="eliminar-usuario" data-id="${u.id}">Eliminar</button>
        </td>`;
      tbody.appendChild(tr);
    });
  }

  function renderProducts(){
    const tbody = document.querySelector('#tablaProductos tbody');
    if(!tbody) return;
    tbody.innerHTML = '';
    getProducts().forEach(p => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${p.id}</td>
        <td class="d-flex align-items-center gap-2">
          <img src="${p.imagen||''}" alt="" style="width:38px;height:38px;object-fit:cover;border-radius:6px;border:1px solid #eee">
          <div>${p.nombre}<div class="small text-muted">${p.categoria||'-'}</div></div>
        </td>
        <td class="text-end">${fmtCLP(p.precio)}</td>
        <td class="text-end">${p.stock ?? 0}</td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-primary me-1" data-action="editar-producto" data-id="${p.id}">Editar</button>
          <button class="btn btn-sm btn-outline-danger" data-action="eliminar-producto" data-id="${p.id}">Eliminar</button>
        </td>`;
      tbody.appendChild(tr);
    });
  }

  // CRUD 
  function upsertUser(data){
    const users = getUsers();
    const idx = users.findIndex(u => u.id == data.id);
    if(idx >= 0){ users[idx] = {...users[idx], ...data}; }
    else { data.id = nextId(users); users.push(data); }
    setUsers(users);
    renderUsers();
  }

  function deleteUser(id){
    const current = JSON.parse(localStorage.getItem(CURRENT_USER_KEY)||'null');
    if(current && current.id == id){ alert('No puedes eliminar tu propio usuario.'); return; }
    setUsers(getUsers().filter(u => u.id != id));
    renderUsers();
  }

  function upsertProduct(data){
    const list = getProducts();
    const idx = list.findIndex(p => p.id == data.id);
    if(idx >= 0){ list[idx] = {...list[idx], ...data}; }
    else { data.id = nextId(list); list.push(data); }
    setProducts(list);
    renderProducts();
  }

  function deleteProduct(id){
    setProducts(getProducts().filter(p => p.id != id));
    renderProducts();
  }

  // Eventos 
  function bindEvents(){
    // Acciones de tablas
    document.addEventListener('click', (e)=>{
      const btn = e.target.closest('button[data-action]');
      if(!btn) return;
      const id = Number(btn.dataset.id);
      const action = btn.dataset.action;

      if(action === 'editar-usuario'){
        const u = getUsers().find(x=>x.id == id); if(!u) return;
        fillUserForm(u);
        new bootstrap.Modal(document.getElementById('modalUsuario')).show();

      }else if(action === 'eliminar-usuario'){
        if(confirm('¿Eliminar usuario?')) deleteUser(id);

      }else if(action === 'editar-producto'){
        const p = getProducts().find(x=>x.id == id); if(!p) return;
        fillProductForm(p);
        new bootstrap.Modal(document.getElementById('modalProducto')).show();

      }else if(action === 'eliminar-producto'){
        if(confirm('¿Eliminar producto?')) deleteProduct(id);
      }
    });

    // Botones "Nuevo"
    document.getElementById('btnNuevoUsuario')?.addEventListener('click', ()=>{
      fillUserForm({id:'', nombre:'', email:'', rol:'cliente', password:''});
      new bootstrap.Modal(document.getElementById('modalUsuario')).show();
    });

    document.getElementById('btnNuevoProducto')?.addEventListener('click', ()=>{
      fillProductForm({id:'', nombre:'', categoria:'', precio:'', stock:'', imagen:''});
      new bootstrap.Modal(document.getElementById('modalProducto')).show();
    });

    // Submit formularios
    document.getElementById('formUsuario')?.addEventListener('submit', (e)=>{
      e.preventDefault();
      const data = Object.fromEntries(new FormData(e.target).entries());
      const id = data.id ? Number(data.id) : undefined;
      const usuario = { id, nombre: data.nombre, email: data.email, rol: data.rol, password: data.password || undefined };
      if(!usuario.nombre || !usuario.email){ alert('Completa nombre y correo.'); return; }
      upsertUser(usuario);
      bootstrap.Modal.getInstance(document.getElementById('modalUsuario')).hide();
      e.target.reset();
    });


    // boton de cerrar sesión
    document.getElementById('btnLogout')?.addEventListener('click', (e) => {
      e.preventDefault();
      handleLogout();
    });
    document.getElementById('formProducto')?.addEventListener('submit', (e)=>{
      e.preventDefault();
      const data = Object.fromEntries(new FormData(e.target).entries());
      const id = data.id ? Number(data.id) : undefined;
      const precio = Number(data.precio||0);
      const stock = Number(data.stock||0);
      if(!data.nombre || !data.categoria || !precio){ alert('Completa nombre, categoría y precio.'); return; }
      upsertProduct({ id, nombre: data.nombre, categoria: data.categoria, precio, stock, imagen: data.imagen });
      bootstrap.Modal.getInstance(document.getElementById('modalProducto')).hide();
      e.target.reset();
    });
  }

  // Helpers de formularios
  function fillUserForm(u){
    document.querySelector('#formUsuario [name=id]').value       = u.id || '';
    document.querySelector('#formUsuario [name=nombre]').value   = u.nombre || '';
    document.querySelector('#formUsuario [name=email]').value    = u.email || '';
    document.querySelector('#formUsuario [name=rol]').value      = u.rol || 'cliente';
    document.querySelector('#formUsuario [name=password]').value = u.password || '';
  }

  function fillProductForm(p){
    document.querySelector('#formProducto [name=id]').value        = p.id || '';
    document.querySelector('#formProducto [name=nombre]').value    = p.nombre || '';
    document.querySelector('#formProducto [name=categoria]').value = p.categoria || '';
    document.querySelector('#formProducto [name=precio]').value    = p.precio || '';
    document.querySelector('#formProducto [name=stock]').value     = p.stock || '';
    document.querySelector('#formProducto [name=imagen]').value    = p.imagen || '';
    const prev = document.getElementById('previewImagen');
    if(prev) prev.src = p.imagen || '';
  }

  // Permisos 
  function requireAdmin(){
    const user = JSON.parse(localStorage.getItem(CURRENT_USER_KEY)||'null');
    if(!user){ alert('Debes iniciar sesión.'); location.href='login.html'; return false; }
    if(user.rol !== 'administrador'){ alert('No tienes permisos.'); location.href='index.html'; return false; }
    return true;
  }

  // Init 
  document.addEventListener('DOMContentLoaded', ()=>{
    if(!requireAdmin()) return;
    seedProducts();
    seedUsers();
    renderUsers();
    renderProducts();
    bindEvents();
  });

})();
