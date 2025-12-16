async function updateStatus() {
  const resp = await fetch('/status');
  const data = await resp.json();

  // data.numbers -> [gab1, gab2, gab3]
  // data.queues -> [ [ {time,number,note}, ...], [ ... ], [ ... ] ]

  for (let i = 1; i <= 3; i++) {
    // Ustawiamy główną wartość licznika
    document.getElementById(`value-${i}`).textContent = data.numbers[i-1];

    // Wypełniamy kolejkę
    const queueContainer = document.getElementById(`queue-${i}`);
    queueContainer.innerHTML = '';
    data.queues[i-1].forEach(entry => {
      // entry: {time, number, note}
      const div = document.createElement('div');
      div.classList.add('flex', 'justify-between', 'items-center', 'mb-2');

      // Treść do wstawienia
      // Pokażemy time, number i note oraz dwa przyciski: Edytuj i USUN
      div.innerHTML = `
        <div>
          <span class="mr-4">${entry.time}</span>
          <span class="mr-4">Nr: ${entry.number}</span>
          <span class="italic text-gray-600">"${entry.note}"</span>
        </div>
        <div>
          <button class="text-blue-500 underline mr-3" onclick="editNumberNote(${i}, ${entry.number})">Edytuj</button>
          <button class="text-red-500 underline" onclick="removeFromQueue(${i}, ${entry.number})">USUN</button>
        </div>
      `;
      queueContainer.appendChild(div);
    });
  }
}

// Funkcje akcji:
async function increment(officeId) {
  await fetch(`/office/${officeId}/action/increment`, { method: 'POST' });
  updateStatus();
}

async function decrement(officeId) {
  await fetch(`/office/${officeId}/action/decrement`, { method: 'POST' });
  updateStatus();
}

async function reset(officeId) {
  await fetch(`/office/${officeId}/action/reset`, { method: 'POST' });
  updateStatus();
}

async function addNumber(officeId) {
  await fetch(`/office/${officeId}/action/add_number`, { method: 'POST' });
  updateStatus();
}

async function removeFromQueue(officeId, number) {
  await fetch(`/office/${officeId}/action/remove_number`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ number: number })
  });
  updateStatus();
}

async function editNumberNote(officeId, number) {
  // Zapytaj użytkownika o nową treść adnotacji
  const note = prompt("Podaj nową adnotację:");
  if (note !== null) {
    await fetch(`/office/${officeId}/action/edit_number`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ number, note })
    });
    updateStatus();
  }
}

// Na starcie ładujemy dane
document.addEventListener('DOMContentLoaded', updateStatus);
// I co 5 sekund odświeżamy
setInterval(updateStatus, 5000);
