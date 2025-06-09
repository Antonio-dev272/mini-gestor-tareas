const API_URL = "http://localhost:5000"; // Cambia si usas docker networks

async function loadBoards() {
  const res = await fetch(`${API_URL}/boards`);
  const boards = await res.json();
  const container = document.getElementById("boards");
  container.innerHTML = "";
  for (const board of boards) {
    const boardDiv = document.createElement("div");
    boardDiv.classList.add("bg-white", "p-4", "rounded", "shadow");
    boardDiv.innerHTML = `<h2 class="text-xl font-semibold mb-2">${board.name}</h2>`;
    container.appendChild(boardDiv);
    loadLists(board.id, boardDiv);
  }
}

async function loadLists(boardId, parentDiv) {
  const res = await fetch(`${API_URL}/boards/${boardId}/lists`);
  const lists = await res.json();
  const listContainer = document.createElement("div");
  listContainer.classList.add("grid", "grid-cols-3", "gap-4");
  for (const list of lists) {
    const listDiv = document.createElement("div");
    listDiv.classList.add("bg-gray-100", "p-2", "rounded");
    listDiv.innerHTML = `<h3 class="font-bold">${list.name}</h3><ul id="tasks-${list.id}" class="pl-4"></ul>`;
    listContainer.appendChild(listDiv);
    loadTasks(list.id);
  }
  parentDiv.appendChild(listContainer);
}

async function loadTasks(listId) {
  const res = await fetch(`${API_URL}/lists/${listId}/tasks`);
  const tasks = await res.json();
  const ul = document.getElementById(`tasks-${listId}`);
  for (const task of tasks) {
    const li = document.createElement("li");
    li.textContent = task.title;
    ul.appendChild(li);
  }
}

async function createBoard() {
  const name = document.getElementById("board-name").value;
  if (!name) return;
  await fetch(`${API_URL}/boards`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });
  document.getElementById("board-name").value = "";
  loadBoards();
}

loadBoards();
