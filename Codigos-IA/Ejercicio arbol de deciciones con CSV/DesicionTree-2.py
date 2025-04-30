import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datasets sin asumir encabezados
file_path = './DecisionTree-1.csv'
dataset = pd.read_csv(file_path)

file_path2 = './DecisionTree-2.csv'
testdata = pd.read_csv(file_path2)

# Asignar nombres genéricos a las columnas para consistencia
dataset.columns = ['feature_1', 'feature_2', 'target']
testdata.columns = ['feature_1', 'feature_2', 'target']

# Dataset 1 (entrenamiento)
X = dataset.iloc[:, :2]  # Características
y = dataset.iloc[:, 2]   # Etiquetas

# Dataset 2 (prueba)
X_datatest = testdata.iloc[:, :2]  # Características
y_datatest = testdata.iloc[:, 2]   # Etiquetas

# Dividir el dataset de entrenamiento (opcional, solo para validación interna)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el clasificador
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Predecir en el dataset de prueba nuevo
y_pred = clf.predict(X_datatest)

# Evaluación
print("Accuracy:", accuracy_score(y_datatest, y_pred))
print("\nReporte de Clasificación:\n", classification_report(y_datatest, y_pred))

# Matriz de confusión
# Obtener clases únicas para las etiquetas
classes = sorted(y_datatest.unique())
cm = confusion_matrix(y_datatest, y_pred, labels=classes)

# Graficar matriz de confusión
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=classes, 
            yticklabels=classes)
plt.xlabel('Predicho')
plt.ylabel('Real')
plt.title('Matriz de Confusión')
plt.show()