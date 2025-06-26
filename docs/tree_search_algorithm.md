# Algoritmo de Búsqueda en Árbol para Análisis de Sentimientos

## Introducción

La búsqueda en árbol es un algoritmo fundamental para recorrer estructuras de datos jerárquicas. En nuestro sistema de análisis de sentimientos, utilizamos un **árbol de decisión** donde cada nodo representa una condición que se evalúa para determinar el sentimiento de un texto.

## Conceptos Básicos

### Estructura de un Nodo

```python
class TreeNode:
    def __init__(self, id, condition, description, true_branch, false_branch, sentiment_scores):
        self.id = id                    # Identificador único
        self.condition = condition      # Función a evaluar
        self.description = description  # Descripción del nodo
        self.true_branch = true_branch  # Nodo siguiente si condición es True
        self.false_branch = false_branch # Nodo siguiente si condición es False
        self.sentiment_scores = sentiment_scores  # Puntuaciones de sentimientos
```

### Tipos de Nodos

- **Nodo Interno**: Tiene ramas (true_branch y false_branch)
- **Nodo Hoja**: No tiene ramas (true_branch = false_branch = None)

## Algoritmos de Búsqueda

### 1. Búsqueda en Profundidad (DFS - Depth First Search)

#### Implementación Recursiva

```python
def depth_first_search(node, text_tokens, accumulated_scores=None):
    """
    Búsqueda en profundidad recursiva del árbol de decisión.
  
    Args:
        node: Nodo actual del árbol
        text_tokens: Lista de tokens del texto a analizar
        accumulated_scores: Puntuaciones acumuladas hasta el momento
  
    Returns:
        dict: Puntuaciones finales de sentimientos
    """
    if accumulated_scores is None:
        accumulated_scores = {
            'alegria': 0.0, 'tristeza': 0.0, 'enojo': 0.0,
            'preocupacion': 0.0, 'informacion': 0.0, 'sorpresa': 0.0
        }
  
    # Acumular puntuaciones del nodo actual
    for sentiment, score in node.sentiment_scores.items():
        accumulated_scores[sentiment] += score
  
    # Si es nodo hoja, retornar resultados
    if node.true_branch is None and node.false_branch is None:
        return accumulated_scores
  
    # Evaluar condición del nodo
    condition_result = evaluate_condition(node.condition, text_tokens)
  
    # Continuar búsqueda según resultado
    if condition_result:
        next_node = get_node_by_id(node.true_branch)
    else:
        next_node = get_node_by_id(node.false_branch)
  
    return depth_first_search(next_node, text_tokens, accumulated_scores)
```

#### Ejemplo de Uso

```python
# Ejemplo: "Estoy muy feliz hoy"
text = "Estoy muy feliz hoy"
tokens = preprocess_text(text)  # ['estoy', 'muy', 'feliz', 'hoy']

# Iniciar búsqueda desde la raíz
root_node = get_node_by_id("root")
results = depth_first_search(root_node, tokens)

print("Resultados:", results)
# Output: {'alegria': 0.85, 'tristeza': 0.0, 'enojo': 0.0, 
#          'preocupacion': 0.0, 'informacion': 0.15, 'sorpresa': 0.0}
```

### 2. Búsqueda Iterativa con Pila

#### Implementación con Stack

```python
def iterative_depth_first_search(root_node, text_tokens):
    """
    Búsqueda en profundidad iterativa usando una pila.
  
    Args:
        root_node: Nodo raíz del árbol
        text_tokens: Lista de tokens del texto
  
    Returns:
        dict: Puntuaciones finales de sentimientos
    """
    stack = [(root_node, {
        'alegria': 0.0, 'tristeza': 0.0, 'enojo': 0.0,
        'preocupacion': 0.0, 'informacion': 0.0, 'sorpresa': 0.0
    })]
  
    while stack:
        current_node, accumulated_scores = stack.pop()
      
        # Acumular puntuaciones
        for sentiment, score in current_node.sentiment_scores.items():
            accumulated_scores[sentiment] += score
      
        # Si es nodo hoja, continuar con siguiente nodo en pila
        if current_node.true_branch is None and current_node.false_branch is None:
            continue
      
        # Evaluar condición
        condition_result = evaluate_condition(current_node.condition, text_tokens)
      
        # Agregar siguiente nodo a la pila
        if condition_result:
            next_node = get_node_by_id(current_node.true_branch)
        else:
            next_node = get_node_by_id(current_node.false_branch)
      
        stack.append((next_node, accumulated_scores.copy()))
  
    return accumulated_scores
```

