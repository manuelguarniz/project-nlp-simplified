# Casos de Prueba - Sistema de Análisis de Sentimientos

## 1. Casos de Prueba por Módulo

### 1.1 TextPreprocessor - Casos de Prueba

#### Casos Básicos de Preprocesamiento

| Caso                  | Entrada                      | Salida Esperada                                                                                                                                                                                                                                 | Descripción                                     |
| --------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **TC-PREP-001** | `"¡Estoy muy feliz hoy!"` | `{'cleaned_text': 'estoy muy feliz hoy', 'words': ['estoy', 'muy', 'feliz', 'hoy'], 'word_count': 4, 'has_negation': False, 'intensifiers': ['muy'], 'attenuators': [], 'punctuation_count': 1, 'exclamation_count': 1, 'question_count': 0}` | Texto positivo con intensificador y exclamación |
| **TC-PREP-002** | `"No estoy triste"`        | `{'cleaned_text': 'no estoy triste', 'words': ['no', 'estoy', 'triste'], 'word_count': 3, 'has_negation': True, 'intensifiers': [], 'attenuators': [], 'punctuation_count': 0, 'exclamation_count': 0, 'question_count': 0}`                  | Texto con negación                              |
| **TC-PREP-003** | `"¿Qué hora es?"`        | `{'cleaned_text': 'que hora es', 'words': ['que', 'hora', 'es'], 'word_count': 3, 'has_negation': False, 'intensifiers': [], 'attenuators': [], 'punctuation_count': 1, 'exclamation_count': 0, 'question_count': 1}`                         | Pregunta informativa                             |

#### Casos Edge de Preprocesamiento

| Caso                  | Entrada                    | Salida Esperada                                                                                                                                                                                                                                            | Descripción                                     |
| --------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| **TC-PREP-004** | `""`                     | `InvalidInputError`                                                                                                                                                                                                                                      | Texto vacío                                     |
| **TC-PREP-005** | `"   "`                  | `InvalidInputError`                                                                                                                                                                                                                                      | Solo espacios en blanco                          |
| **TC-PREP-006** | `"a" * 51`               | `InvalidInputError`                                                                                                                                                                                                                                      | Texto muy largo (>50 palabras)                   |
| **TC-PREP-007** | `"¡¡¡MUY FELIZ!!!"`   | `{'cleaned_text': 'muy feliz', 'words': ['muy', 'feliz'], 'word_count': 2, 'has_negation': False, 'intensifiers': ['muy'], 'attenuators': [], 'punctuation_count': 6, 'exclamation_count': 3, 'question_count': 0, 'uppercase_words': ['MUY', 'FELIZ']}` | Texto con múltiples exclamaciones y mayúsculas |
| **TC-PREP-008** | `"😊 Estoy contento 😊"` | `{'cleaned_text': 'estoy contento', 'words': ['estoy', 'contento'], 'word_count': 2, 'has_negation': False, 'intensifiers': [], 'attenuators': [], 'punctuation_count': 0, 'exclamation_count': 0, 'question_count': 0, 'emoticons': ['😊', '😊']}`      | Texto con emoticones                             |

### 1.2 KeywordMatcher - Casos de Prueba

#### Casos Básicos de Coincidencia

| Caso                | Entrada                                 | Salida Esperada                                                                                                          | Descripción              |
| ------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------- |
| **TC-KW-001** | `['estoy', 'muy', 'feliz', 'hoy']`    | `{'alegria': ['feliz'], 'tristeza': [], 'enojo': [], 'preocupacion': [], 'informacion': [], 'sorpresa': []}`           | Palabra clave de alegría |
| **TC-KW-002** | `['me', 'siento', 'triste']`          | `{'alegria': [], 'tristeza': ['triste'], 'enojo': [], 'preocupacion': [], 'informacion': [], 'sorpresa': []}`          | Palabra clave de tristeza |
| **TC-KW-003** | `['estoy', 'enojado', 'y', 'triste']` | `{'alegria': [], 'tristeza': ['triste'], 'enojo': ['enojado'], 'preocupacion': [], 'informacion': [], 'sorpresa': []}` | Múltiples sentimientos   |

#### Casos Edge de Coincidencia

