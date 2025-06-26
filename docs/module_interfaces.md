# Interfaces entre Módulos - Sistema de Análisis de Sentimientos

## 1. Visión General de la Arquitectura

El sistema se organiza en los siguientes módulos principales:

```
src/
├── core/
│   ├── __init__.py
│   ├── text_preprocessor.py      # Preprocesamiento de texto
│   ├── tree_searcher.py          # Búsqueda en árbol de decisión
│   └── fuzzy_logic.py           # Lógica difusa
├── models/
│   ├── __init__.py
│   ├── decision_tree.py         # Modelo del árbol de decisión
│   ├── sentiment_analyzer.py    # Analizador principal
│   └── sentiment_result.py      # Estructura de resultados
├── utils/
│   ├── __init__.py
│   ├── keyword_matcher.py       # Coincidencia de palabras clave
│   ├── intensity_calculator.py  # Cálculo de intensidades
│   └── normalizer.py           # Normalización de puntuaciones
└── main.py                     # Punto de entrada principal
```

## 2. Interfaces de Datos

### 2.1 Estructura de Sentimiento (SentimentResult)

```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class SentimentResult:
    """Resultado del análisis de sentimientos"""
    text: str
    sentiments: Dict[str, float]  # {'alegria': 0.75, 'tristeza': 0.2, ...}
    confidence: float             # Confianza general del análisis (0-1)
    processing_time: float        # Tiempo de procesamiento en segundos
    matched_keywords: Dict[str, List[str]]  # Palabras clave encontradas por sentimiento
    tree_path: List[str]          # Ruta recorrida en el árbol de decisión
    modifiers_applied: Dict[str, List[str]]  # Modificadores aplicados
```

### 2.2 Nodo del Árbol de Decisión

```python
@dataclass
class DecisionTreeNode:
    """Nodo del árbol de decisión"""
    id: str
    condition: Optional[str]      # Condición a evaluar (None para nodos hoja)
    branches: Dict[str, str]      # {'true': 'node_id', 'false': 'node_id'}
    sentiment_scores: Dict[str, float]  # Puntuaciones de sentimientos
    keywords: List[str]           # Palabras clave asociadas al nodo
    description: str              # Descripción del nodo
```

### 2.3 Configuración del Sistema

```python
@dataclass
class SystemConfig:
    """Configuración del sistema"""
    max_text_length: int = 50     # Longitud máxima del texto
    min_confidence: float = 0.3   # Confianza mínima para considerar resultado válido
    enable_fuzzy_logic: bool = True
    enable_memoization: bool = True
    sentiment_thresholds: Dict[str, float] = None  # Umbrales por sentimiento
```

## 3. Interfaces de Módulos

### 3.1 Módulo de Preprocesamiento (text_preprocessor.py)

```python
class TextPreprocessor:
    """Preprocesador de texto"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
    
    def preprocess(self, text: str) -> Dict[str, any]:
        """
        Preprocesa el texto de entrada
        
        Args:
            text: Texto a preprocesar
            
        Returns:
            Dict con:
            - 'cleaned_text': str
            - 'words': List[str]
            - 'word_count': int
            - 'has_negation': bool
            - 'intensifiers': List[str]
            - 'attenuators': List[str]
            - 'punctuation_count': int
        """
        pass
    
    def validate_input(self, text: str) -> bool:
        """Valida que el texto cumpla con los requisitos"""
        pass
    
    def extract_modifiers(self, words: List[str]) -> Dict[str, List[str]]:
        """Extrae modificadores (negaciones, intensificadores, atenuadores)"""
        pass
```

### 3.2 Módulo de Búsqueda en Árbol (tree_searcher.py)

```python
class TreeSearcher:
    """Buscador en árbol de decisión"""
    
    def __init__(self, tree_data: Dict, config: SystemConfig):
        self.tree = self._build_tree(tree_data)
        self.config = config
        self.memoization_cache = {} if config.enable_memoization else None
    
    def search(self, preprocessed_data: Dict[str, any]) -> Dict[str, any]:
        """
        Realiza búsqueda en el árbol de decisión
        
        Args:
            preprocessed_data: Datos preprocesados del texto
            
        Returns:
            Dict con:
            - 'path': List[str] - Ruta recorrida
            - 'final_scores': Dict[str, float] - Puntuaciones finales
            - 'matched_keywords': Dict[str, List[str]]
            - 'confidence': float
        """
        pass
    
    def evaluate_condition(self, condition: str, data: Dict[str, any]) -> bool:
        """Evalúa una condición del árbol"""
        pass
    
    def _build_tree(self, tree_data: Dict) -> Dict[str, DecisionTreeNode]:
        """Construye el árbol de decisión desde los datos JSON"""
        pass
```

### 3.3 Módulo de Lógica Difusa (fuzzy_logic.py)

```python
class FuzzyLogicProcessor:
    """Procesador de lógica difusa"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
    
    def apply_fuzzy_rules(self, base_scores: Dict[str, float], 
                         modifiers: Dict[str, List[str]]) -> Dict[str, float]:
        """
        Aplica reglas de lógica difusa a las puntuaciones base
        
        Args:
            base_scores: Puntuaciones base de sentimientos
            modifiers: Modificadores extraídos del texto
            
        Returns:
            Puntuaciones ajustadas por lógica difusa
        """
        pass
    
    def intensify_sentiment(self, score: float, intensifiers: List[str]) -> float:
        """Intensifica un sentimiento basado en intensificadores"""
        pass
    
    def attenuate_sentiment(self, score: float, attenuators: List[str]) -> float:
        """Atenúa un sentimiento basado en atenuadores"""
        pass
    
    def apply_negation(self, scores: Dict[str, float], negations: List[str]) -> Dict[str, float]:
        """Aplica negaciones a las puntuaciones"""
        pass
    
    def combine_emotions(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Combina emociones mixtas usando operadores difusos"""
        pass
```

