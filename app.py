from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Definir um modelo de dados para a matriz
matriz = [[0] * 5 for _ in range(5)]

# Rota para exibir a matriz
@app.route('/')
def exibir_matriz():
    return render_template('matriz.html', matriz=matriz)

# Rota para criar uma nova entrada na matriz
@app.route('/nova_entrada', methods=['GET', 'POST'])
def nova_entrada():
    if request.method == 'POST':
        linha = int(request.form['linha'])
        coluna = int(request.form['coluna'])
        valor = int(request.form['valor'])
        matriz[linha][coluna] = valor
        return redirect(url_for('exibir_matriz'))
    else:
        return render_template('nova_entrada.html')

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
    app.run(debug=True)
