// js/dashboard.js

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

   
    const balanceResponse = await fetch('http://localhost:5000/wallet/balance', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (balanceResponse.status === 200) {
        const balanceData = await balanceResponse.json();
        document.getElementById('walletBalance').innerText = balanceData.wallet_balance.toFixed(2);
    } else {
        alert('Failed to fetch balance. Please login again.');
        localStorage.removeItem('token');
        window.location.href = 'index.html';
    }


    const transactionsResponse = await fetch('http://localhost:5000/wallet/transactions', {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (transactionsResponse.status === 200) {
        const transactions = await transactionsResponse.json();
        const tbody = document.querySelector('#transactionsTable tbody');
        transactions.forEach(tx => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${tx.sender}</td>
                <td>${tx.recipient}</td>
                <td>$${tx.amount.toFixed(2)}</td>
                <td>${new Date(tx.timestamp).toLocaleString()}</td>
                <td>${tx.status}</td>
            `;
            tbody.appendChild(tr);
        });
    } else {
        alert('Failed to fetch transactions.');
    }
});
