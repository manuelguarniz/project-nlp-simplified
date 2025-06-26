# Especificaciones Técnicas - Interfaces de Módulos

## 1. Tipos de Datos y Validaciones

### 1.1 SentimentResult

**Estructura completa:**
```python
@dataclass
class SentimentResult:
    text: str                                    # Texto original analizado
    sentiments: Dict[str, float]                 # Puntuaciones por sentimiento
    confidence: float                            # Confianza (0.0 - 1.0)
    processing_time: float                       # Tiempo en segundos
    matched_keywords: Dict[str, List[str]]       # Palabras clave encontradas
    tree_path: List[str]                         # Ruta en el árbol
    modifiers_applied: Dict[str, List[str]]      # Modificadores aplicados
    dominant_sentiment: Optional[str]            # Sentimiento dominante
    secondary_sentiments: List[str]              # Sentimientos secundarios
    analysis_quality: str                        # 'high', 'medium', 'low'
```

**Validaciones:**
- `text`: No vacío, longitud ≤ 50 palabras
- `sentiments`: Claves válidas: ['alegria', 'tristeza', 'enojo', 'preocupacion', 'informacion', 'sorpresa']
- `confidence`: Rango [0.0, 1.0]
- `processing_time`: Valor positivo
- `dominant_sentiment`: Debe existir en `sentiments` si no es None

### 1.2 DecisionTreeNode

**Estructura completa:**
```python
@dataclass
class DecisionTreeNode:
    id: str                                     # Identificador único
    condition: Optional[str]                    # Condición a evaluar
    branches: Dict[str, str]                    # Ramas del nodo
    sentiment_scores: Dict[str, float]          # Puntuaciones base
    keywords: List[str]                         # Palabras clave
    description: str                            # Descripción
    node_type: str                              # 'decision', 'leaf', 'root'
    depth: int                                  # Profundidad en el árbol
    parent_id: Optional[str]                    # Nodo padre
    children_ids: List[str]                     # Nodos hijos
```

**Validaciones:**
- `id`: Único en todo el árbol
- `condition`: Sintaxis válida para evaluación
- `branches`: Solo claves 'true' y 'false'
- `sentiment_scores`: Valores en rango [0.0, 1.0]
- `node_type`: Valores válidos: ['decision', 'leaf', 'root']

### 1.3 SystemConfig

**Estructura completa:**
```python
@dataclass
class SystemConfig:
    max_text_length: int = 50
    min_confidence: float = 0.3
    enable_fuzzy_logic: bool = True
    enable_memoization: bool = True
    sentiment_thresholds: Dict[str, float] = None
    fuzzy_parameters: Dict[str, float] = None
    preprocessing: Dict[str, any] = None
    tree_search: Dict[str, any] = None
    output_format: Dict[str, any] = None
    logging: Dict[str, any] = None
```

## 2. Especificaciones de Métodos

### 2.1 TextPreprocessor

#### `preprocess(text: str) -> Dict[str, any]`

**Parámetros:**
- `text`: String no vacío, longitud ≤ 50 palabras

**Retorna:**
```python
{
    'cleaned_text': str,           # Texto limpio
    'words': List[str],            # Lista de palabras
    'word_count': int,             # Número de palabras
    'has_negation': bool,          # Contiene negaciones
    'intensifiers': List[str],     # Intensificadores encontrados
    'attenuators': List[str],      # Atenuadores encontrados
    'punctuation_count': int,      # Número de signos de puntuación
    'exclamation_count': int,      # Número de exclamaciones
    'question_count': int,         # Número de interrogaciones
    'uppercase_words': List[str],  # Palabras en mayúsculas
    'emoticons': List[str],        # Emoticones encontrados
    'processing_errors': List[str] # Errores de procesamiento
}
```

**Validaciones:**
- Texto no vacío
- Longitud ≤ 50 palabras
- Caracteres válidos (UTF-8)

