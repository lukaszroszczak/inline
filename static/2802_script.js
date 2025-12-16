async function updateStatus() {
  const resp = await fetch('/status');
  const data = await resp.json();
  for (let i = 1; i <= 3; i++) {
    document.getElementById(`value-${i}`).textContent = data.numbers[i-1];
    const queueContainer = document.getElementById(`queue-${i}`);
    queueContainer.innerHTML = '';
    data.queues[i-1].forEach(entry => {
      const div = document.createElement('div');
      div.classList.add('flex', 'justify-between');
      div.innerHTML = `<span>${entry.time}</span><span>${entry.number}</span><button class="text-red-500" onclick="removeFromQueue(${i}, ${entry.number})">USUN</button>`;
      queueContainer.appendChild(div);
    });
  }
}

async function increment(office) {
  await fetch(`/office/${office}/increment`, { method: 'POST' });
  updateStatus();
}

async function decrement(office) {
  await fetch(`/office/${office}/decrement`, { method: 'POST' });
  updateStatus();
}

async function reset(office) {
  await fetch(`/office/${office}/reset`, { method: 'POST' });
  updateStatus();
}

async function addNumber(office) {
  await fetch(`/office/${office}/add_number`, { method: 'POST' });
  updateStatus();
}

async function removeFromQueue(office, number) {
  await fetch(`/office/${office}/remove_number`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({number: number})
  });
  updateStatus();
}

document.addEventListener('DOMContentLoaded', updateStatus);
setInterval(updateStatus, 5000);
