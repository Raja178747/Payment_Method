// js/addMoney.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const addMoneyForm = document.getElementById('addMoneyForm');
    addMoneyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const amount = parseFloat(document.getElementById('amount').value);

        const response = await fetch('http://localhost:5000/wallet/add', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            },
            body: JSON.stringify({ amount })
        });

        const data = await response.json();
        const messageDiv = document.getElementById('message');

        if (response.status === 200) {
            messageDiv.innerText = data.message;
            messageDiv.style.color = 'green';
            addMoneyForm.reset();
            
        } else {
            messageDiv.innerText = data.message;
            messageDiv.style.color = 'red';
        }
    });
});