| Caso                | Entrada                            | Salida Esperada                                                                                                                 | Descripción            |
| ------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| **TC-KW-004** | `[]`                             | `{'alegria': [], 'tristeza': [], 'enojo': [], 'preocupacion': [], 'informacion': [], 'sorpresa': []}`                         | Lista vacía            |
| **TC-KW-005** | `['xyz', 'abc', 'def']`          | `{'alegria': [], 'tristeza': [], 'enojo': [], 'preocupacion': [], 'informacion': [], 'sorpresa': []}`                         | Sin palabras clave      |
| **TC-KW-006** | `['FELIZ', 'TRISTE', 'ENOJADO']` | `{'alegria': ['FELIZ'], 'tristeza': ['TRISTE'], 'enojo': ['ENOJADO'], 'preocupacion': [], 'informacion': [], 'sorpresa': []}` | Palabras en mayúsculas |

### 1.3 TreeSearcher - Casos de Prueba

#### Casos Básicos de Búsqueda

| Caso                  | Entrada                                                                                             | Salida Esperada                                                                                                                                                                           | Descripción              |
| --------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| **TC-TREE-001** | `{'words': ['estoy', 'feliz'], 'word_count': 2, 'has_negation': False, 'intensifiers': []}`       | `{'path': ['root', 'node_1', 'leaf_1'], 'final_scores': {'alegria': 0.8, 'tristeza': 0.1, 'enojo': 0.0, 'preocupacion': 0.0, 'informacion': 0.0, 'sorpresa': 0.1}, 'confidence': 0.85}` | Búsqueda simple positiva |
| **TC-TREE-002** | `{'words': ['no', 'estoy', 'triste'], 'word_count': 3, 'has_negation': True, 'intensifiers': []}` | `{'path': ['root', 'node_2', 'leaf_2'], 'final_scores': {'alegria': 0.7, 'tristeza': 0.2, 'enojo': 0.0, 'preocupacion': 0.0, 'informacion': 0.0, 'sorpresa': 0.1}, 'confidence': 0.75}` | Búsqueda con negación   |

#### Casos Edge de Búsqueda

| Caso                  | Entrada                                                                            | Salida Esperada                                                                                                                                                                      | Descripción           |
| --------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| **TC-TREE-003** | `{'words': [], 'word_count': 0, 'has_negation': False, 'intensifiers': []}`      | `{'path': ['root', 'default_leaf'], 'final_scores': {'alegria': 0.5, 'tristeza': 0.5, 'enojo': 0.5, 'preocupacion': 0.5, 'informacion': 0.5, 'sorpresa': 0.5}, 'confidence': 0.3}` | Sin palabras (neutral) |
| **TC-TREE-004** | `{'words': ['xyz'], 'word_count': 1, 'has_negation': False, 'intensifiers': []}` | `TreeSearchError`                                                                                                                                                                  | Palabra no reconocida  |

### 1.4 FuzzyLogicProcessor - Casos de Prueba

#### Casos Básicos de Lógica Difusa

| Caso                   | Entrada                                                                                                                                   | Salida Esperada                         | Descripción            |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ----------------------- |
| **TC-FUZZY-001** | `{'base_scores': {'alegria': 0.6, 'tristeza': 0.2}, 'modifiers': {'intensifiers': ['muy'], 'negations': [], 'attenuators': []}}`        | `{'alegria': 0.9, 'tristeza': 0.2}`   | Intensificación simple |
| **TC-FUZZY-002** | `{'base_scores': {'alegria': 0.6, 'tristeza': 0.2}, 'modifiers': {'intensifiers': [], 'negations': ['no'], 'attenuators': []}}`         | `{'alegria': 0.4, 'tristeza': 0.8}`   | Negación simple        |
| **TC-FUZZY-003** | `{'base_scores': {'alegria': 0.6, 'tristeza': 0.2}, 'modifiers': {'intensifiers': [], 'negations': [], 'attenuators': ['un', 'poco']}}` | `{'alegria': 0.42, 'tristeza': 0.14}` | Atenuación             |

#### Casos Edge de Lógica Difusa

