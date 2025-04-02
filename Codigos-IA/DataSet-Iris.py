from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# Cargar dataset Iris
iris = load_iris()
X, y = iris.data, iris.target
# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# Normalizar las características (Importante par MLP) 
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# Definir la red neuronal con una capa oculta de 10 neuronas
mlp = MLPClassifier(hidden_layer_sizes=(10), activation='relu', solver='adam', max_iter=500, random_state=42)
# Entrenar modelo
mlp.fit(X_train, y_train)
# Hacer predicciones 
Y_pred = mlp.predict(X_test)
# Evaluar el modelo
accuracy = accuracy_score(y_test, Y_pred)
print(f'\nPrecisión en test: {accuracy:4f}')