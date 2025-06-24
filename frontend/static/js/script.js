const API_URL = "http://localhost:5000/api/cards";

document.addEventListener('DOMContentLoaded', async () => {
  await cargarTarjetas();

  const addButtons = document.querySelectorAll('.add-card-btn');
  addButtons.forEach(button => {
    button.addEventListener('click', async () => {
      const container = button.closest('[data-list]');
      const input = container.querySelector('input');
      const text = input.value.trim();
      if (!text) return;

      const listName = container.getAttribute('data-list');
      const nueva = await agregarTarjeta(text, listName);
      if (nueva) {
        const card = crearTarjeta(nueva);
        container.querySelector('.card-list').appendChild(card);
        input.value = '';
      }
    });
  });

  initDragAndDrop();
});

// Cargar tarjetas existentes desde backend
async function cargarTarjetas() {
  const response = await fetch(API_URL);
  const tarjetas = await response.json();

  tarjetas.forEach(t => {
    const card = crearTarjeta(t);
    const lista = document.querySelector(`[data-list="${t.list}"] .card-list`);
    if (lista) lista.appendChild(card);
  });
}

// Crear tarjeta visual
function crearTarjeta({ id, text, list }) {
  const card = document.createElement('div');
  card.className = 'bg-gray-700 p-3 rounded shadow cursor-pointer flex justify-between items-center group';
  card.draggable = true;
  card.dataset.id = id;

  const span = document.createElement('span');
  span.textContent = text;
  span.className = 'flex-grow';

  // Editar texto
  span.addEventListener('dblclick', async () => {
    const nuevoTexto = prompt('Editar tarjeta:', span.textContent);
    if (nuevoTexto !== null) {
      span.textContent = nuevoTexto.trim();
      await fetch(`${API_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: nuevoTexto.trim(), list })
      });
    }
  });

  // Botón eliminar
  const eliminar = document.createElement('button');
  eliminar.innerHTML = '<i class="ti ti-trash text-lg"></i>';
  eliminar.className = 'text-red-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-opacity ml-2';
  eliminar.title = 'Eliminar tarjeta';
  eliminar.addEventListener('click', async e => {
    e.stopPropagation();
    if (confirm('¿Eliminar esta tarjeta?')) {
      await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      card.remove();
    }
  });

  card.appendChild(span);
  card.appendChild(eliminar);

  agregarEventosDrag(card);
  return card;
}

// Agregar tarjeta al backend
async function agregarTarjeta(texto, lista) {
  const res = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: texto, list: lista })
  });
  return await res.json();
}

// Eventos drag and drop
function agregarEventosDrag(card) {
  card.addEventListener('dragstart', e => {
    card.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
  });

  card.addEventListener('dragend', async () => {
    card.classList.remove('dragging');

    const zona = card.closest('.card-list');
    const lista = zona.closest('[data-list]').getAttribute('data-list');
    const id = card.dataset.id;
    const texto = card.querySelector('span').textContent.trim();

    await fetch(`${API_URL}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: texto, list: lista })
    });
  });
}

function initDragAndDrop() {
  const zonas = document.querySelectorAll('.card-list');

  zonas.forEach(zona => {
    zona.addEventListener('dragover', e => {
      e.preventDefault();
      zona.classList.add('bg-gray-600');
    });

    zona.addEventListener('dragleave', () => {
      zona.classList.remove('bg-gray-600');
    });

    zona.addEventListener('drop', e => {
      e.preventDefault();
      const card = document.querySelector('.dragging');
      if (card && !zona.contains(card)) {
        zona.appendChild(card);
      }
      zona.classList.remove('bg-gray-600');
    });
  });
}