| Caso                   | Entrada                                                                                                                                                  | Salida Esperada                       | Descripción                            |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | --------------------------------------- |
| **TC-FUZZY-004** | `{'base_scores': {'alegria': 0.6, 'tristeza': 0.2}, 'modifiers': {'intensifiers': ['muy', 'extremadamente'], 'negations': ['no'], 'attenuators': []}}` | `{'alegria': 0.1, 'tristeza': 0.9}` | Múltiples intensificadores + negación |
| **TC-FUZZY-005** | `{'base_scores': {'alegria': 0.6, 'tristeza': 0.2}, 'modifiers': {'intensifiers': [], 'negations': ['no', 'no'], 'attenuators': []}}`                  | `{'alegria': 0.6, 'tristeza': 0.2}` | Doble negación (cancelan)              |
| **TC-FUZZY-006** | `{'base_scores': {'alegria': 1.0, 'tristeza': 0.0}, 'modifiers': {'intensifiers': ['muy'], 'negations': [], 'attenuators': []}}`                       | `{'alegria': 1.0, 'tristeza': 0.0}` | Intensificación en máximo             |

### 1.5 ScoreNormalizer - Casos de Prueba

#### Casos Básicos de Normalización

| Caso                  | Entrada                                             | Salida Esperada                                       | Descripción              |
| --------------------- | --------------------------------------------------- | ----------------------------------------------------- | ------------------------- |
| **TC-NORM-001** | `{'alegria': 0.8, 'tristeza': 0.3, 'enojo': 1.2}` | `{'alegria': 0.67, 'tristeza': 0.25, 'enojo': 1.0}` | Normalización con capped |
| **TC-NORM-002** | `{'alegria': 0.5, 'tristeza': 0.5, 'enojo': 0.5}` | `{'alegria': 0.5, 'tristeza': 0.5, 'enojo': 0.5}`   | Valores ya normalizados   |
| **TC-NORM-003** | `{'alegria': 0.0, 'tristeza': 0.0, 'enojo': 0.0}` | `{'alegria': 0.0, 'tristeza': 0.0, 'enojo': 0.0}`   | Todos en cero             |

#### Casos Edge de Normalización

| Caso                  | Entrada                                              | Salida Esperada                                     | Descripción           |
| --------------------- | ---------------------------------------------------- | --------------------------------------------------- | ---------------------- |
| **TC-NORM-004** | `{'alegria': -0.5, 'tristeza': 2.0, 'enojo': 0.8}` | `{'alegria': 0.0, 'tristeza': 1.0, 'enojo': 0.8}` | Valores fuera de rango |
| **TC-NORM-005** | `{}`                                               | `{}`                                              | Diccionario vacío     |

## 2. Casos de Prueba de Integración

### 2.1 Flujo Completo - Casos Positivos

| Caso                 | Entrada                               | Salida Esperada                                                                                                                                                                                                                      | Descripción                 |
| -------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------- |
| **TC-INT-001** | `"¡Estoy muy feliz hoy!"`          | `SentimentResult(text="¡Estoy muy feliz hoy!", sentiments={'alegria': 0.85, 'tristeza': 0.05, 'enojo': 0.0, 'preocupacion': 0.0, 'informacion': 0.05, 'sorpresa': 0.05}, confidence=0.82, dominant_sentiment='alegria')`          | Texto claramente positivo    |
| **TC-INT-002** | `"No estoy triste, estoy contento"` | `SentimentResult(text="No estoy triste, estoy contento", sentiments={'alegria': 0.75, 'tristeza': 0.15, 'enojo': 0.0, 'preocupacion': 0.0, 'informacion': 0.05, 'sorpresa': 0.05}, confidence=0.78, dominant_sentiment='alegria')` | Negación + palabra positiva |
| **TC-INT-003** | `"¿Qué hora es?"`                 | `SentimentResult(text="¿Qué hora es?", sentiments={'alegria': 0.1, 'tristeza': 0.1, 'enojo': 0.0, 'preocupacion': 0.0, 'informacion': 0.8, 'sorpresa': 0.0}, confidence=0.85, dominant_sentiment='informacion')`                 | Pregunta informativa         |

### 2.2 Flujo Completo - Casos Edge