### 3. Búsqueda con Backtracking

#### Implementación con Backtracking

```python
def backtracking_search(node, text_tokens, path=None, best_scores=None):
    """
    Búsqueda con backtracking para encontrar múltiples caminos posibles.
  
    Args:
        node: Nodo actual
        text_tokens: Tokens del texto
        path: Camino actual recorrido
        best_scores: Mejores puntuaciones encontradas
  
    Returns:
        dict: Mejores puntuaciones encontradas
    """
    if path is None:
        path = []
    if best_scores is None:
        best_scores = {
            'alegria': 0.0, 'tristeza': 0.0, 'enojo': 0.0,
            'preocupacion': 0.0, 'informacion': 0.0, 'sorpresa': 0.0
        }
  
    # Agregar nodo actual al camino
    path.append(node.id)
  
    # Acumular puntuaciones
    current_scores = sum_scores(path)
  
    # Si es nodo hoja, evaluar si es mejor resultado
    if node.true_branch is None and node.false_branch is None:
        if is_better_solution(current_scores, best_scores):
            best_scores = current_scores.copy()
        return best_scores
  
    # Evaluar condición
    condition_result = evaluate_condition(node.condition, text_tokens)
  
    # Explorar rama correspondiente
    if condition_result:
        next_node = get_node_by_id(node.true_branch)
    else:
        next_node = get_node_by_id(node.false_branch)
  
    best_scores = backtracking_search(next_node, text_tokens, path, best_scores)
  
    # Backtrack: remover nodo actual del camino
    path.pop()
  
    return best_scores
```

## Funciones de Evaluación de Condiciones

### 1. Evaluación de Palabras Clave

```python
def evaluate_condition(condition_name, text_tokens):
    """
    Evalúa una condición específica basada en los tokens del texto.
  
    Args:
        condition_name: Nombre de la condición a evaluar
        text_tokens: Lista de tokens del texto
  
    Returns:
        bool: Resultado de la evaluación
    """
    condition_functions = {
        'has_emotion_words': has_emotion_words,
        'has_positive_words': has_positive_words,
        'has_negative_words': has_negative_words,
        'has_joy_words': has_joy_words,
        'has_sadness_words': has_sadness_words,
        'has_anger_words': has_anger_words,
        'has_worry_words': has_worry_words,
        'has_surprise_words': has_surprise_words,
        'has_informational_words': has_informational_words,
        'is_neutral': is_neutral
    }
  
    if condition_name in condition_functions:
        return condition_functions[condition_name](text_tokens)
  
    return False

def has_emotion_words(text_tokens):
    """Verifica si el texto contiene palabras emocionales."""
    emotion_words = set()
  
    # Cargar palabras emocionales desde el diccionario
    for sentiment in ['alegria', 'tristeza', 'enojo', 'preocupacion', 'sorpresa']:
        sentiment_data = load_sentiment_data(sentiment)
        for level in ['debil', 'moderado', 'fuerte']:
            emotion_words.update(sentiment_data['intensity_levels'][level]['words'])
  
    return any(token.lower() in emotion_words for token in text_tokens)

def has_positive_words(text_tokens):
    """Verifica si el texto contiene palabras positivas."""
    positive_words = set()
    sentiment_data = load_sentiment_data('alegria')
  
    for level in ['debil', 'moderado', 'fuerte']:
        positive_words.update(sentiment_data['intensity_levels'][level]['words'])
  
    return any(token.lower() in positive_words for token in text_tokens)
```

