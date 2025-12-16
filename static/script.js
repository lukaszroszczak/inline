async function updateStatus() {
  const resp = await fetch('/status');
  const data = await resp.json();

  // data.numbers -> [gab1, gab2, gab3]
  // data.queues -> [ [ {time, number, note}, ... ], [ ... ], [ ... ] ]

  for (let i = 1; i <= 3; i++) {
    // Ustawiamy liczbę w polu #value-i
    document.getElementById(`value-${i}`).textContent = data.numbers[i-1];

    // Wypełniamy kolejkę
    const queueContainer = document.getElementById(`queue-${i}`);
    queueContainer.innerHTML = '';
    data.queues[i-1].forEach(entry => {
      const div = document.createElement('div');
      div.classList.add('flex', 'justify-between', 'items-center', 'mb-2');

      // entry.time, entry.number, entry.note
      div.innerHTML = `
        <div>
          <span class="mr-4">${entry.time}</span>
          <span class="mr-4">Nr: ${entry.number}</span>
          <span class="italic text-gray-600">"${entry.note}"</span>
        </div>
        <div>
          <button class="text-blue-500 underline mr-2" onclick="editNumberNote(${i}, ${entry.number})">Edytuj</button>
          <button class="text-red-500 underline" onclick="removeFromQueue(${i}, ${entry.number})">Usuń</button>
        </div>
      `;
      queueContainer.appendChild(div);
    });
  }
}

// Funkcje sterujące licznikiem:
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

// Dodawanie numeru z notatką
async function addNumber(officeId) {
  const noteInput = document.getElementById(`note-${officeId}`);
  const note = noteInput.value;
  await fetch(`/office/${officeId}/action/add_number`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ note })
  });
  updateStatus();
  // Wyzeruj pole
  noteInput.value = '';
}

async function removeFromQueue(officeId, number) {
  await fetch(`/office/${officeId}/action/remove_number`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ number })
  });
  updateStatus();
}

async function editNumberNote(officeId, number) {
  const newNote = prompt("Podaj nową notatkę:");
  if (newNote !== null) {
    await fetch(`/office/${officeId}/action/edit_number`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ number, note: newNote })
    });
    updateStatus();
  }
}

// Inicjalizacja
document.addEventListener('DOMContentLoaded', updateStatus);
setInterval(updateStatus, 200);
