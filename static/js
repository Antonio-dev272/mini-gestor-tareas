document.addEventListener('DOMContentLoaded', () => {
    const backendUrl = 'http://localhost:5000/api/tasks'; // URL de tu backend Flask

    const taskTitleInput = document.getElementById('task-title');
    const taskDescriptionInput = document.getElementById('task-description');
    const addTaskBtn = document.getElementById('add-task-btn');

    const pendingTasksList = document.getElementById('pending-tasks');
    const inProgressTasksList = document.getElementById('in-progress-tasks');
    const completedTasksList = document.getElementById('completed-tasks');

    // Función para cargar las tareas desde el backend
    async function loadTasks() {
        pendingTasksList.innerHTML = '';
        inProgressTasksList.innerHTML = '';
        completedTasksList.innerHTML = '';

        try {
            const response = await fetch(backendUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const tasks = await response.json();
            
            tasks.forEach(task => {
                const taskItem = createTaskElement(task);
                if (task.status === 'pending') {
                    pendingTasksList.appendChild(taskItem);
                } else if (task.status === 'in-progress') {
                    inProgressTasksList.appendChild(taskItem);
                } else if (task.status === 'completed') {
                    completedTasksList.appendChild(taskItem);
                }
            });
        } catch (error) {
            console.error('Error al cargar las tareas:', error);
            alert('Error al cargar las tareas. Asegúrate de que el backend esté funcionando.');
        }
    }

    // Función para crear un elemento de tarea HTML
    function createTaskElement(task) {
        const li = document.createElement('li');
        li.className = 'task-item';
        li.dataset.taskId = task.id;

        li.innerHTML = `
            <h4>${task.title}</h4>
            <p>${task.description}</p>
            <select class="task-status">
                <option value="pending" ${task.status === 'pending' ? 'selected' : ''}>Pendiente</option>
                <option value="in-progress" ${task.status === 'in-progress' ? 'selected' : ''}>En Progreso</option>
                <option value="completed" ${task.status === 'completed' ? 'selected' : ''}>Completada</option>
            </select>
            <button class="delete-btn">Eliminar</button>
        `;

        // Event listener para el cambio de estado
        li.querySelector('.task-status').addEventListener('change', async (e) => {
            const newStatus = e.target.value;
            await updateTaskStatus(task.id, newStatus);
        });

        // Event listener para el botón eliminar
        li.querySelector('.delete-btn').addEventListener('click', async () => {
            await deleteTask(task.id);
        });

        return li;
    }

    // Función para añadir una nueva tarea
    addTaskBtn.addEventListener('click', async () => {
        const title = taskTitleInput.value.trim();
        const description = taskDescriptionInput.value.trim();

        if (title) {
            try {
                const response = await fetch(backendUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ title, description }),
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const newTask = await response.json();
                // No necesitamos añadirla manualmente, recargamos todas para simplicidad
                loadTasks(); 
                taskTitleInput.value = '';
                taskDescriptionInput.value = '';
            } catch (error) {
                console.error('Error al añadir la tarea:', error);
                alert('Error al añadir la tarea. Asegúrate de que el backend esté funcionando.');
            }
        } else {
            alert('El título de la tarea no puede estar vacío.');
        }
    });

    // Función para actualizar el estado de una tarea
    async function updateTaskStatus(id, newStatus) {
        try {
            const response = await fetch(`${backendUrl}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ status: newStatus }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            loadTasks(); // Recargar todas las tareas para actualizar las listas
        } catch (error) {
            console.error('Error al actualizar la tarea:', error);
            alert('Error al actualizar la tarea. Asegúrate de que el backend esté funcionando.');
        }
    }

    // Función para eliminar una tarea
    async function deleteTask(id) {
        if (confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
            try {
                const response = await fetch(`${backendUrl}/${id}`, {
                    method: 'DELETE',
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                loadTasks(); // Recargar todas las tareas
            } catch (error) {
                console.error('Error al eliminar la tarea:', error);
                alert('Error al eliminar la tarea. Asegúrate de que el backend esté funcionando.');
            }
        }
    }

    // Cargar las tareas al iniciar la aplicación
    loadTasks();
});
