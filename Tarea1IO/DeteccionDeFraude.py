#Libreria para extaer los datos
import pandas as pd
#Libreria requisito para manejo numerico de sklearn
import numpy as np
#Modelo regresor para poder hacer la red
from sklearn.neural_network import MLPRegressor
#Módulo para separar los datos
from sklearn.model_selection import train_test_split
#Libreria para guardar el modelo
import joblib

#Voy a utilizar el dataset https://www.kaggle.com/datasets/dhanushnarayananr/credit-card-fraud
'''
La cabecera de los datos es:
    distance_from_home
    distance_from_last_transaction
    ratio_to_median_purchase_price
    repeat_retailer
    used_chip
    used_pin_number
    online_order
    fraud
'''
#Para cargar los datos
df = pd.read_csv("./card_transdata.csv")

#La libreria según la documentacion requiere utilizar arreglos para guardar la matriz de entrada y de salida

#Seleccion de los valores de la tabla excepto la ultima columna
#La entrada x es una matriz MxN, N=Numero de ejemplos y M=Entradas
'''
Solo se van a utilizar las siguientes caracteristicas:
ratio_to_median_purchase_price: Ratio medio de compra
repeat_retailer : Minorista habitual
used_chip : Se utilizó chip?
used_pin_number : Se utilizó numero pin?
online_order : Compra online?
'''
x = np.array(df.iloc[:-1, 2:-1], dtype="int64").T

#Seleccion de la ultima columna
y = np.array(df["fraud"], dtype="int64")[:-1]

#Separa los datos en datos de entrenamiento y datos de prueba
X, X_t, Y, Y_t = train_test_split(x.T, y)

#Verifica si ya se entreno previemente un modelo
try:
  #Carga los modelos preentrenados, en caso de que existan, de forma que sea más eficiente para el usuario final: policias, entidades bancarias, forenses, etc.
  modela = joblib.load('modelo_entrenadoa.pkl')
  modelb = joblib.load('modelo_entrenadob.pkl')
except:
  #configuracion de la red, Calculará la probabilidad de que se trate de un fraude.

  modela = MLPRegressor(
    solver="adam",  #Optimizador
    alpha=1e-5,  #Paso de optimización
    hidden_layer_sizes=(10, 5, 2),  #Capas de la red
    activation="logistic")

  #Entrenamiento de la red
  modela.fit(X, Y)
  #Puntuación de la red, mientras mas cercano a 1 es mejor
  print("Score:", modela.score(X, Y))

  #Para guardar el modelo si la puntuación es minimo .7
  if modela.model.score(X, Y) > .7:
    joblib.dump(modela, 'modelo_entrenadoa.pkl')

  #configuracion de la red, Calculará la probabilidad inversa de que se trate de un fraude.
  print("a")
  modelb = MLPRegressor(
    solver="adam",  #Optimizador
    alpha=1e-5,  #Paso de optimización
    hidden_layer_sizes=(10, 5, 2),  #Capas de la red
    activation="logistic")

  #Modificación de la salida
  Y=np.ones(len(Y))-Y
  #Entrenamiento de la red
  modelb.fit(X, Y)
  #Puntuación de la red, mientras mas cercano a 1 es mejor
  
  print("Score:", modelb.score(X, Y))

  #Para guardar el modelo si la puntuación es minimo .7
  if modelb.score(X, Y) > .7:
    joblib.dump(modelb, 'modelo_entrenadob.pkl')


entrada=np.array([[int(input(i + ">>"))for i in ("Ratio medio de compra", "Minorista habitual", "Se utilizó chip?", "Se utilizó numero pin?", "Compra online?")]])

#Primera predicción y Segúnda prediccion
prediccion = np.array([modela.predict(entrada),modelb.predict(entrada)])
#Se aplica una distribución de probabilidad

prediccion=pow(np.e,prediccion)/sum(pow(np.e,prediccion))


##Para retornar una respuesta al usuario se puede verificar cual es la probabilidad mayor con ayuda de argmax
print(["Fraude","No es fraude"][np.argmax(prediccion)])
