from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)

# Definir um modelo de dados para a matriz
matriz = [[0] * 5 for _ in range(5)]

# # configurar a URL de conexão com o banco de dados
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://seu_usuario:sua_senha@localhost/seu_banco_de_dados'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matriz.db'
# initialize the app with the extension
db.init_app(app)

# Definição do modelo MatrizRiscos
class MatrizRiscos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    risco = db.Column(db.String(20))
    descricao = db.Column(db.String(100))
    probabilidade = db.Column(db.String(20))
    severidade = db.Column(db.String(20))
    acoes = db.Column(db.String(100))

    def __init__(self, risco, descricao, probabilidade, severidade, acoes):
        self.risco = risco
        self.descricao = descricao
        self.probabilidade = probabilidade
        self.severidade = severidade
        self.acoes = acoes

with app.app_context():
    db.create_all()

# Rota para exibir a matriz
@app.route('/')
def exibir_matriz():
    return render_template('matriz55.html', matriz=matriz)

# rota para exibir o formulário de nova entrada
@app.route('/nova_entrada')
def exibir_formulario():
    return render_template('nova_entrada.html')

# Rota para criar uma nova entrada na matriz
@app.route('/nova_entrada', methods=['POST'])
def nova_entrada():
    if request.method == 'POST':
        risco = request.form['risco']
        descricao = request.form['descricao']
        probabilidade = request.form['probabilidade']
        severidade = request.form['severidade']
        acoes = request.form['acoes']
        nova_entrada = MatrizRiscos(risco=risco, descricao=descricao, probabilidade=probabilidade, 
                                     severidade=severidade, acoes=acoes)
        db.session.add(nova_entrada)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('matriz55.html')


# Rota para editar uma entrada existente na matriz
@app.route('/editar_entrada/<int:linha>/<int:coluna>', methods=['GET', 'POST'])
def editar_entrada(linha, coluna):
    if request.method == 'POST':
        valor = int(request.form['valor'])
        matriz[linha][coluna] = valor
        return redirect(url_for('exibir_matriz'))
    else:
        valor = matriz[linha][coluna]
        return render_template('editar_entrada.html', linha=linha, coluna=coluna, valor=valor)

# Rota para excluir uma entrada existente na matriz
@app.route('/excluir_entrada/<int:linha>/<int:coluna>')
def excluir_entrada(linha, coluna):
    matriz[linha][coluna] = 0
    return redirect(url_for('exibir_matriz'))

if __name__ == '__main__':
    # db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)