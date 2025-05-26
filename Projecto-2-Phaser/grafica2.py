import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

def graficar_datos(ruta_archivo):
    try:
        # Cargar los datos desde el CSV
        df = pd.read_csv(ruta_archivo)  # No uses header=None ni names
        
        # Verificar que las columnas sean numéricas
        df = df.apply(pd.to_numeric, errors='coerce')  # Convierte a numérico, errores a NaN
        
        # Eliminar filas con valores NaN (opcional)
        df = df.dropna()

        # Crear la figura 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Graficar puntos con Salto=0
        ax.scatter(df[df['Salto'] == 0]['Distancia'],  # Eje X: Distancia
                   df[df['Salto'] == 0]['Velocidad'], # Eje Y: Velocidad
                   df[df['Salto'] == 0]['Salto'],     # Eje Z: Salto
                   c='blue', marker='o', label='Salto=0')

        # Graficar puntos con Salto=1
        ax.scatter(df[df['Salto'] == 1]['Distancia'],  # Eje X: Distancia
                   df[df['Salto'] == 1]['Velocidad'], # Eje Y: Velocidad
                   df[df['Salto'] == 1]['Salto'],     # Eje Z: Salto
                   c='red', marker='x', label='Salto=1')

        # Etiquetas de los ejes
        ax.set_xlabel('Distancia')
        ax.set_ylabel('Velocidad')
        ax.set_zlabel('Salto')

        # Mostrar leyenda
        ax.legend()

        # Mostrar el gráfico
        plt.show()

    except Exception as e:
        print(f"Error al cargar o graficar los datos: {e}")

if __name__ == "__main__":
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Graficar datos desde un archivo CSV.')
    parser.add_argument('ruta_archivo', type=str, help='Ruta del archivo CSV a graficar')
    
    # Obtener los argumentos
    args = parser.parse_args()
    
    # Llamar a la función de graficación
    graficar_datos(args.ruta_archivo)