### 2. Evaluación con Intensificadores

```python
def evaluate_with_intensifiers(text_tokens):
    """
    Evalúa el texto considerando intensificadores y atenuadores.
  
    Args:
        text_tokens: Lista de tokens del texto
  
    Returns:
        dict: Puntuaciones ajustadas por intensificadores
    """
    base_scores = evaluate_base_sentiments(text_tokens)
    intensifiers = detect_intensifiers(text_tokens)
    negations = detect_negations(text_tokens)
  
    # Aplicar modificadores
    for i, token in enumerate(text_tokens):
        if token.lower() in intensifiers:
            # Buscar palabra siguiente para intensificar
            if i + 1 < len(text_tokens):
                next_word = text_tokens[i + 1]
                sentiment = find_word_sentiment(next_word)
                if sentiment:
                    base_scores[sentiment] *= 1.5
      
        if token.lower() in negations:
            # Buscar palabra siguiente para negar
            if i + 1 < len(text_tokens):
                next_word = text_tokens[i + 1]
                sentiment = find_word_sentiment(next_word)
                if sentiment:
                    base_scores[sentiment] *= -0.8
  
    return base_scores
```

## Ejemplos Prácticos

### Ejemplo 1: Texto Positivo Simple

```python
# Texto: "Estoy feliz"
text = "Estoy feliz"
tokens = ['estoy', 'feliz']

# Recorrido del árbol:
# root → positive_check → joy_intensity → moderately_happy

def trace_tree_execution(text_tokens):
    """Traza la ejecución del árbol paso a paso."""
    current_node = get_node_by_id("root")
    path = []
  
    while current_node:
        path.append(f"{current_node.id}: {current_node.description}")
      
        # Evaluar condición
        condition_result = evaluate_condition(current_node.condition, text_tokens)
        path.append(f"  Condición '{current_node.condition}': {condition_result}")
      
        # Acumular puntuaciones
        path.append(f"  Puntuaciones: {current_node.sentiment_scores}")
      
        # Determinar siguiente nodo
        if current_node.true_branch is None and current_node.false_branch is None:
            path.append("  → Nodo hoja alcanzado")
            break
      
        if condition_result:
            current_node = get_node_by_id(current_node.true_branch)
            path.append(f"  → Siguiente: {current_node.id}")
        else:
            current_node = get_node_by_id(current_node.false_branch)
            path.append(f"  → Siguiente: {current_node.id}")
  
    return path

# Ejecutar traza
trace = trace_tree_execution(tokens)
for step in trace:
    print(step)
```

### Ejemplo 2: Texto con Negación

```python
# Texto: "No estoy feliz"
text = "No estoy feliz"
tokens = ['no', 'estoy', 'feliz']

# El árbol detectará "no" como negación y ajustará las puntuaciones
def analyze_with_negation(text_tokens):
    """Analiza texto considerando negaciones."""
    # Primero evaluar sin negaciones
    base_scores = depth_first_search(get_node_by_id("root"), text_tokens)
  
    # Aplicar reglas de negación
    for i, token in enumerate(text_tokens):
        if token.lower() == 'no' and i + 1 < len(text_tokens):
            next_word = text_tokens[i + 1]
            sentiment = find_word_sentiment(next_word)
            if sentiment:
                base_scores[sentiment] *= -0.8
                # Aumentar sentimiento opuesto
                opposite_sentiment = get_opposite_sentiment(sentiment)
                base_scores[opposite_sentiment] += 0.3
  
    return base_scores

results = analyze_with_negation(tokens)
print("Resultados con negación:", results)
```

### Ejemplo 3: Texto Complejo

