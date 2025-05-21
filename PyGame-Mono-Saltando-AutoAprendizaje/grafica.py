import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse
from matplotlib import cm

def graficar_datos(ruta_archivo, features=None, targets=None):
    try:
        # Cargar los datos desde el CSV
        df = pd.read_csv(ruta_archivo)
        
        # Verificar que las columnas sean numéricas
        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.dropna()

        # Verificar columnas necesarias
        required_cols = ['Distancia_Bala', 'Velocidad_Bala', 'Salto', 'Izquierda']
        if not all(col in df.columns for col in required_cols):
            print("Error: El archivo no contiene las columnas requeridas")
            return

        # Crear variable combinada para el eje Z (profundidad)
        df['Accion_Combinada'] = df.apply(lambda row: 
            0 if row['Salto'] == 0 and row['Izquierda'] == 0 else
            1 if row['Salto'] == 1 and row['Izquierda'] == 0 else
            2 if row['Salto'] == 0 and row['Izquierda'] == 1 else
            3,  # Salto=1 e Izquierda=1
            axis=1
        )

        # Configurar el gráfico 3D
        fig = plt.figure(figsize=(14, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Asignar colores según la acción combinada
        colors = cm.jet(df['Accion_Combinada']/3)  # Normalizar a rango [0,1]

        # Crear el gráfico de dispersión 3D
        scatter = ax.scatter(
            df['Velocidad_Bala'],    # Eje X: Velocidad
            df['Distancia_Bala'],    # Eje Y: Distancia
            df['Accion_Combinada'],  # Eje Z: Acción combinada
            c=df['Accion_Combinada'],
            cmap='jet',
            alpha=0.7,
            edgecolors='w',
            s=40
        )

        # Configurar etiquetas y título
        ax.set_xlabel('Velocidad Bala (px/frame)', labelpad=12, fontsize=12)
        ax.set_ylabel('Distancia Bala (px)', labelpad=12, fontsize=12)
        ax.set_zlabel('Acción Combinada', labelpad=12, fontsize=12)
        ax.set_title('Relación 3D: Velocidad vs Distancia vs Acciones Combinadas', 
                    pad=20, fontsize=14, fontweight='bold')

        # Configurar ticks del eje Z
        ax.set_zticks([0, 1, 2, 3])
        ax.set_zticklabels([
            'No acción\n(Salto=0, Izq=0)', 
            'Solo Salto\n(Salto=1, Izq=0)',
            'Solo Izquierda\n(Salto=0, Izq=1)',
            'Ambas acciones\n(Salto=1, Izq=1)'
        ], fontsize=10)

        # Configurar vista inicial
        ax.view_init(elev=25, azim=-45)

        # Añadir barra de color
        cbar = fig.colorbar(scatter, ax=ax, shrink=0.6, aspect=10, pad=0.1)
        cbar.set_label('Acción Combinada', rotation=270, labelpad=15)
        cbar.set_ticks([0, 1, 2, 3])
        cbar.set_ticklabels([
            'No acción', 
            'Solo Salto',
            'Solo Izquierda',
            'Ambas acciones'
        ])

        # Ajustar márgenes
        plt.tight_layout()
        
        # Mostrar el gráfico
        plt.show()

    except Exception as e:
        print(f"Error al graficar los datos: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Graficar datos de entrenamiento del juego.')
    parser.add_argument('ruta_archivo', type=str, help='Ruta al archivo CSV con los datos')
    parser.add_argument('--features', nargs='+', help='Nombres de las columnas de características')
    parser.add_argument('--targets', nargs='+', help='Nombres de las columnas objetivo')
    
    args = parser.parse_args()
    
    print("\nVisualización 3D de Datos de Entrenamiento")
    print(f"Archivo analizado: {args.ruta_archivo}\n")
    
    graficar_datos(args.ruta_archivo, args.features, args.targets)