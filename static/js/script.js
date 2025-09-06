

const modal = document.getElementById('details-modal');
const transactionMessage = document.getElementById('transaction-message');

/**
 * 
 * @param {number} accountId - O ID da conta a ser detalhada.
 */
async function openDetailsModal(accountId) {
    
    if (!modal) return;
    
    transactionMessage.innerText = '';
    document.getElementById('transaction-valor').value = ''; 
    
    try {
        const response = await fetch(`/accounts/details/${accountId}`);
        if (!response.ok) {
            throw new Error('Falha ao buscar dados da conta.');
        }
        
        const data = await response.json();

        
        document.getElementById('modal-conta-id').value = data.id;
        document.getElementById('modal-nome').innerText = data.holder_name;
        document.getElementById('modal-conta-numero').innerText = data.account_number;
        document.getElementById('modal-saldo').innerText = data.balance.toFixed(2);

        const historyBody = document.getElementById('history-body');
        historyBody.innerHTML = '';
        
        if (data.transactions && data.transactions.length > 0) {
           
            data.transactions.slice().reverse().forEach(t => {
                const row = `<tr>
                                <td>${t.timestamp}</td>
                                <td>${t.type}</td>
                                <td>R$ ${parseFloat(t.amount).toFixed(2)}</td>
                             </tr>`;
                historyBody.innerHTML += row;
            });
        } else {
            historyBody.innerHTML = '<tr><td colspan="3">Nenhuma transação registada.</td></tr>';
        }

        modal.style.display = 'block';
    } catch (error) {
        console.error('Erro:', error);
        alert('Não foi possível carregar os detalhes da conta.');
    }
}


function closeDetailsModal() {
    if (modal) {
        modal.style.display = 'none';
    }
}


window.onclick = function(event) {
    if (event.target == modal) {
        closeDetailsModal();
    }
}

/**
 
 * @param {Event} event - O evento de submit do formulário.
 */
async function handleTransaction(event) {
    event.preventDefault(); 

    const form = event.target;
    const formData = new FormData(form);
    const accountId = formData.get('account_id');
    
    transactionMessage.classList.remove('success', 'error');

    try {
        const response = await fetch('/accounts/transaction', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            const newBalance = parseFloat(result.new_balance).toFixed(2);
            
            document.getElementById(`saldo-${accountId}`).innerText = `R$ ${newBalance}`;
            document.getElementById('modal-saldo').innerText = newBalance;
            
            transactionMessage.innerText = result.message;
            transactionMessage.classList.add('success');
            
            
            openDetailsModal(accountId);
        } else {
            
            transactionMessage.innerText = result.message || 'Ocorreu um erro.';
            transactionMessage.classList.add('error');
        }
    } catch (error) {
        console.error('Erro na transação:', error);
        transactionMessage.innerText = 'Erro de conexão. Tente novamente.';
        transactionMessage.classList.add('error');
    }
}

