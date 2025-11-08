import nltk
from collections import Counter
import re

# Verificamos si las stopwords están descargadas
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Ahora sí importamos stopwords después de asegurarnos de que existe
from nltk.corpus import stopwords

# Lista de stopwords en español
spanish_stopwords = set(stopwords.words('spanish'))


def obtener_palabras_clave(comentarios, top_n=10):
    """
    Procesa una lista de comentarios para encontrar las N palabras más comunes.
    """
    all_words = []
    
    for comentario in comentarios:
        # 1. Limpieza: Quitar puntuación, números y convertir a minúsculas
        text = re.sub(r'[^\w\s]', '', comentario.lower()) 
        # 2. Tokenización y filtrado de stopwords y palabras cortas (> 2 letras)
        words = [
            word for word in text.split() 
            if word not in spanish_stopwords and len(word) > 2
        ]
        all_words.extend(words)

    # Contar la frecuencia de cada palabra
    word_counts = Counter(all_words)
    
    # Devolver las top N palabras como una lista de diccionarios (para fácil uso en JSON)
    return [{'word': w, 'count': c} for w, c in word_counts.most_common(top_n)]