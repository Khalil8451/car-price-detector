from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

car = pd.read_csv('clean_final.csv')
car['puissance_fiscale'] = car['puissance_fiscale'].astype(int)
X = car[['marque', 'modele', 'puissance_fiscale', 'kilometrage', 'annee', 'energie', 'boite']]
y = car['prix']

ohe = OneHotEncoder()
ohe.fit(car[['marque', 'modele', 'energie', 'boite']])
column_trans = make_column_transformer(
    (OneHotEncoder(categories=ohe.categories_), ['marque', 'modele', 'energie', 'boite']),
    remainder='passthrough'
)
pipe_tree = make_pipeline(column_trans, DecisionTreeClassifier())
pipe_tree.fit(X, y)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    marque = data['marque']
    modele = data['modele']
    puissance_fiscale = int(data['puissance_fiscale'])
    kilometrage = int(data['kilometrage'])
    annee = int(data['annee'])
    energie = data['energie']
    boite = data['boite']

    # Make prediction
    prix = pipe_tree.predict(pd.DataFrame(columns=X.columns, data=np.array([marque, modele, puissance_fiscale, kilometrage, annee, energie, boite]).reshape(1, 7)))[0]
    response = jsonify({'prix': float(prix)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    
    return response

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)