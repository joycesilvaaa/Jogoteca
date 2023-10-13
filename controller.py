from flask import Flask,render_template, request, redirect, session, flash, url_for

#função global
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria =categoria
        self.console = console

jogo1 = Jogo ('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo ('Xadrez', 'Lógico', 'Tabuleiro')
jogo3 = Jogo ('Mortal Kombat', 'Luta', 'Ps2')
lista = [jogo1, jogo2, jogo3]                                               

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Joyce', 'Joy', '6284')
usuario2 = Usuario('Lais', 'LaLa', '8462')

usuarios = { usuario1.nickname: usuario1,
             usuario2.nickname: usuario2}

app = Flask(__name__)
app.secret_key='jogoteca'

#rota da pagina inicial
@app.route('/')
def index():
    return render_template('lista.html', titulo = 'JOGOS', jogos = lista)

#rota tela do formulario
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #redireciona a pagina para a pagina de login
        return redirect (url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

#rota para criar um novo jogo
@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

#rota da pagina de login
@app.route('/login')
def login():
    #vamos colocar essa variavel para pegar a informação da query string(?proxima=novo)
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

#rota oculta da autenticação
@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if usuario in usuarios:
        if senha ==  usuarios[usuario].senha:
            session['usuario_logado'] = usuarios[usuario].nickname
            flash(usuario +' logado com sucesso!')
            proxima_pagina = request.form.get('proxima')
            if proxima_pagina:
                return redirect(proxima_pagina)
            return redirect (url_for('index'))
        #aparece uma mensagem 
    flash('Usuario não logado!')
    return redirect (url_for('login'))

#rota de deslogar  
@app.route('/logout')
def logout():
    #não salva nenhum dado nos cookies
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect (url_for('index'))



#para fazer rodar a aplicação sem precisar ficar reinicializar toda vez
app.run(debug=True)