**Ejemplo de uso:**
```python
preprocessor = TextPreprocessor(config)
result = preprocessor.preprocess("¡Estoy muy feliz hoy!")
# Resultado:
# {
#     'cleaned_text': 'estoy muy feliz hoy',
#     'words': ['estoy', 'muy', 'feliz', 'hoy'],
#     'word_count': 4,
#     'has_negation': False,
#     'intensifiers': ['muy'],
#     'attenuators': [],
#     'punctuation_count': 1,
#     'exclamation_count': 1,
#     'question_count': 0,
#     'uppercase_words': [],
#     'emoticons': [],
#     'processing_errors': []
# }
```

#### `validate_input(text: str) -> bool`

**Validaciones:**
- Texto no None
- Texto no vacío después de limpiar espacios
- Longitud ≤ 50 palabras
- Solo caracteres UTF-8 válidos
- No contiene caracteres de control

### 2.2 TreeSearcher

#### `search(preprocessed_data: Dict[str, any]) -> Dict[str, any]`

**Parámetros:**
- `preprocessed_data`: Resultado de `TextPreprocessor.preprocess()`

**Retorna:**
```python
{
    'path': List[str],                    # Ruta recorrida
    'final_scores': Dict[str, float],     # Puntuaciones finales
    'matched_keywords': Dict[str, List[str]], # Palabras clave
    'confidence': float,                  # Confianza del resultado
    'search_depth': int,                  # Profundidad alcanzada
    'nodes_visited': int,                 # Nodos visitados
    'search_time': float,                 # Tiempo de búsqueda
    'cache_hits': int,                    # Aciertos en caché
    'backtrack_count': int                # Número de backtrackings
}
```

**Algoritmo de búsqueda:**
1. Iniciar desde nodo raíz
2. Evaluar condición del nodo actual
3. Seguir rama correspondiente (true/false)
4. Repetir hasta llegar a nodo hoja
5. Aplicar puntuaciones del nodo hoja
6. Retornar resultado con ruta completa

#### `evaluate_condition(condition: str, data: Dict[str, any]) -> bool`

**Condiciones soportadas:**
- `has_keyword(sentiment, word)`: Verifica si existe palabra clave
- `word_count > N`: Compara número de palabras
- `has_intensifier()`: Verifica presencia de intensificadores
- `has_negation()`: Verifica presencia de negaciones
- `has_emoticon()`: Verifica presencia de emoticones
- `is_question()`: Verifica si es pregunta
- `is_exclamation()`: Verifica si es exclamación

**Ejemplo:**
```python
condition = "has_keyword('alegria', 'feliz') and word_count > 3"
data = {'words': ['estoy', 'muy', 'feliz', 'hoy'], 'word_count': 4}
result = searcher.evaluate_condition(condition, data)  # True
```

### 2.3 FuzzyLogicProcessor

#### `apply_fuzzy_rules(base_scores: Dict[str, float], modifiers: Dict[str, List[str]]) -> Dict[str, float]`

**Parámetros:**
- `base_scores`: Puntuaciones base del árbol
- `modifiers`: Modificadores extraídos del texto

**Reglas aplicadas:**
1. **Intensificación**: Multiplicar por factor si hay intensificadores
2. **Atenuación**: Multiplicar por factor si hay atenuadores
3. **Negación**: Invertir puntuaciones si hay negaciones
4. **Contexto**: Ajustar basado en puntuación y signos de puntuación
5. **Emociones mixtas**: Combinar usando operadores difusos

**Ejemplo:**
```python
base_scores = {'alegria': 0.6, 'tristeza': 0.2}
modifiers = {
    'intensifiers': ['muy', 'extremadamente'],
    'negations': ['no'],
    'attenuators': []
}
result = fuzzy_processor.apply_fuzzy_rules(base_scores, modifiers)
# Resultado: {'alegria': 0.18, 'tristeza': 0.54}
```

#### `intensify_sentiment(score: float, intensifiers: List[str]) -> float`

