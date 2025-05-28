import wikipediaapi
import requests
from bs4 import BeautifulSoup
import json
import os
import random
import time
from googlesearch import search as google_search
from urllib.parse import quote_plus

# Configuración mejorada
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
NUM_ARCHIVOS = 100
TEMAS_PRINCIPALES = {
    "aborto": {
        "query": "autonomía personal aborto ética tecnológica",
        "contra": ["vida humana desde la concepción", "aborto asesinato", "consecuencias negativas del aborto"],
        "favor": ["derecho al aborto", "autonomía corporal mujer", "aborto derechos reproductivos"]
    },
    "eutanasia": {
        "query": "eutanasia dignidad humana inteligencia artificial",
        "contra": ["peligros de la eutanasia", "eutanasia contra la vida", "deslizamiento ético eutanasia"],
        "favor": ["derecho a morir dignamente", "autonomía pacientes terminales", "leyes eutanasia"]
    }
}
POSICIONES = ['a_favor', 'en_contra', 'neutral']

# Crear estructura de carpetas mejorada
def crear_estructura_carpetas():
    base_dir = "./MegaInfo"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    for tema in TEMAS_PRINCIPALES.keys():
        for posicion in POSICIONES:
            path = os.path.join(base_dir, tema, posicion)
            os.makedirs(path, exist_ok=True)

# Wikipedia con manejo de errores mejorado
def obtener_wikipedia(query):
    wiki = wikipediaapi.Wikipedia(
        user_agent=USER_AGENT,
        language='es',
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )
    
    try:
        page = wiki.page(query)
        if not page.exists():
            return None
        
        return {
            "titulo": page.title,
            "texto": page.text[:10000],  # Limitar tamaño
            "url": page.fullurl,
            "tema": query
        }
    except Exception as e:
        print(f"Error Wikipedia ({query}): {str(e)}")
        return None

# Búsqueda web mejorada
def buscar_web(query, num_results=5):
    resultados = []
    try:
        # Usar quote_plus para codificar correctamente la query
        query_encoded = quote_plus(query)
        for url in google_search(query, num=num_results, stop=num_results, pause=2.0):
            try:
                headers = {'User-Agent': USER_AGENT}
                response = requests.get(url, timeout=10, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extraer contenido de manera más robusta
                texto = ' '.join([p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()][:20])
                titulo = soup.title.string if soup.title else "Sin título"
                
                resultados.append({
                    'url': url,
                    'titulo': titulo,
                    'texto': texto[:5000],  # Limitar tamaño
                    'tema': query
                })
            except Exception as e:
                print(f"Error al procesar {url}: {str(e)}")
                continue
    except Exception as e:
        print(f"Error en búsqueda web ({query}): {str(e)}")
    
    return resultados

# Sistema de clasificación mejorado
def clasificar_contenido(contenido):
    if not contenido:
        return 'neutral'
    
    texto = (contenido.get('titulo', '') + ' ' + contenido.get('texto', '')).lower()
    
    # Palabras clave mejoradas y ponderadas
    palabras_favor = {
        'derecho a': 2, 'libertad de': 2, 'autonomía': 3, 'elección': 1,
        'derechos reproductivos': 3, 'muerte digna': 2, 'decisión personal': 2,
        'libertad individual': 2, 'autodeterminación': 3
    }
    
    palabras_contra = {
        'asesinato': 3, 'vida humana': 2, 'derecho a vivir': 2, 'crimen': 2,
        'pecado': 1, 'moralidad': 1, 'asesinato': 3, 'vida inocente': 2,
        'protección de la vida': 2, 'contra la vida': 2
    }
    
    score_favor = sum(peso for palabra, peso in palabras_favor.items() if palabra in texto)
    score_contra = sum(peso for palabra, peso in palabras_contra.items() if palabra in texto)
    
    # Umbrales más estrictos
    if score_favor > 3 and score_favor > score_contra:
        return 'a_favor'
    elif score_contra > 3 and score_contra > score_favor:
        return 'en_contra'
    else:
        return 'neutral'

# Guardar archivo con verificación
def guardar_archivo(tema, posicion, contenido, indice):
    try:
        path = os.path.join("./MegaInfo", tema, posicion, f"doc_{indice}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(contenido, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error guardando archivo: {str(e)}")
        return False

# Proceso principal mejorado
def recolectar_informacion():
    crear_estructura_carpetas()
    contadores = {tema: {pos: 0 for pos in POSICIONES} for tema in TEMAS_PRINCIPALES}
    
    while any(contadores[tema][pos] < NUM_ARCHIVOS//6 for tema in TEMAS_PRINCIPALES for pos in POSICIONES):
        for tema, config in TEMAS_PRINCIPALES.items():
            # Búsquedas específicas para cada posición
            queries = {
                'a_favor': config['favor'],
                'en_contra': config['contra'],
                'neutral': [config['query']]
            }
            
            for posicion, terminos in queries.items():
                if contadores[tema][posicion] >= NUM_ARCHIVOS//6:
                    continue
                
                for termino in terminos:
                    try:
                        # Wikipedia
                        if random.random() < 0.5:  # 50% de probabilidad
                            wiki_data = obtener_wikipedia(termino)
                            if wiki_data:
                                pos_detectada = clasificar_contenido(wiki_data)
                                if pos_detectada == posicion and guardar_archivo(tema, posicion, wiki_data, contadores[tema][posicion]):
                                    contadores[tema][posicion] += 1
                                    print(f"Progreso {tema}: {contadores[tema]}")
                        
                        # Búsqueda web
                        if random.random() < 0.7:  # 70% de probabilidad
                            web_data = buscar_web(termino, num_results=3)
                            for data in web_data:
                                pos_detectada = clasificar_contenido(data)
                                if pos_detectada == posicion and contadores[tema][posicion] < NUM_ARCHIVOS//6:
                                    if guardar_archivo(tema, posicion, data, contadores[tema][posicion]):
                                        contadores[tema][posicion] += 1
                                        print(f"Progreso {tema}: {contadores[tema]}")
                        
                        time.sleep(random.uniform(1, 3))
                        
                    except Exception as e:
                        print(f"Error en término {termino}: {str(e)}")
                        continue

if __name__ == "__main__":
    recolectar_informacion()
    print("Recolección completada. Resumen final:")
    for tema in TEMAS_PRINCIPALES:
        print(f"{tema}: {POSICIONES}")