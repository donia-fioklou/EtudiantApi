from crypt import methods
from email import message
from itertools import count
from os import abort
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import false
load_dotenv()
app=Flask(__name__)

motdepasse=quote_plus(os.getenv('db.password'))
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:{}@localhost:5432/appg3".format(motdepasse)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Etudiant(db.Model):
    __tablename__='etudiants'
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.String(50),nullable=False)
    prenom=db.Column(db.String(100),nullable=False)
    addresse=db.Column(db.String(100),nullable=True)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
    def delete():
        db.session.delete()
        db.session.commit()
        
        
    

    def format(self):
        return {
            'id':self.id,
            'nom':self.nom,
            'addresse':self.addresse,
            'prenom':self.prenom
        }
db.create_all()



#######################################################
#
#       endpoint liste de tout les etudiants
#
#######################################################
@app.route('/etudiants',methods=['GET'])
def listeEtudiant():
    #recuper la liste des etudeints
    etudiants=Etudiant.query.all()
    etudiantsFormate=[et.format() for et in etudiants]
    return jsonify({
        'success':True,
        'totalEtudiants':len(etudiants),
        'etudiants':etudiantsFormate
    })

#######################################################
#
#       endpoint selectionner un etudiant
#
#######################################################
@app.route('/etudiants/<int:id>')
def selectionnerEtudiant(id):
    #selectionner un etudiant
    etudiant=Etudiant.query.get(id)
    # verfier si l'etudiant exist
    if etudiant is None:
        abort(404) 
        #404 status code pour ressourse n'exist pas
    else:
        return jsonify({
            'succses':True,
            'selected':id,
            'etudiant':etudiant.format()
        })
#######################################################
#
#       endpoint selectionner un etudiant
#
#######################################################
@app.route('/etudiants',methods=['POST'])
def ajouterEtudiant():
    body=request.get_json()#recuperer les donnée json
    newNom=body.get('nom',None) 
    newPrenom=body.get('prenom',None)
    newAddresse=body.get('addresse',None)
    etudiant = Etudiant(nom=newNom,prenom=newPrenom,addresse=newAddresse)
    etudiant.insert()
    return jsonify({
        'succes':True,
        'totalEtudiant':Etudiant.query.count(),
        'etudiant':[et.format()for et in Etudiant.query.all()]
    })
    #######################################################
#
#       endpoint selectionner un etudiant
#
#######################################################
@app.route('/etudiants<int:id>',methods=['DELETE'])
def deleteEtudaint(id):
    etudiant=Etudiant.query.get(id)
    if etudiant is None:
        abort(404)
    else:
        #supprimer la personne
        etudiant.delete()
        return({
            'id':id,
            'sucdess':True,
            'totalEtudiant':Etudiant.query.count()
        })

#######################################################
#
#       endpoint selectionner un etudiant
#
#######################################################
@app.route('/etudiants/<int:id>',methods=['PATCH'])
def modifierEtudaint(id):
    etudiant=Etudiant.query.get(id)
    if etudiant is None:
        abort(404)
    else:
        body=request.get_json()#recuperer les donnée json
        etudiant=Etudiant.query.get(id)
        etudiant.nom=body.get('nom')
        etudiant.prenom=body.get('prenom')
        etudiant.addresse=body.get('addresse')
        etudiant.update()
        return jsonify({
            'success':True,
            'updateId':id,
            'etudiant':etudiant.format()
        })
#recuper un le type d'error et lance l'erreur sous forme json
@app.errorhandler(404)
def serverError(error):
    return jsonify({
        "success":false,
        "error":404,
        "message":"Not Found"
    }),404

    
###
# pip install python-dotenv
### 

    