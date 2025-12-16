// (1) Ładuje stan z /status i aktualizuje elementy w index.html
async function updateStatus() {
  const resp = await fetch('/status');
  const data = await resp.json();

  // data.numbers -> [liczba_gab1, liczba_gab2, liczba_gab3]
  // data.queues -> [ [ {time, number}, ... ], [ ... ], [ ... ] ]

  for (let i = 1; i <= 3; i++) {
    // Ustawiamy liczbę w polu #value-i
    document.getElementById(`value-${i}`).textContent = data.numbers[i-1];

    // Wypełniamy kolejkę
    const queueContainer = document.getElementById(`queue-${i}`);
    queueContainer.innerHTML = '';
    data.queues[i-1].forEach(entry => {
      const div = document.createElement('div');
      div.classList.add('flex', 'justify-between');
      div.innerHTML = `
        <span>${entry.time}</span>
        <span>${entry.number}</span>
        <button class="text-red-500" onclick="removeFromQueue(${i}, ${entry.number})">USUN</button>
      `;
      queueContainer.appendChild(div);
    });
  }
}

// (2) Funkcje do akcji
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

// (3) Uruchamiamy updateStatus po załadowaniu i co 5 sekund
document.addEventListener('DOMContentLoaded', updateStatus);
setInterval(updateStatus, 5000);
