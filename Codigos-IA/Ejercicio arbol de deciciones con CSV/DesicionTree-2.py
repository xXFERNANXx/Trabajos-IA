# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeClassifier, export_graphviz
# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Cargar el dataset
# file_path = './DecisionTree-1.csv'
# dataset = pd.read_csv(file_path)

# file_path2 = './DecisionTree-2.csv'
# testdata = pd.read_csv(file_path2)

# # Eliminar columnas innecesarias (como la vacía "Unnamed: 3")
# #dataset = dataset.drop(columns=['Unnamed: 3'])

# # Dataset 1
# # Definir características (X) y etiquetas (y)
# X = dataset.iloc[:, :2]  # Las dos primeras columnas son las características
# y = dataset.iloc[:, 2]   # La tercera columna es la etiqueta

# # Dataset 2
# # Definir características (X) y etiquetas (y)
# x2 = testdata.iloc[:, :2]  # Las dos primeras columnas son las características
# y2 = testdata.iloc[:, 2]   # La tercera columna es la etiqueta

# # print(X)
# # Dividir los datos en conjunto de entrenamiento y prueba
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# x2_train, x2_test, y2_train, y2_test = train_test_split(x2, y2, test_size=1, random_state=42)

# # Crear el clasificador de Árbol de Decisión
# clf = DecisionTreeClassifier()

# # Entrenar el modelo
# clf.fit(X_train, y_train)

# y_pred = clf.predict(x2_test)

# # 5. Evaluación
# print("Accuracy:", accuracy_score(y2, y_pred))
# print("\nReporte de Clasificación:\n", classification_report(y2, y_pred))

# # 6. Matriz de confusión
# cm = confusion_matrix(y2, y_pred)
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
#             xticklabels=testdata.target_names,
#             yticklabels=testdata.target_names)
# plt.xlabel('Predicho')
# plt.ylabel('Real')
# plt.title('Matriz de Confusión')
# plt.show()
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