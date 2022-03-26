from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret'


db = SQLAlchemy()
db.init_app(app)

class Tarefa(db.Model):
    __tablename__ = 'tarefas'

    id = db.Column(db.Integer, primary_key=True)
    tarefa = db.Column(db.String(80), nullable=True)
    estado = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.tarefa


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        tarefa = request.form.get('tarefa')
        estado = request.form.get('estado')
        
        if estado == 'on':
            estado = True
        else:
            estado = False

        todo = Tarefa(
            tarefa=tarefa,
            estado=estado
        )
        

        db.session.add(todo)
        db.session.commit()

        return redirect(url_for('tarefas'))

    return render_template('cadastrar.html')

@app.route('/tarefas')
def tarefas():
    tarefas = Tarefa.query.all()
    return render_template('tarefas.html', tarefas=tarefas)

@app.route('/deletar')
@app.route('/deletar/<int:id>')
def deletar(id=None):
    if id != None:
        tarefa = Tarefa.query.get(id)

        db.session.delete(tarefa)
        db.session.commit()

    return redirect(url_for('tarefas'))


@app.route('/editar/<int:id>')
def editar(id=None):
    tarefa = Tarefa.query.get(id)
    return render_template('editar.html', tarefa=tarefa)

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    if request.method == 'POST':
        tarefa = request.form.get('tarefa')
        estado = request.form.get('estado')
        if estado == 'on':
            estado = True
        else:
            estado = False

        todo = Tarefa.query.get(id)
        todo.tarefa = tarefa
        todo.estado = estado

        db.session.commit()

    return redirect(url_for('tarefas'))


if __name__ == '__main__':
    app.run(debug=True)