**Fórmula:**
```
factor = 1.0 + (len(intensifiers) * intensification_factor)
new_score = min(1.0, score * factor)
```

#### `attenuate_sentiment(score: float, attenuators: List[str]) -> float`

**Fórmula:**
```
factor = attenuation_factor ** len(attenuators)
new_score = score * factor
```

#### `apply_negation(scores: Dict[str, float], negations: List[str]) -> Dict[str, float]`

**Fórmula:**
```
if len(negations) % 2 == 1:  # Número impar de negaciones
    for sentiment in scores:
        scores[sentiment] = 1.0 - scores[sentiment]
```

### 2.4 KeywordMatcher

#### `find_matches(words: List[str]) -> Dict[str, List[str]]`

**Algoritmo:**
1. Normalizar palabras (minúsculas, sin acentos)
2. Buscar coincidencias exactas
3. Buscar coincidencias parciales (stemming)
4. Buscar sinónimos
5. Agrupar por sentimiento

**Retorna:**
```python
{
    'alegria': ['feliz', 'contento'],
    'tristeza': ['triste'],
    'enojo': [],
    'preocupacion': [],
    'informacion': [],
    'sorpresa': []
}
```

#### `calculate_word_scores(matches: Dict[str, List[str]]) -> Dict[str, float]`

**Fórmula:**
```
score = (len(matches[sentiment]) / total_words) * base_weight
```

### 2.5 ScoreNormalizer

#### `normalize_scores(scores: Dict[str, float]) -> Dict[str, float]`

**Métodos de normalización:**
1. **Min-Max**: `(score - min) / (max - min)`
2. **Z-Score**: `(score - mean) / std`
3. **Softmax**: `exp(score) / sum(exp(scores))`
4. **Capped**: Limitar a rango [0, 1]

**Ejemplo:**
```python
scores = {'alegria': 0.8, 'tristeza': 0.3, 'enojo': 1.2}
normalized = normalizer.normalize_scores(scores)
# Resultado: {'alegria': 0.67, 'tristeza': 0.25, 'enojo': 1.0}
```

#### `calculate_confidence(scores: Dict[str, float], matched_keywords: Dict[str, List[str]]) -> float`

**Factores considerados:**
- Número de palabras clave encontradas
- Distribución de puntuaciones
- Consistencia entre sentimientos
- Calidad del texto de entrada

**Fórmula:**
```
keyword_confidence = sum(len(keywords)) / (total_words * expected_keywords)
distribution_confidence = 1 - (max_score - min_score)
consistency_confidence = 1 - (number_of_high_scores / total_sentiments)
confidence = (keyword_confidence + distribution_confidence + consistency_confidence) / 3
```

### 2.6 SentimentAnalyzer

#### `analyze(text: str) -> SentimentResult`

**Flujo completo:**
1. Validar entrada
2. Preprocesar texto
3. Buscar palabras clave
4. Realizar búsqueda en árbol
5. Aplicar lógica difusa
6. Normalizar puntuaciones
7. Calcular confianza
8. Determinar sentimiento dominante
9. Generar resultado

**Ejemplo de uso:**
```python
analyzer = SentimentAnalyzer('tree.json', 'keywords.json', config)
result = analyzer.analyze("¡Estoy muy feliz hoy!")

print(f"Sentimiento dominante: {result.dominant_sentiment}")
print(f"Confianza: {result.confidence:.3f}")
print(f"Puntuaciones: {result.sentiments}")
```

## 3. Manejo de Errores

### 3.1 Jerarquía de Excepciones

```python
class SentimentAnalysisError(Exception):
    """Excepción base"""
    pass

class InvalidInputError(SentimentAnalysisError):
    """Error de entrada inválida"""
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message)

class TreeSearchError(SentimentAnalysisError):
    """Error en búsqueda del árbol"""
    def __init__(self, message: str, node_id: str = None):
        self.node_id = node_id
        super().__init__(message)

class ConfigurationError(SentimentAnalysisError):
    """Error de configuración"""
    pass

class ProcessingError(SentimentAnalysisError):
    """Error durante el procesamiento"""
    pass
```

