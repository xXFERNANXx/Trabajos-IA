# Detección de Vida y Emociones

## Descripción Inicial

- **MediaPipe**: MediaPipe Solutions proporciona un paquete de bibliotecas y herramientas para que apliques rápidamente técnicas de inteligencia artificial (IA) y aprendizaje automático (AA) en tus aplicaciones.
- **Face Landmarks**: Genera una malla facial con 468 puntos 3D que representan la geometría del rostro.
- **Modelos adicionales (embeddings)**: Convertir los rasgos faciales en vectores numéricos (embeddings) para comparación.

## Detección de Emociones

La detección de emociones se puede implementar combinando los landmarks faciales con un modelo de clasificación:

### Proceso de Detección

- **Extracción de Landmarks**: Obtener todos los 468 puntos de referencia faciales.
- **Normalización**: Ajustar las coordenadas para ser invariantes a posición y tamaño.
- **Clasificación**: Usar los landmarks como input a un modelo de ML pre-entrenado.

### Emociones Básicas

- Felicidad (elevación de los labios)
- Tristeza (caída de los labiales)
- Sorpresa (elevación de cejas y apertura ocular)
- Enojo (cejas fruncidas)
- Neutral (sin expresión)

## Implementación de Seguridad (Anti-Spoofing)

Para prevenir ataques con fotos, vídeos o máscaras, se pueden implementar las siguientes técnicas:

### Métodos de Detección de Vitalidad (Liveness Detection)

- **Análisis de Textura**:
  - Detectar patrones de impresión o pantalla
  - Analizar reflectancia de la piel real vs una imagen impresa o similares

- **Movimiento 3D**:
  - Requerir movimientos de cabeza ( movimientos de cabeza, guiños, sonrisa, etc.)
  - Analizar la coherencia de los landmarks en el movimiento 3D

- **Parpadeo**:
  - Detectar el cierre/abertura natural de párpados
  - Frecuencia y completitud del parpadeo