| Caso                 | Entrada                                  | Salida Esperada                                                                                                                                                                                                                        | Descripción                   |
| -------------------- | ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **TC-INT-004** | `"😊😊😊"`                             | `SentimentResult(text="😊😊😊", sentiments={'alegria': 0.9, 'tristeza': 0.0, 'enojo': 0.0, 'preocupacion': 0.0, 'informacion': 0.0, 'sorpresa': 0.1}, confidence=0.75, dominant_sentiment='alegria')`                                | Solo emoticones                |
| **TC-INT-005** | `"Estoy un poco triste pero no mucho"` | `SentimentResult(text="Estoy un poco triste pero no mucho", sentiments={'alegria': 0.3, 'tristeza': 0.4, 'enojo': 0.0, 'preocupacion': 0.0, 'informacion': 0.15, 'sorpresa': 0.15}, confidence=0.65, dominant_sentiment='tristeza')` | Emoción mixta con atenuadores |
| **TC-INT-006** | `"¡¡¡NO ESTOY ENOJADO!!!"`          | `SentimentResult(text="¡¡¡NO ESTOY ENOJADO!!!", sentiments={'alegria': 0.6, 'tristeza': 0.1, 'enojo': 0.2, 'preocupacion': 0.0, 'informacion': 0.05, 'sorpresa': 0.05}, confidence=0.72, dominant_sentiment='alegria')`           | Negación enfática            |

## 3. Casos de Prueba de Rendimiento

### 3.1 Casos de Memoización

| Caso                  | Entrada                                       | Salida Esperada            | Descripción            |
| --------------------- | --------------------------------------------- | -------------------------- | ----------------------- |
| **TC-PERF-001** | `"Estoy feliz"` (primera vez)               | `processing_time: 0.15s` | Primera ejecución      |
| **TC-PERF-002** | `"Estoy feliz"` (segunda vez)               | `processing_time: 0.02s` | Cache hit               |
| **TC-PERF-003** | `"Estoy feliz"` (después de 1000 entradas) | `processing_time: 0.15s` | Cache miss por eviction |

### 3.2 Casos de Carga

| Caso                  | Entrada                | Salida Esperada            | Descripción        |
| --------------------- | ---------------------- | -------------------------- | ------------------- |
| **TC-PERF-004** | 100 textos diferentes  | `average_time: 0.12s`    | Carga normal        |
| **TC-PERF-005** | 1000 textos diferentes | `average_time: 0.18s`    | Carga alta          |
| **TC-PERF-006** | Texto de 50 palabras   | `processing_time: 0.25s` | Límite de longitud |

## 4. Casos de Prueba de Error

### 4.1 Errores de Entrada

| Caso                 | Entrada                                    | Error Esperado                                                     | Descripción          |
| -------------------- | ------------------------------------------ | ------------------------------------------------------------------ | --------------------- |
| **TC-ERR-001** | `None`                                   | `InvalidInputError: "El texto no puede ser None"`                | Entrada nula          |
| **TC-ERR-002** | `""`                                     | `InvalidInputError: "El texto no puede estar vacío"`            | Texto vacío          |
| **TC-ERR-003** | `"a" * 1000`                             | `InvalidInputError: "El texto excede el límite de 50 palabras"` | Texto muy largo       |
| **TC-ERR-004** | `"Texto con caracteres inválidos \x00"` | `InvalidInputError: "El texto contiene caracteres de control"`   | Caracteres inválidos |

### 4.2 Errores de Configuración

| Caso                 | Entrada                            | Error Esperado                                                            | Descripción             |
| -------------------- | ---------------------------------- | ------------------------------------------------------------------------- | ------------------------ |
| **TC-ERR-005** | Archivo de configuración corrupto | `ConfigurationError: "No se puede cargar la configuración"`            | Configuración inválida |
| **TC-ERR-006** | Archivo de árbol no encontrado    | `TreeSearchError: "No se encontró el archivo del árbol de decisión"` | Recurso faltante         |
| **TC-ERR-007** | Archivo de palabras clave corrupto | `ConfigurationError: "Formato inválido en archivo de palabras clave"`  | Recurso corrupto         |

### 4.3 Errores de Procesamiento

| Caso                 | Entrada                        | Error Esperado                                             | Descripción                     |
| -------------------- | ------------------------------ | ---------------------------------------------------------- | -------------------------------- |
| **TC-ERR-008** | Condición inválida en árbol | `TreeSearchError: "Condición inválida en nodo node_5"` | Lógica del árbol corrupta      |
| **TC-ERR-009** | Nodo faltante en árbol        | `TreeSearchError: "Nodo node_10 no encontrado"`          | Estructura del árbol incompleta |
| **TC-ERR-010** | Timeout en búsqueda           | `ProcessingError: "Timeout en búsqueda del árbol"`     | Búsqueda muy lenta              |

