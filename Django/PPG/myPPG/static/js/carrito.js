// carrito.js - Versión mejorada
const CLP = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 });
const parseCLP = (txt) => Number(String(txt).replace(/[^0-9]/g, '')) || 0;

const CART_KEY = 'ppg_cart';

const Cart = {
  _load() {
    try { return JSON.parse(localStorage.getItem(CART_KEY)) || []; } catch { return []; }
  },
  _save(items) {
    localStorage.setItem(CART_KEY, JSON.stringify(items));
    Cart.renderBadge();
  },
  all() { return this._load(); },
  count() { return this._load().reduce((acc, it) => acc + it.qty, 0); },
  total() { return this._load().reduce((acc, it) => acc + (it.price * it.qty), 0); },
  add(item) {
    const items = this._load();
    const idx = items.findIndex(i => i.id === item.id);
    if (idx >= 0) { items[idx].qty += item.qty || 1; }
    else { items.push({ ...item, qty: item.qty || 1 }); }
    this._save(items);
  },
  setQty(id, qty) {
    const items = this._load().map(i => i.id === id ? { ...i, qty: Math.max(1, qty|0) } : i);
    this._save(items);
  },
  remove(id) {
    const items = this._load().filter(i => i.id !== id);
    this._save(items);
  },
  clear() { this._save([]); },

  // Badge flotante del carrito
  ensureBadge() {
    if (document.getElementById('ppg-cart-badge')) return;

    const a = document.createElement('a');
    a.id = 'ppg-cart-badge';
    a.href = 'carrito.html';
    a.setAttribute('aria-label', 'Abrir carrito');
    a.style.position = 'fixed';
    a.style.right = '16px';
    a.style.bottom = '16px';
    a.style.zIndex = '9999';
    a.style.textDecoration = 'none';

    const btn = document.createElement('div');
    btn.style.minWidth = '56px';
    btn.style.height = '56px';
    btn.style.borderRadius = '999px';
    btn.style.display = 'flex';
    btn.style.alignItems = 'center';
    btn.style.justifyContent = 'center';
    btn.style.boxShadow = '0 6px 16px rgba(0,0,0,.25)';
    btn.style.background = '#0d6efd';
    btn.style.color = 'white';
    btn.style.fontWeight = '700';
    btn.style.fontFamily = 'system-ui, -apple-system, Segoe UI, Roboto, sans-serif';
    btn.textContent = '🛒 0';

    a.appendChild(btn);
    document.body.appendChild(a);
  },
  renderBadge() {
    this.ensureBadge();
    const el = document.querySelector('#ppg-cart-badge div');
    if (el) el.textContent = '🛒 ' + this.count();
  }
};

// Añadir botones "Agregar al carrito" a las tarjetas de productos
function enhanceCards() {
  const cards = document.querySelectorAll('.category-card');
  cards.forEach((card, idx) => {
    // Evitar duplicados
    if (card.querySelector('.ppg-add-btn')) return;

    const title = (card.querySelector('h3')?.textContent || 'Producto').trim();
    const priceTxt = (card.querySelector('.price')?.textContent || '$0').trim();
    const img = card.querySelector('img')?.getAttribute('src') || '';

    // ID estable: por título + precio (y un índice de respaldo)
    const id = (title + '|' + priceTxt).toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9\-|]/g,'') + '-' + idx;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ppg-add-btn';
    btn.textContent = 'Agregar al carrito';
    btn.style.marginTop = '8px';
    btn.style.display = 'inline-block';
    btn.style.padding = '8px 12px';
    btn.style.borderRadius = '8px';
    btn.style.border = '0';
    btn.style.background = '#198754';
    btn.style.color = '#fff';
    btn.style.cursor = 'pointer';
    btn.addEventListener('click', () => {
      Cart.add({ id, name: title, price: parseCLP(priceTxt), img, qty: 1 });
    
      btn.textContent = '¡Agregado!';
      setTimeout(() => (btn.textContent = 'Agregar al carrito'), 900);
    });

    const content = card.querySelector('.category-content') || card;
    content.appendChild(btn);
  });
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
  // Muestra el badge del carrito
  Cart.renderBadge();
  
  // Añade botones a las tarjetas de productos
  enhanceCards();
});