```python
# Texto: "Estoy muy feliz pero también un poco preocupado"
text = "Estoy muy feliz pero también un poco preocupado"
tokens = ['estoy', 'muy', 'feliz', 'pero', 'tambien', 'un', 'poco', 'preocupado']

def analyze_complex_text(text_tokens):
    """Analiza texto complejo con múltiples sentimientos."""
    # Dividir en frases por conectores
    phrases = split_by_connectors(text_tokens)
  
    all_scores = []
    for phrase in phrases:
        phrase_scores = depth_first_search(get_node_by_id("root"), phrase)
        all_scores.append(phrase_scores)
  
    # Combinar puntuaciones usando lógica difusa
    final_scores = combine_sentiment_scores(all_scores)
    return final_scores

results = analyze_complex_text(tokens)
print("Resultados complejos:", results)
```

## Optimizaciones

### 1. Memoización

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_evaluate_condition(condition_name, text_tuple):
    """
    Versión cacheada de evaluate_condition para mejorar rendimiento.
  
    Args:
        condition_name: Nombre de la condición
        text_tuple: Tupla de tokens (para poder cachear)
  
    Returns:
        bool: Resultado de la evaluación
    """
    return evaluate_condition(condition_name, list(text_tuple))
```

### 2. Búsqueda con Poda

```python
def pruned_search(node, text_tokens, accumulated_scores, max_depth=10):
    """
    Búsqueda con poda para evitar caminos poco prometedores.
  
    Args:
        node: Nodo actual
        text_tokens: Tokens del texto
        accumulated_scores: Puntuaciones acumuladas
        max_depth: Profundidad máxima permitida
  
    Returns:
        dict: Puntuaciones finales
    """
    if max_depth <= 0:
        return accumulated_scores
  
    # Acumular puntuaciones
    for sentiment, score in node.sentiment_scores.items():
        accumulated_scores[sentiment] += score
  
    # Poda: si ya tenemos un sentimiento dominante, continuar
    dominant_sentiment = max(accumulated_scores, key=accumulated_scores.get)
    if accumulated_scores[dominant_sentiment] > 0.8:
        return accumulated_scores
  
    # Continuar búsqueda normal
    if node.true_branch is None and node.false_branch is None:
        return accumulated_scores
  
    condition_result = evaluate_condition(node.condition, text_tokens)
  
    if condition_result:
        next_node = get_node_by_id(node.true_branch)
    else:
        next_node = get_node_by_id(node.false_branch)
  
    return pruned_search(next_node, text_tokens, accumulated_scores, max_depth - 1)
```

## Complejidad y Rendimiento

### Análisis de Complejidad

- **Tiempo**: O(h) donde h es la altura del árbol
- **Espacio**: O(h) para la pila de recursión
- **En el peor caso**: O(n) donde n es el número total de nodos

### Métricas de Rendimiento

```python
import time

def measure_performance(text_samples):
    """Mide el rendimiento del algoritmo de búsqueda."""
    results = []
  
    for text in text_samples:
        tokens = preprocess_text(text)
      
        start_time = time.time()
        scores = depth_first_search(get_node_by_id("root"), tokens)
        end_time = time.time()
      
        results.append({
            'text': text,
            'tokens': len(tokens),
            'time': end_time - start_time,
            'scores': scores
        })
  
    return results

# Ejemplo de uso
test_texts = [
    "Estoy feliz",
    "Me siento muy triste hoy",
    "Estoy enojado contigo",
    "Me preocupa mucho el futuro",
    "¡Increíble! No puedo creerlo"
]

performance_results = measure_performance(test_texts)
for result in performance_results:
    print(f"Texto: {result['text']}")
    print(f"Tokens: {result['tokens']}, Tiempo: {result['time']:.4f}s")
    print(f"Sentimientos: {result['scores']}\n")
```

## Conclusión

La búsqueda en árbol es un algoritmo eficiente y efectivo para el análisis de sentimientos. Sus principales ventajas son:

✅ **Eficiencia**: Complejidad O(h) donde h es la altura del árbol
✅ **Interpretabilidad**: Cada decisión es clara y explicable
✅ **Flexibilidad**: Fácil modificar y extender
✅ **Precisión**: Puede manejar casos complejos con múltiples sentimientos

El algoritmo se adapta perfectamente a nuestro sistema de análisis de sentimientos basado en árboles de decisión y lógica difusa.
