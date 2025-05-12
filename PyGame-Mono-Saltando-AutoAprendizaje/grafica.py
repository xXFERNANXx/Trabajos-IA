import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import argparse
import numpy as np

def graficar_datos(ruta_archivo):
    try:
        # Cargar los datos desde el CSV
        df = pd.read_csv(ruta_archivo)
        
        # Verificar que las columnas sean numéricas
        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.dropna()

        # Verificar qué columnas existen en los datos
        columnas_disponibles = df.columns.tolist()
        print("Columnas disponibles:", columnas_disponibles)

        # Configurar el estilo de los gráficos
        plt.style.use('seaborn')
        sns.set_palette("husl")

        # --------------------------------------------------
        # Gráfico 1: Relación entre Distancia_Bala y Velocidad_Bala con Salto
        if all(col in df.columns for col in ['Distancia_Bala', 'Velocidad_Bala', 'Salto']):
            fig1 = plt.figure(figsize=(12, 6))
            
            # Gráfico 3D
            ax1 = fig1.add_subplot(121, projection='3d')
            
            # Mapear colores según acción
            colors = np.where(df['Salto'] == 1, 'r', 'b')
            
            ax1.scatter(df['Distancia_Bala'], df['Velocidad_Bala'], df['Salto'],
                       c=colors, alpha=0.6, edgecolors='w', s=40)
            
            ax1.set_xlabel('Distancia Bala Horizontal')
            ax1.set_ylabel('Velocidad Bala Horizontal')
            ax1.set_zlabel('Salto')
            ax1.set_title('Relación Salto vs Bala Horizontal')

            # Gráfico 2D
            ax2 = fig1.add_subplot(122)
            sns.scatterplot(data=df, x='Distancia_Bala', y='Velocidad_Bala', 
                           hue='Salto', palette=['blue', 'red'], alpha=0.6, ax=ax2)
            ax2.set_title('Distribución 2D: Salto vs Bala Horizontal')
            plt.tight_layout()
            plt.show()

        # --------------------------------------------------
        # Gráfico 2: Relación entre Distancia_Bala2 y Velocidad_Bala2 con Derecha/Izquierda
        if all(col in df.columns for col in ['Distancia_Bala2', 'Velocidad_Bala2', 'Derecha', 'Izquierda']):
            fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Gráfico para movimiento Derecha
            sns.scatterplot(data=df, x='Distancia_Bala2', y='Velocidad_Bala2',
                           hue='Derecha', palette=['blue', 'green'], alpha=0.6, ax=ax3)
            ax3.set_title('Movimiento Derecha vs Bala Vertical')
            
            # Gráfico para movimiento Izquierda
            sns.scatterplot(data=df, x='Distancia_Bala2', y='Velocidad_Bala2',
                           hue='Izquierda', palette=['blue', 'orange'], alpha=0.6, ax=ax4)
            ax4.set_title('Movimiento Izquierda vs Bala Vertical')
            
            plt.tight_layout()
            plt.show()

        # --------------------------------------------------
        # Gráfico 3: Matriz de correlación
        if len(df.columns) > 1:
            plt.figure(figsize=(10, 8))
            corr = df.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f',
                       annot_kws={"size": 10}, linewidths=.5)
            plt.title('Matriz de Correlación entre Variables')
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.show()

        # --------------------------------------------------
        # Gráfico 4: Distribución de acciones
        if any(col in df.columns for col in ['Salto', 'Derecha', 'Izquierda']):
            acciones = [col for col in ['Salto', 'Derecha', 'Izquierda'] if col in df.columns]
            
            if acciones:
                fig4, axes = plt.subplots(1, len(acciones), figsize=(15, 5))
                if len(acciones) == 1:
                    axes = [axes]
                
                for i, accion in enumerate(acciones):
                    sns.countplot(x=df[accion], ax=axes[i])
                    axes[i].set_title(f'Distribución de {accion}')
                    axes[i].set_xticklabels(['No', 'Sí'])
                
                plt.tight_layout()
                plt.show()

    except Exception as e:
        print(f"Error al graficar los datos: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Graficar datos de entrenamiento del juego.')
    parser.add_argument('ruta_archivo', type=str, help='Ruta al archivo CSV con los datos')
    
    args = parser.parse_args()
    graficar_datos(args.ruta_archivo)