## 5. Casos de Prueba de Validación

### 5.1 Validación de Resultados

| Caso                 | Entrada                                  | Validación | Descripción                |
| -------------------- | ---------------------------------------- | ----------- | --------------------------- |
| **TC-VAL-001** | `SentimentResult` válido              | `True`    | Resultado correcto          |
| **TC-VAL-002** | `SentimentResult` con puntuaciones > 1 | `False`   | Puntuaciones fuera de rango |
| **TC-VAL-003** | `SentimentResult` con confianza > 1    | `False`   | Confianza fuera de rango    |
| **TC-VAL-004** | `SentimentResult` sin texto            | `False`   | Campo requerido faltante    |

### 5.2 Validación de Configuración

| Caso                 | Entrada                                  | Validación | Descripción            |
| -------------------- | ---------------------------------------- | ----------- | ----------------------- |
| **TC-VAL-005** | Configuración válida                   | `True`    | Configuración correcta |
| **TC-VAL-006** | Umbrales fuera de rango                  | `False`   | Umbrales inválidos     |
| **TC-VAL-007** | Parámetros de lógica difusa inválidos | `False`   | Parámetros incorrectos |

## 6. Ejemplos Simplificados de Casos de Prueba

### 6.1 Ejemplo: Texto Positivo Simple

```python
# Caso de prueba: TC-SIMPLE-001
input_text = "Estoy feliz"
expected_result = {
    'dominant_sentiment': 'alegria',
    'confidence': 0.75,
    'sentiments': {
        'alegria': 0.75,
        'tristeza': 0.1,
        'enojo': 0.0,
        'preocupacion': 0.0,
        'informacion': 0.1,
        'sorpresa': 0.05
    }
}

# Explicación:
# 1. "feliz" es palabra clave de alegría
# 2. No hay negaciones ni intensificadores
# 3. El árbol asigna alta puntuación a alegría
# 4. La lógica difusa no modifica significativamente
# 5. Resultado: alegría dominante con alta confianza
```

### 6.2 Ejemplo: Negación Simple

```python
# Caso de prueba: TC-SIMPLE-002
input_text = "No estoy triste"
expected_result = {
    'dominant_sentiment': 'alegria',
    'confidence': 0.65,
    'sentiments': {
        'alegria': 0.65,
        'tristeza': 0.25,
        'enojo': 0.0,
        'preocupacion': 0.0,
        'informacion': 0.05,
        'sorpresa': 0.05
    }
}

# Explicación:
# 1. "triste" es palabra clave de tristeza
# 2. "no" es negación
# 3. El árbol asigna puntuación base
# 4. La lógica difusa invierte las puntuaciones
# 5. Resultado: alegría (negación de tristeza) dominante
```

### 6.3 Ejemplo: Intensificación

```python
# Caso de prueba: TC-SIMPLE-003
input_text = "Estoy muy feliz"
expected_result = {
    'dominant_sentiment': 'alegria',
    'confidence': 0.85,
    'sentiments': {
        'alegria': 0.9,
        'tristeza': 0.05,
        'enojo': 0.0,
        'preocupacion': 0.0,
        'informacion': 0.02,
        'sorpresa': 0.03
    }
}

# Explicación:
# 1. "feliz" es palabra clave de alegría
# 2. "muy" es intensificador
# 3. El árbol asigna puntuación base
# 4. La lógica difusa multiplica por factor de intensificación
# 5. Resultado: alegría muy alta con alta confianza
```

### 6.4 Ejemplo: Emoción Mixta

```python
# Caso de prueba: TC-SIMPLE-004
input_text = "Estoy feliz pero preocupado"
expected_result = {
    'dominant_sentiment': 'alegria',
    'confidence': 0.6,
    'sentiments': {
        'alegria': 0.55,
        'tristeza': 0.1,
        'enojo': 0.0,
        'preocupacion': 0.45,
        'informacion': 0.0,
        'sorpresa': 0.0
    }
}

# Explicación:
# 1. "feliz" → alegría, "preocupado" → preocupación
# 2. "pero" indica contraste
# 3. El árbol asigna puntuaciones base
# 4. La lógica difusa combina emociones mixtas
# 5. Resultado: alegría ligeramente dominante, confianza media
```

