// js/transfer.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const transferForm = document.getElementById('transferForm');
    transferForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const recipient = document.getElementById('recipient').value;
        const amount = parseFloat(document.getElementById('amount').value);

        const response = await fetch('http://localhost:5000//wallet/transfer', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify({ recipient_username: recipient, amount })
        });

        const data = await response.json();
        const messageDiv = document.getElementById('message');

        if (response.status === 200) {
            messageDiv.innerText = data.message;
            messageDiv.style.color = 'green';
            transferForm.reset();
        } else {
            messageDiv.innerText = data.message;
            messageDiv.style.color = 'red';
        }
    });
});
