
async function loadMetrics() {
    const res = await fetch('/api/metrics');
    const data = await res.json();
    document.getElementById('cpu-percent').innerText = data.cpu + '%';
    document.getElementById('memory-percent').innerText = data.ram + '%';
    document.getElementById('system-cpu').innerText = data.cpu + '%';
    document.getElementById('system-memory').innerText = data.ram + '%';
    document.getElementById('system-disk').innerText = data.disk + '%';
}

async function loadTraffic() {
    const res = await fetch('/api/traffic');
    const data = await res.json();
    const table = document.getElementById('traffic-logs-table');
    table.innerHTML = '';
    data.slice(-10).forEach(log => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${log.timestamp}</td><td>${log.ip}</td><td>${log.method}</td><td>${log.url}</td><td>${log.status}</td><td>${log.user_agent}</td>`;
        table.appendChild(row);
    });
}

setInterval(() => {
    loadMetrics();
    loadTraffic();
}, 5000);

document.getElementById('block-ip-form').addEventListener('submit', async e => {
    e.preventDefault();
    const ip = document.getElementById('ip-to-block').value;
    const reason = document.getElementById('block-reason').value;
    await fetch('/api/block', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ip, reason })
    });
    alert(`IP ${ip} bloqueada`);
});