## 7. Matriz de Cobertura de Pruebas

| Módulo             | Casos Básicos | Casos Edge   | Casos de Error | Total        |
| ------------------- | -------------- | ------------ | -------------- | ------------ |
| TextPreprocessor    | 3              | 5            | 4              | 12           |
| KeywordMatcher      | 3              | 3            | 0              | 6            |
| TreeSearcher        | 2              | 2            | 3              | 7            |
| FuzzyLogicProcessor | 3              | 3            | 0              | 6            |
| ScoreNormalizer     | 3              | 2            | 0              | 5            |
| Integración        | 3              | 3            | 0              | 6            |
| Rendimiento         | 0              | 0            | 3              | 3            |
| Validación         | 0              | 0            | 7              | 7            |
| **Total**     | **17**   | **18** | **17**   | **52** |

## 8. Criterios de Aceptación

### 8.1 Criterios Funcionales

- ✅ **CF-001**: El sistema debe procesar textos de hasta 50 palabras
- ✅ **CF-002**: El sistema debe detectar 6 sentimientos básicos
- ✅ **CF-003**: El sistema debe aplicar lógica difusa correctamente
- ✅ **CF-004**: El sistema debe manejar negaciones
- ✅ **CF-005**: El sistema debe calcular confianza del análisis

### 8.2 Criterios de Rendimiento

- ✅ **CR-001**: Tiempo de procesamiento < 0.5 segundos por texto
- ✅ **CR-002**: Memoria utilizada < 100MB para 1000 textos
- ✅ **CR-003**: Cache hit rate > 80% después de 100 textos
- ✅ **CR-004**: Error rate < 1% en condiciones normales

### 8.3 Criterios de Calidad

- ✅ **CQ-001**: Cobertura de código > 90%
- ✅ **CQ-002**: Todos los casos de prueba deben pasar
- ✅ **CQ-003**: Documentación completa y actualizada
- ✅ **CQ-004**: Manejo de errores robusto

## 9. Instrucciones para Ejecutar las Pruebas

### 9.1 Configuración del Entorno

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install pytest pytest-cov

# Ejecutar todas las pruebas
pytest tests/ -v --cov=src --cov-report=html
```

### 9.2 Estructura de Archivos de Prueba

```
tests/
├── test_text_preprocessor.py
├── test_keyword_matcher.py
├── test_tree_searcher.py
├── test_fuzzy_logic.py
├── test_score_normalizer.py
├── test_sentiment_analyzer.py
├── test_integration.py
└── conftest.py
```

### 9.3 Ejemplo de Archivo de Prueba

```python
# tests/test_text_preprocessor.py
import pytest
from src.core.text_preprocessor import TextPreprocessor
from src.models.sentiment_result import SystemConfig

class TestTextPreprocessor:
    def setup_method(self):
        self.config = SystemConfig()
        self.preprocessor = TextPreprocessor(self.config)
  
    def test_basic_preprocessing(self):
        """TC-PREP-001: Texto positivo con intensificador"""
        result = self.preprocessor.preprocess("¡Estoy muy feliz hoy!")
      
        assert result['cleaned_text'] == 'estoy muy feliz hoy'
        assert result['words'] == ['estoy', 'muy', 'feliz', 'hoy']
        assert result['word_count'] == 4
        assert result['has_negation'] == False
        assert result['intensifiers'] == ['muy']
        assert result['exclamation_count'] == 1
  
    def test_empty_text(self):
        """TC-PREP-004: Texto vacío"""
        with pytest.raises(InvalidInputError, match="El texto no puede estar vacío"):
            self.preprocessor.preprocess("")
```

## 10. Próximos Pasos

1. **Implementar los módulos** según las interfaces definidas
2. **Crear los archivos de prueba** siguiendo la estructura propuesta
3. **Ejecutar las pruebas** para validar la funcionalidad
4. **Refinar los casos de prueba** basándose en los resultados
5. **Documentar los resultados** de las pruebas
6. **Optimizar el rendimiento** según las métricas obtenidas
