document.addEventListener('DOMContentLoaded', () => {
  const addButtons = document.querySelectorAll('.add-card-btn');

  addButtons.forEach(button => {
    button.addEventListener('click', () => {
      const container = button.closest('[data-list]');
      const input = container.querySelector('input');
      const text = input.value.trim();
      if (!text) return;

      const card = createCard(text);
      const list = container.querySelector('.card-list');
      list.appendChild(card);
      input.value = '';
    });
  });

  initDragAndDrop();

  // 🔧 Agregar eventos a las tarjetas que ya están en el HTML
  const existingCards = document.querySelectorAll('.card-list > div');
  existingCards.forEach(card => {
    addDragEvents(card);
  });
});

// Crea una tarjeta con edición y eliminación
function createCard(text) {
  const card = document.createElement('div');
  card.className = 'bg-gray-700 p-3 rounded shadow cursor-pointer flex justify-between items-center group';
  card.draggable = true;

  const span = document.createElement('span');
  span.textContent = text;
  span.className = 'flex-grow';

  // Doble clic para editar el texto
  span.addEventListener('dblclick', () => {
    const newText = prompt('Editar tarjeta:', span.textContent);
    if (newText !== null) {
      span.textContent = newText.trim();
    }
  });

  // Botón de eliminar
  const deleteBtn = document.createElement('button');
  deleteBtn.innerHTML = '<i class="ti ti-trash text-lg"></i>';
  deleteBtn.className = 'text-red-400 hover:text-red-600 opacity-0 group-hover:opacity-100 transition-opacity ml-2';
  deleteBtn.title = 'Eliminar tarjeta';
  deleteBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    if (confirm('¿Estás seguro de eliminar esta tarjeta?')) {
      card.remove();
    }
  });

  card.appendChild(span);
  card.appendChild(deleteBtn);

  addDragEvents(card);
  return card;
}

// Eventos de arrastrar una tarjeta
function addDragEvents(card) {
  card.addEventListener('dragstart', e => {
    card.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', '');
  });

  card.addEventListener('dragend', () => {
    card.classList.remove('dragging');
  });
}

// Configura las listas para recibir tarjetas
function initDragAndDrop() {
  const dropzones = document.querySelectorAll('.card-list');

  dropzones.forEach(zone => {
    zone.addEventListener('dragover', e => {
      e.preventDefault();
      zone.classList.add('bg-gray-600');
    });

    zone.addEventListener('dragleave', () => {
      zone.classList.remove('bg-gray-600');
    });

    zone.addEventListener('drop', e => {
      e.preventDefault();
      const dragging = document.querySelector('.dragging');
      if (dragging) {
        zone.appendChild(dragging);
      }
      zone.classList.remove('bg-gray-600');
    });
  });
}

