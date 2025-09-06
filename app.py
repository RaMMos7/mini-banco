

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import threading

app = Flask(__name__)


data_lock = threading.Lock()
contas_db = {} 
ultima_conta_id = 0

def gerar_novo_id():
    """ Gera um novo ID de conta de forma segura. """
    global ultima_conta_id
    with data_lock:
        ultima_conta_id += 1
        return ultima_conta_id



@app.route('/')
def index():
    """ Rota principal que exibe todas as contas. """
    contas_ordenadas = sorted(list(contas_db.values()), key=lambda c: c['nome_titular'])
    return render_template('index.html', contas=contas_ordenadas)

@app.route('/conta/add', methods=['POST'])
def add_conta():
    """ Rota para adicionar uma nova conta. """
    nome_titular = request.form['nome_titular']
    numero_conta = request.form['numero_conta']
    saldo_inicial = float(request.form['saldo_inicial'] or 0.0)

    if any(c['numero_conta'] == numero_conta for c in contas_db.values()):
        return redirect(url_for('index'))

    novo_id = gerar_novo_id()
    nova_conta = {
        'id': novo_id,
        'nome_titular': nome_titular,
        'numero_conta': numero_conta,
        'saldo': saldo_inicial,
        'transacoes': []
    }
    
    if saldo_inicial > 0:
        nova_conta['transacoes'].append({
            'tipo': 'Depósito Inicial',
            'valor': saldo_inicial,
            'timestamp': datetime.utcnow()
        })
    
    with data_lock:
        contas_db[novo_id] = nova_conta
        
    return redirect(url_for('index'))

@app.route('/conta/delete/<int:id>')
def delete_conta(id):
    """ Rota para deletar uma conta. """
    with data_lock:
        if id in contas_db:
            del contas_db[id]
    return redirect(url_for('index'))


@app.route('/transacao', methods=['POST'])
def realizar_transacao():
    """ Rota para realizar um depósito ou saque. """
    conta_id = int(request.form['conta_id'])
    tipo_transacao = request.form['tipo_transacao']
    valor = float(request.form['valor'])

    with data_lock:
        conta = contas_db.get(conta_id)

        if not conta or valor <= 0:
            return jsonify({'success': False, 'message': 'Dados inválidos.'}), 400

        if tipo_transacao == 'deposito':
            conta['saldo'] += valor
            transacao_tipo = 'Depósito'
        elif tipo_transacao == 'saque':
            if conta['saldo'] < valor:
                return jsonify({'success': False, 'message': 'Saldo insuficiente.'}), 400
            conta['saldo'] -= valor
            transacao_tipo = 'Saque'
        else:
            return jsonify({'success': False, 'message': 'Tipo de transação inválido.'}), 400
        
        conta['transacoes'].append({
            'tipo': transacao_tipo,
            'valor': valor,
            'timestamp': datetime.utcnow()
        })

        return jsonify({
            'success': True,
            'novo_saldo': f"{conta['saldo']:.2f}",
            'message': f'{tipo_transacao.capitalize()} realizado com sucesso!'
        })


@app.route('/conta/get/<int:id>')
def get_conta_details(id):
    """ Retorna os detalhes e transações de uma conta em formato JSON. """
    conta = contas_db.get(id)
    if not conta:
        return jsonify({'error': 'Conta não encontrada'}), 404
    
    transacoes_formatadas = []
    transacoes_ordenadas = sorted(conta['transacoes'], key=lambda t: t['timestamp'], reverse=True)
    
    for t in transacoes_ordenadas:
        transacoes_formatadas.append({
            'tipo': t['tipo'],
            'valor': f"{t['valor']:.2f}",
            'timestamp': t['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
        })

    return jsonify({
        'id': conta['id'],
        'nome_titular': conta['nome_titular'],
        'numero_conta': conta['numero_conta'],
        'saldo': f"{conta['saldo']:.2f}",
        'transacoes': transacoes_formatadas
    })

if __name__ == '__main__':
    app.run(debug=True)