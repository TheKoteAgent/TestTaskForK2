async function sendData(url, data, resultElementId) {
    const resEl = document.getElementById(resultElementId);
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        if (!response.ok) {
            resEl.className = 'error';
            resEl.innerText = 'Помилка: ' + (result.error || 'Щось пішло не так');
        } else {
            resEl.className = 'result';
            resEl.innerText = 'Успішно!';
            if (url.includes('clients')) loadClients();
            if (url.includes('product')) loadProducts();
            if (url.includes('order')) { loadOrders(); loadProducts(); }
        }
    } catch (error) {
        resEl.className = 'error';
        resEl.innerText = 'Помилка з\'єднання';
    }
}

document.getElementById('clientForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById('clientName').value,
        phone: document.getElementById('clientPhone').value
    };
    sendData('/api/clients/create', data, 'clientResult');
});

document.getElementById('productForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const data = {
        product_name: document.getElementById('productName').value,
        product_amount: parseInt(document.getElementById('productAmount').value),
        product_price: parseFloat(document.getElementById('productPrice').value)
    };
    sendData('/api/product/create', data, 'productResult');
});

document.getElementById('orderForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const data = {
        client_id: parseInt(document.getElementById('orderClientId').value),
        items: [
            {
                product_id: parseInt(document.getElementById('orderProductId').value),
                quantity: parseInt(document.getElementById('orderQuantity').value)
            }
        ]
    };
    sendData('/api/order/create', data, 'orderResult');
});

// --- ЛОГІКА ОТРИМАННЯ (GET) ---
async function loadClients() {
    const res = await fetch('/api/clients');
    const data = await res.json();
    const list = document.getElementById('clientsList');
    list.innerHTML = '';
    data.clients.forEach(c => {
        list.innerHTML += `<li><strong>ID ${c.id}</strong>: ${c.name} (Тел: ${c.phone})</li>`;
    });
}

async function loadProducts() {
    const res = await fetch('/api/products');
    const data = await res.json();
    const list = document.getElementById('productsList');
    list.innerHTML = '';
    data.products.forEach(p => {
        list.innerHTML += `<li><strong>ID ${p.id}</strong>: ${p.product_name} | Залишок: ${p.product_amount} шт. | Ціна: ${p.product_price} грн</li>`;
    });
}

async function loadOrders() {
    const res = await fetch('/api/orders');
    const data = await res.json();
    const list = document.getElementById('ordersList');
    list.innerHTML = '';
    data.orders.forEach(o => {
        let itemsStr = o.products.map(p => `${p.name} (x${p.quantity})`).join(', ');
        list.innerHTML += `<li><strong>Замовлення ID ${o.id}</strong> (Клієнт ID ${o.client_id})<br>
                           Товари: ${itemsStr}<br>
                           <strong>Сума: ${o.total_sum} грн</strong></li>`;
    });
}

window.onload = () => {
    loadClients();
    loadProducts();
    loadOrders();
};