### 3.2 Códigos de Error

```python
ERROR_CODES = {
    'INVALID_INPUT': 'E001',
    'TEXT_TOO_LONG': 'E002',
    'EMPTY_TEXT': 'E003',
    'INVALID_CHARACTERS': 'E004',
    'TREE_NOT_FOUND': 'E005',
    'INVALID_TREE_STRUCTURE': 'E006',
    'NODE_NOT_FOUND': 'E007',
    'INVALID_CONDITION': 'E008',
    'KEYWORDS_NOT_FOUND': 'E009',
    'INVALID_KEYWORDS_FORMAT': 'E010',
    'CONFIGURATION_ERROR': 'E011',
    'PROCESSING_TIMEOUT': 'E012',
    'MEMORY_ERROR': 'E013'
}
```

## 4. Optimizaciones

### 4.1 Memoización

```python
class MemoizationCache:
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}
    
    def get(self, key: str) -> Optional[any]:
        if key in self.cache:
            self.access_count[key] += 1
            return self.cache[key]
        return None
    
    def set(self, key: str, value: any):
        if len(self.cache) >= self.max_size:
            self._evict_least_used()
        self.cache[key] = value
        self.access_count[key] = 1
    
    def _evict_least_used(self):
        least_used = min(self.access_count.items(), key=lambda x: x[1])
        del self.cache[least_used[0]]
        del self.access_count[least_used[0]]
```

### 4.2 Búsqueda Optimizada

- **Early termination**: Detener si se alcanza confianza alta
- **Pruning**: Eliminar ramas con baja probabilidad
- **Parallel processing**: Procesar múltiples ramas en paralelo
- **Caching**: Almacenar resultados de búsquedas previas

## 5. Métricas de Rendimiento

### 5.1 Métricas a Monitorear

```python
@dataclass
class PerformanceMetrics:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_processing_time: float = 0.0
    cache_hit_rate: float = 0.0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    error_rate: float = 0.0
```

### 5.2 Logging

```python
import logging

def setup_logging(config: SystemConfig):
    logger = logging.getLogger('sentiment_analyzer')
    logger.setLevel(getattr(logging, config.logging['level']))
    
    if config.logging['enable_file_logging']:
        file_handler = logging.FileHandler(config.logging['log_file'])
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)
    
    if config.logging['enable_console_logging']:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(levelname)s - %(message)s'
        ))
        logger.addHandler(console_handler)
    
    return logger
```

## 6. Pruebas y Validación

### 6.1 Casos de Prueba

```python
TEST_CASES = [
    {
        'input': '¡Estoy muy feliz hoy!',
        'expected_dominant': 'alegria',
        'expected_confidence': 0.7,
        'description': 'Texto positivo con intensificador'
    },
    {
        'input': 'No estoy triste',
        'expected_dominant': 'alegria',
        'expected_confidence': 0.6,
        'description': 'Negación de sentimiento negativo'
    },
    {
        'input': '¿Qué hora es?',
        'expected_dominant': 'informacion',
        'expected_confidence': 0.8,
        'description': 'Pregunta informativa'
    }
]
```

### 6.2 Validación de Resultados

```python
def validate_result(result: SentimentResult) -> bool:
    """Valida que el resultado cumpla con las especificaciones"""
    
    # Validar estructura
    if not hasattr(result, 'text') or not result.text:
        return False
    
    if not hasattr(result, 'sentiments') or not isinstance(result.sentiments, dict):
        return False
    
    # Validar puntuaciones
    for sentiment, score in result.sentiments.items():
        if not isinstance(score, (int, float)) or score < 0 or score > 1:
            return False
    
    # Validar confianza
    if not isinstance(result.confidence, (int, float)) or result.confidence < 0 or result.confidence > 1:
        return False
    
    return True
``` 