from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from services.user_service import UserService
from services.account_service import AccountService # Importar o novo serviço
from functools import wraps

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta-muito-forte-e-dificil-de-adivinhar' 
user_service = UserService()
account_service = AccountService() # Instanciar o serviço de contas

# --- Decorators para Controlo de Acesso ---
def login_required(f):
    """ Garante que o utilizador esteja autenticado para aceder à rota. """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('É necessário estar autenticado para aceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """ Garante que o utilizador seja um administrador. """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Acesso negado.', 'danger')
            return redirect(url_for('login'))
        if not session.get('is_admin'):
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('dashboard')) # Redireciona para o dashboard
        return f(*args, **kwargs)
    return decorated_function

# --- Rotas de Autenticação e Utilizador (já existentes) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = user_service.authenticate(email, password)
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['is_admin'] = user.is_admin
            flash('Login efetuado com sucesso!', 'success')
            return redirect(url_for('dashboard')) # Redireciona para o novo dashboard
        else:
            flash('Email ou palavra-passe inválidos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if user_service.find_by_email(email):
            flash('Este email já se encontra registado.', 'warning')
        else:
            user_service.create_user(name, email, password)
            flash('Registo efetuado com sucesso! Por favor, inicie a sessão.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sessão terminada com sucesso.', 'info')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    user = user_service.find_by_id(session['user_id'])
    return render_template('profile.html', user=user)

# --- ROTAS NOVAS E ATUALIZADAS PARA O MINI BANCO ---

@app.route('/dashboard')
@login_required
def dashboard():
    """ Rota principal que mostra as contas do utilizador. """
    user_id = session['user_id']
    accounts = account_service.get_accounts_for_user(user_id)
    return render_template('dashboard.html', accounts=accounts)

@app.route('/accounts/add', methods=['POST'])
@login_required
def add_account():
    """ Rota para adicionar uma nova conta bancária. """
    user_id = session['user_id']
    holder_name = request.form['holder_name']
    account_number = request.form['account_number']
    initial_balance = float(request.form.get('initial_balance') or 0.0)
    
    account_service.create_account(user_id, holder_name, account_number, initial_balance)
    flash('Nova conta bancária criada com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/accounts/delete/<int:account_id>', methods=['POST'])
@login_required
def delete_account(account_id):
    """ Rota para eliminar uma conta. """
    user_id = session['user_id']
    success = account_service.delete_account(account_id, user_id)
    if success:
        flash('Conta eliminada com sucesso.', 'success')
    else:
        flash('Erro ao eliminar a conta.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/accounts/details/<int:account_id>')
@login_required
def get_account_details(account_id):
    """ Rota chamada pelo JavaScript para obter os detalhes de uma conta. """
    user_id = session['user_id']
    account = account_service.find_account_by_id(account_id, user_id)
    if not account:
        return jsonify({'error': 'Conta não encontrada'}), 404
    return jsonify(account.to_dict())

@app.route('/accounts/transaction', methods=['POST'])
@login_required
def make_transaction():
    """ Rota chamada pelo JavaScript para fazer depósitos e saques. """
    user_id = session['user_id']
    account_id = request.form['account_id']
    transaction_type = request.form['transaction_type']
    amount = request.form['amount']

    account, message = account_service.perform_transaction(int(account_id), user_id, transaction_type, amount)

    if account:
        return jsonify({'success': True, 'message': message, 'new_balance': account.balance})
    else:
        return jsonify({'success': False, 'message': message}), 400

# --- Rotas de Admin (manter como estão) ---
@app.route('/admin')
@admin_required
def admin_dashboard():
    all_users = user_service.get_all_users()
    return render_template('admin_dashboard.html', users=all_users)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    if user_id == session.get('user_id'):
        flash('Não pode eliminar a sua própria conta de administrador.', 'warning')
        return redirect(url_for('admin_dashboard'))
    user_service.delete_user(user_id)
    flash(f'O utilizador com o ID {user_id} foi eliminado.', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

