

const modal = document.getElementById('details-modal');
const transactionMessage = document.getElementById('transaction-message');

async function openDetailsModal(contaId) {
    transactionMessage.innerText = '';
    document.getElementById('transaction-valor').value = ''; 
    
    try {
        const response = await fetch(`/conta/get/${contaId}`);
        if (!response.ok) {
            throw new Error('Falha ao buscar dados da conta.');
        }
        const data = await response.json();

     
        document.getElementById('modal-conta-id').value = data.id;
        document.getElementById('modal-nome').innerText = data.nome_titular;
        document.getElementById('modal-conta').innerText = data.numero_conta;
        document.getElementById('modal-saldo').innerText = data.saldo;

       
        const historyBody = document.getElementById('history-body');
        historyBody.innerHTML = '';
        
        if (data.transacoes.length > 0) {
            data.transacoes.forEach(t => {
                const row = `<tr>
                                <td>${t.timestamp}</td>
                                <td>${t.tipo}</td>
                                <td>R$ ${t.valor}</td>
                             </tr>`;
                historyBody.innerHTML += row;
            });
        } else {
            historyBody.innerHTML = '<tr><td colspan="3">Nenhuma transação registrada.</td></tr>';
        }

        modal.style.display = 'block';
    } catch (error) {
        console.error('Erro:', error);
        alert('Não foi possível carregar os detalhes da conta.');
    }
}


function closeDetailsModal() {
    modal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modal) {
        closeDetailsModal();
    }
}

async function handleTransaction(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const contaId = formData.get('conta_id');
    
    transactionMessage.classList.remove('success', 'error');

    try {
        const response = await fetch('/transacao', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            
            const novoSaldo = result.novo_saldo;
            document.getElementById(`saldo-${contaId}`).innerText = `R$ ${novoSaldo}`;
            document.getElementById('modal-saldo').innerText = novoSaldo;
            
            transactionMessage.innerText = result.message;
            transactionMessage.classList.add('success');
            
            openDetailsModal(contaId);
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