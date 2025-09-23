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
    if (idx >= 0) { 
      items[idx].qty += item.qty || 1; 
    } else { 
      items.push({ ...item, qty: item.qty || 1 }); 
    }
    this._save(items);
    this.showAddNotification(item.name);
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

  // Función para mostrar notificación de producto añadido
  showAddNotification(productName) {
    // Crear notificación
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #198754;
      color: white;
      padding: 12px 16px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      z-index: 10000;
      font-family: system-ui;
      font-size: 14px;
      animation: slideIn 0.3s ease;
    `;
    
    notification.innerHTML = `
      <strong>✓ Producto añadido</strong><br>
      ${productName}
    `;
    
    document.body.appendChild(notification);
    
    // Remover después de 3 segundos
    setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  },

  // Badge flotante del carrito
  ensureBadge() {
    if (document.getElementById('ppg-cart-badge')) return;

    const a = document.createElement('a');
    a.id = 'ppg-cart-badge';
    a.href = 'carrito.html';
    a.setAttribute('aria-label', 'Abrir carrito');
    a.style.cssText = `
      position: fixed;
      right: 16px;
      bottom: 16px;
      z-index: 9999;
      text-decoration: none;
    `;

    const btn = document.createElement('div');
    btn.style.cssText = `
      min-width: 56px;
      height: 56px;
      border-radius: 999px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 6px 16px rgba(0,0,0,.25);
      background: #0d6efd;
      color: white;
      font-weight: 700;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      font-size: 14px;
    `;
    btn.textContent = '🛒 0';

    a.appendChild(btn);
    document.body.appendChild(a);

    // Añadir estilos de animación
    const style = document.createElement('style');
    style.textContent = `
      @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
      @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
      }
      @keyframes bounce {
        0%, 20%, 60%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        80% { transform: translateY(-5px); }
      }
      .ppg-add-btn {
        margin-top: 8px;
        padding: 8px 12px;
        border-radius: 8px;
        border: 0;
        background: #198754;
        color: #fff;
        cursor: pointer;
        transition: all 0.2s ease;
      }
      .ppg-add-btn:hover {
        background: #157347;
        transform: translateY(-1px);
      }
      .ppg-add-btn:active {
        transform: translateY(0);
      }
    `;
    document.head.appendChild(style);
  },

  renderBadge() {
    this.ensureBadge();
    const el = document.querySelector('#ppg-cart-badge div');
    if (el) {
      const count = this.count();
      el.textContent = `🛒 ${count}`;
      
      // Animación cuando se añade un producto
      if (count > 0) {
        el.style.animation = 'bounce 0.5s ease';
        setTimeout(() => el.style.animation = '', 500);
      }
    }
  }
};

// Función global para añadir al carrito (necesaria para productos.html)
function addToCart(item) {
  Cart.add(item);
}

// Añadir botones "Agregar al carrito" a las tarjetas de productos
function enhanceCards() {
  const cards = document.querySelectorAll('.category-card');
  cards.forEach((card, idx) => {
    // Evitar duplicados
    if (card.querySelector('.ppg-add-btn')) return;

    const title = (card.querySelector('h3')?.textContent || 'Producto').trim();
    const priceTxt = (card.querySelector('.price')?.textContent || '$0').trim();
    const img = card.querySelector('img')?.getAttribute('src') || '';

    // ID único basado en título + precio + índice
    const id = (title + '|' + priceTxt).toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9\-|]/g,'') + '-' + idx;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ppg-add-btn';
    btn.textContent = 'Agregar al carrito';
    
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      
      Cart.add({ 
        id, 
        name: title, 
        price: parseCLP(priceTxt), 
        img, 
        qty: 1 
      });
    });

    const content = card.querySelector('.category-content') || card;
    content.appendChild(btn);
  });
}

// Inicialización cuando el DOM esté listo
function initCart() {
  // Muestra el badge del carrito
  Cart.renderBadge();
  
  // Añade botones a las tarjetas de productos (excepto en carrito.html)
  if (!document.getElementById('ppg-cart-page')) {
    enhanceCards();
  }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCart);
} else {
  initCart();
}