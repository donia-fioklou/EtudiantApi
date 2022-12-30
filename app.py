from doctest import debug_script
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus


app=Flask(__name__)
motPasse = quote_plus('password')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:{}@localhost:5432/appg3'.format(motPasse)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Etudiant(db.Model):
    __tablename__='etudiants'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    addresse=db.Column(db.String(100),nullable=True)

db.create_all()
#liste de tout les etudiant dans la base
@app.route('/')
def getAllStudents():
    etudiants=Etudiant.query.all()
    return render_template('index.html',data=etudiants)

@app.route('/create')
def afficherForm():
    return render_template('create.html')

@app.route('/add ',methods=['GET','POST'])
def ajouter_etudiant():
    try:
        if request.method =='GET':
            return render_template('create.html')
        elif request.method =='POST':
            new_nom=request.form.get('nom','')
            new_prenom=request.form.get('prenom','')
            new_addresse=request.form.get('adresse','')
            etudiant=Etudiant(nom=new_nom,prenom=new_prenom,addresse=new_addresse)
            db.session.add(etudiant)
            db.session.commit()
            return redirect(url_for('getAllStudents'))
    except:
        db.session.rollback()
    finally:
        db.session.close()
    
    
"""les achitecture
graphful
restfull
"""
