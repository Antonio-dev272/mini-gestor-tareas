const API_URL = "http://localhost:5000";

async function fetchBoards() {
  const res = await fetch(`${API_URL}/boards`);
  const boards = await res.json();
  const boardsContainer = document.getElementById("boards");
  boardsContainer.innerHTML = "";

  boards.forEach((board) => {
    const boardCard = document.createElement("div");
    boardCard.className = "bg-white rounded-lg shadow-md p-4";

    const title = document.createElement("h2");
    title.textContent = board.name;
    title.className = "text-xl font-semibold mb-2";

    boardCard.appendChild(title);

    const listsContainer = document.createElement("div");
    listsContainer.className = "space-y-2";
    boardCard.appendChild(listsContainer);

    fetchLists(board.id, listsContainer);

    // Add new list input and button
    const newListInput = document.createElement("input");
    newListInput.placeholder = "Nueva lista";
    newListInput.className =
      "border border-gray-300 rounded-md p-1 w-full mb-2 focus:outline-none focus:ring-2 focus:ring-blue-400";

    const newListButton = document.createElement("button");
    newListButton.textContent = "Agregar lista";
    newListButton.className =
      "bg-green-500 hover:bg-green-600 text-white rounded-md px-2 py-1 text-sm";
    newListButton.onclick = () => {
      createList(board.id, newListInput.value, listsContainer, newListInput);
    };

    boardCard.appendChild(newListInput);
    boardCard.appendChild(newListButton);

    boardsContainer.appendChild(boardCard);
  });
}

async function createBoard() {
  const nameInput = document.getElementById("board-name");
  const name = nameInput.value.trim();
  if (!name) return alert("Ingresa un nombre para el tablero");

  await fetch(`${API_URL}/boards`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });

  nameInput.value = "";
  fetchBoards();
}

async function fetchLists(boardId, container) {
  const res = await fetch(`${API_URL}/boards/${boardId}/lists`);
  const lists = await res.json();
  container.innerHTML = "";

  lists.forEach((list) => {
    const listDiv = document.createElement("div");
    listDiv.className = "bg-gray-100 rounded-md p-2";

    const listTitle = document.createElement("h3");
    listTitle.textContent = list.name;
    listTitle.className = "font-semibold mb-1";

    listDiv.appendChild(listTitle);

    const tasksContainer = document.createElement("div");
    tasksContainer.className = "space-y-1 mb-2";
    listDiv.appendChild(tasksContainer);

    fetchTasks(list.id, tasksContainer);

    // Add new task input and button
    const newTaskInput = document.createElement("input");
    newTaskInput.placeholder = "Nueva tarea";
    newTaskInput.className =
      "border border-gray-300 rounded-md p-1 w-full mb-1 focus:outline-none focus:ring-2 focus:ring-green-400";

    const newTaskButton = document.createElement("button");
    newTaskButton.textContent = "Agregar tarea";
    newTaskButton.className =
      "bg-blue-500 hover:bg-blue-600 text-white rounded-md px-2 py-1 text-sm";
    newTaskButton.onclick = () => {
      createTask(list.id, newTaskInput.value, tasksContainer, newTaskInput);
    };

    listDiv.appendChild(newTaskInput);
    listDiv.appendChild(newTaskButton);

    container.appendChild(listDiv);
  });
}

async function createList(boardId, listName, container, inputElement) {
  if (!listName.trim()) return alert("Ingresa un nombre para la lista");

  await fetch(`${API_URL}/boards/${boardId}/lists`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: listName }),
  });

  inputElement.value = "";
  fetchLists(boardId, container);
}

async function fetchTasks(listId, container) {
  const res = await fetch(`${API_URL}/lists/${listId}/tasks`);
  const tasks = await res.json();
  container.innerHTML = "";

  tasks.forEach((task) => {
    const taskDiv = document.createElement("div");
    taskDiv.className =
      "bg-white rounded-md p-1 text-sm border border-gray-300 shadow-sm";
    taskDiv.textContent = task.title;
    container.appendChild(taskDiv);
  });
}

async function createTask(listId, title, container, inputElement) {
  if (!title.trim()) return alert("Ingresa un título para la tarea");

  await fetch(`${API_URL}/lists/${listId}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  inputElement.value = "";
  fetchTasks(listId, container);
}

window.onload = fetchBoards;
