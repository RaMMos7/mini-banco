// --- Gerenciamento do Modal ---

const modal = document.getElementById('details-modal');
const transactionMessage = document.getElementById('transaction-message');

// Abre o modal e busca os dados da conta
async function openDetailsModal(contaId) {
    transactionMessage.innerText = ''; // Limpa mensagens anteriores
    document.getElementById('transaction-valor').value = ''; // Limpa o campo de valor
    
    try {
        const response = await fetch(`/conta/get/${contaId}`);
        if (!response.ok) {
            throw new Error('Falha ao buscar dados da conta.');
        }
        const data = await response.json();

        // Preenche os dados do modal
        document.getElementById('modal-conta-id').value = data.id;
        document.getElementById('modal-nome').innerText = data.nome_titular;
        document.getElementById('modal-conta').innerText = data.numero_conta;
        document.getElementById('modal-saldo').innerText = data.saldo;

        // Preenche o histórico de transações
        const historyBody = document.getElementById('history-body');
        historyBody.innerHTML = ''; // Limpa o histórico anterior
        
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

// Fecha o modal
function closeDetailsModal() {
    modal.style.display = 'none';
}

// Fecha o modal se o usuário clicar fora do conteúdo
window.onclick = function(event) {
    if (event.target == modal) {
        closeDetailsModal();
    }
}


// --- Lógica de Transação ---

async function handleTransaction(event) {
    event.preventDefault(); // Impede o recarregamento da página

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
            // Atualiza o saldo na tela principal e no modal
            const novoSaldo = result.novo_saldo;
            document.getElementById(`saldo-${contaId}`).innerText = `R$ ${novoSaldo}`;
            document.getElementById('modal-saldo').innerText = novoSaldo;
            
            // Exibe mensagem de sucesso
            transactionMessage.innerText = result.message;
            transactionMessage.classList.add('success');
            
            // Recarrega os detalhes para atualizar o histórico
            openDetailsModal(contaId);
        } else {
            // Exibe mensagem de erro
            transactionMessage.innerText = result.message || 'Ocorreu um erro.';
            transactionMessage.classList.add('error');
        }
    } catch (error) {
        console.error('Erro na transação:', error);
        transactionMessage.innerText = 'Erro de conexão. Tente novamente.';
        transactionMessage.classList.add('error');
    }
}