### 3.4 Módulo de Coincidencia de Palabras Clave (keyword_matcher.py)

```python
class KeywordMatcher:
    """Coincidencia de palabras clave"""
    
    def __init__(self, keywords_data: Dict):
        self.keywords = self._load_keywords(keywords_data)
    
    def find_matches(self, words: List[str]) -> Dict[str, List[str]]:
        """
        Encuentra coincidencias de palabras clave por sentimiento
        
        Args:
            words: Lista de palabras del texto
            
        Returns:
            Dict con sentimientos como claves y listas de palabras encontradas
        """
        pass
    
    def calculate_word_scores(self, matches: Dict[str, List[str]]) -> Dict[str, float]:
        """Calcula puntuaciones basadas en palabras encontradas"""
        pass
    
    def _load_keywords(self, keywords_data: Dict) -> Dict[str, Dict[str, List[str]]]:
        """Carga las palabras clave desde el archivo JSON"""
        pass
```

### 3.5 Módulo de Normalización (normalizer.py)

```python
class ScoreNormalizer:
    """Normalizador de puntuaciones"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
    
    def normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Normaliza las puntuaciones al rango [0, 1]
        
        Args:
            scores: Puntuaciones a normalizar
            
        Returns:
            Puntuaciones normalizadas
        """
        pass
    
    def cap_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Limita las puntuaciones al rango [0, 1]"""
        pass
    
    def calculate_confidence(self, scores: Dict[str, float], 
                           matched_keywords: Dict[str, List[str]]) -> float:
        """Calcula la confianza del análisis"""
        pass
```

### 3.6 Analizador Principal (sentiment_analyzer.py)

```python
class SentimentAnalyzer:
    """Analizador principal de sentimientos"""
    
    def __init__(self, tree_file: str, keywords_file: str, config: SystemConfig):
        self.config = config
        self.preprocessor = TextPreprocessor(config)
        self.tree_searcher = TreeSearcher(self._load_tree(tree_file), config)
        self.keyword_matcher = KeywordMatcher(self._load_keywords(keywords_file))
        self.fuzzy_processor = FuzzyLogicProcessor(config)
        self.normalizer = ScoreNormalizer(config)
    
    def analyze(self, text: str) -> SentimentResult:
        """
        Analiza el sentimiento de un texto
        
        Args:
            text: Texto a analizar
            
        Returns:
            SentimentResult con los resultados del análisis
        """
        pass
    
    def _load_tree(self, tree_file: str) -> Dict:
        """Carga el árbol de decisión desde archivo"""
        pass
    
    def _load_keywords(self, keywords_file: str) -> Dict:
        """Carga las palabras clave desde archivo"""
        pass
```

## 4. Flujo de Datos entre Módulos

```
1. main.py
   ↓ (texto de entrada)
2. SentimentAnalyzer.analyze()
   ↓
3. TextPreprocessor.preprocess()
   ↓ (datos preprocesados)
4. KeywordMatcher.find_matches()
   ↓ (coincidencias de palabras)
5. TreeSearcher.search()
   ↓ (puntuaciones base)
6. FuzzyLogicProcessor.apply_fuzzy_rules()
   ↓ (puntuaciones ajustadas)
7. ScoreNormalizer.normalize_scores()
   ↓ (puntuaciones finales)
8. SentimentResult (resultado final)
```

## 5. Manejo de Errores

### 5.1 Excepciones Personalizadas

```python
class SentimentAnalysisError(Exception):
    """Excepción base para errores de análisis de sentimientos"""
    pass

class InvalidInputError(SentimentAnalysisError):
    """Error de entrada inválida"""
    pass

class TreeSearchError(SentimentAnalysisError):
    """Error en búsqueda del árbol"""
    pass

class ConfigurationError(SentimentAnalysisError):
    """Error de configuración"""
    pass
```

### 5.2 Validaciones por Módulo

- **TextPreprocessor**: Validación de longitud, caracteres válidos
- **TreeSearcher**: Validación de estructura del árbol, nodos existentes
- **KeywordMatcher**: Validación de formato de palabras clave
- **FuzzyLogicProcessor**: Validación de rangos de puntuaciones
- **ScoreNormalizer**: Validación de valores numéricos

## 6. Configuración y Archivos de Recursos

### 6.1 Estructura de Archivos

```
resources/
├── decision_tree_structure.json    # Estructura del árbol de decisión
├── sentiment_keywords.json         # Palabras clave por sentimiento
└── system_config.json             # Configuración del sistema

docs/
├── module_interfaces.md           # Este documento
├── api_reference.md              # Referencia de API
└── implementation_guide.md       # Guía de implementación
```

### 6.2 Configuración del Sistema

```json
{
    "max_text_length": 50,
    "min_confidence": 0.3,
    "enable_fuzzy_logic": true,
    "enable_memoization": true,
    "sentiment_thresholds": {
        "alegria": 0.4,
        "tristeza": 0.4,
        "enojo": 0.4,
        "preocupacion": 0.4,
        "informacion": 0.3,
        "sorpresa": 0.4
    },
    "fuzzy_parameters": {
        "intensification_factor": 1.5,
        "attenuation_factor": 0.7,
        "negation_factor": 0.3
    }
}
```

## 7. Próximos Pasos

1. **Implementación de módulos**: Desarrollar cada módulo según las interfaces definidas
2. **Pruebas unitarias**: Crear tests para cada módulo
3. **Integración**: Conectar todos los módulos en el analizador principal
4. **Optimización**: Implementar memoización y optimizaciones de rendimiento
5. **Documentación**: Completar documentación de API y guías de uso 