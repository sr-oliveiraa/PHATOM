from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data", "consultores.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Consultor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    prioridade = db.Column(db.String(10), nullable=False)

@app.route('/')
def painel():
    consultores = Consultor.query.all()
    return render_template('panel.html', consultores=consultores)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        nome = request.form['nome']
        data = request.form['data']
        quantidade = request.form['quantidade']
        prioridade = request.form['prioridade']
        novo_consultor = Consultor(nome=nome, data=data, quantidade=quantidade, prioridade=prioridade)
        db.session.add(novo_consultor)
        db.session.commit()
        return redirect(url_for('admin'))
    consultores = Consultor.query.all()
    return render_template('admin.html', consultores=consultores)

@app.route('/delete/<int:id>')
def delete(id):
    consultor = Consultor.query.get_or_404(id)
    db.session.delete(consultor)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    if not os.path.exists(os.path.join(basedir, 'data')):
        os.makedirs(os.path.join(basedir, 'data'))
    
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
