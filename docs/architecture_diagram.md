# Diagrama de Arquitectura del Sistema

## 1. Arquitectura General

```mermaid
graph TB
    subgraph "Entrada"
        A[main.py] --> B[Texto de entrada]
    end
    
    subgraph "Capa de Análisis"
        C[SentimentAnalyzer] --> D[TextPreprocessor]
        C --> E[TreeSearcher]
        C --> F[KeywordMatcher]
        C --> G[FuzzyLogicProcessor]
        C --> H[ScoreNormalizer]
    end
    
    subgraph "Recursos"
        I[decision_tree_structure.json]
        J[sentiment_keywords.json]
        K[system_config.json]
    end
    
    subgraph "Salida"
        L[SentimentResult]
    end
    
    B --> C
    I --> E
    J --> F
    K --> C
    C --> L
    
    style A fill:#e1f5fe
    style C fill:#f3e5f5
    style L fill:#e8f5e8
    style I fill:#fff3e0
    style J fill:#fff3e0
    style K fill:#fff3e0
```

## 2. Flujo de Datos Detallado

```mermaid
sequenceDiagram
    participant M as main.py
    participant SA as SentimentAnalyzer
    participant TP as TextPreprocessor
    participant KM as KeywordMatcher
    participant TS as TreeSearcher
    participant FL as FuzzyLogicProcessor
    participant SN as ScoreNormalizer
    participant R as Recursos JSON
    
    M->>SA: analyze(text)
    SA->>TP: preprocess(text)
    TP-->>SA: preprocessed_data
    
    SA->>KM: find_matches(words)
    KM-->>SA: matched_keywords
    
    SA->>TS: search(preprocessed_data)
    TS-->>SA: tree_results
    
    SA->>FL: apply_fuzzy_rules(scores, modifiers)
    FL-->>SA: adjusted_scores
    
    SA->>SN: normalize_scores(scores)
    SN-->>SA: normalized_scores
    
    SA->>SN: calculate_confidence()
    SN-->>SA: confidence
    
    SA-->>M: SentimentResult
```

## 3. Estructura de Módulos

```mermaid
graph LR
    subgraph "Core"
        A[text_preprocessor.py]
        B[tree_searcher.py]
        C[fuzzy_logic.py]
    end
    
    subgraph "Models"
        D[decision_tree.py]
        E[sentiment_analyzer.py]
        F[sentiment_result.py]
    end
    
    subgraph "Utils"
        G[keyword_matcher.py]
        H[intensity_calculator.py]
        I[normalizer.py]
    end
    
    subgraph "Resources"
        J[decision_tree_structure.json]
        K[sentiment_keywords.json]
        L[system_config.json]
    end
    
    E --> A
    E --> B
    E --> C
    E --> G
    E --> I
    B --> D
    G --> K
    E --> L
    
    style E fill:#f3e5f5
    style J fill:#fff3e0
    style K fill:#fff3e0
    style L fill:#fff3e0
```

## 4. Jerarquía de Clases

```mermaid
classDiagram
    class SentimentAnalyzer {
        +config: SystemConfig
        +preprocessor: TextPreprocessor
        +tree_searcher: TreeSearcher
        +keyword_matcher: KeywordMatcher
        +fuzzy_processor: FuzzyLogicProcessor
        +normalizer: ScoreNormalizer
        +analyze(text: str): SentimentResult
        -_load_tree(file: str): Dict
        -_load_keywords(file: str): Dict
    }
    
    class TextPreprocessor {
        +config: SystemConfig
        +preprocess(text: str): Dict
        +validate_input(text: str): bool
        +extract_modifiers(words: List): Dict
    }
    
    class TreeSearcher {
        +tree: Dict
        +config: SystemConfig
        +memoization_cache: Dict
        +search(data: Dict): Dict
        +evaluate_condition(condition: str, data: Dict): bool
        -_build_tree(data: Dict): Dict
    }
    
    class FuzzyLogicProcessor {
        +config: SystemConfig
        +apply_fuzzy_rules(scores: Dict, modifiers: Dict): Dict
        +intensify_sentiment(score: float, intensifiers: List): float
        +attenuate_sentiment(score: float, attenuators: List): float
        +apply_negation(scores: Dict, negations: List): Dict
    }
    
    class KeywordMatcher {
        +keywords: Dict
        +find_matches(words: List): Dict
        +calculate_word_scores(matches: Dict): Dict
        -_load_keywords(data: Dict): Dict
    }
    
    class ScoreNormalizer {
        +config: SystemConfig
        +normalize_scores(scores: Dict): Dict
        +cap_scores(scores: Dict): Dict
        +calculate_confidence(scores: Dict, keywords: Dict): float
    }
    
    SentimentAnalyzer --> TextPreprocessor
    SentimentAnalyzer --> TreeSearcher
    SentimentAnalyzer --> KeywordMatcher
    SentimentAnalyzer --> FuzzyLogicProcessor
    SentimentAnalyzer --> ScoreNormalizer
```

## 5. Flujo de Procesamiento

```mermaid
flowchart TD
    A[Texto de entrada] --> B{Validar entrada}
    B -->|Válido| C[Preprocesar texto]
    B -->|Inválido| Z[Error: InvalidInputError]
    
    C --> D[Extraer palabras clave]
    D --> E[Buscar en árbol de decisión]
    E --> F{Aplicar lógica difusa?}
    
    F -->|Sí| G[Aplicar reglas difusas]
    F -->|No| H[Normalizar puntuaciones]
    
    G --> H
    H --> I[Calcular confianza]
    I --> J[Determinar sentimiento dominante]
    J --> K[Generar resultado]
    K --> L[SentimentResult]
    
    style A fill:#e1f5fe
    style L fill:#e8f5e8
    style Z fill:#ffebee
```

## 6. Manejo de Errores

```mermaid
graph TD
    A[Error detectado] --> B{Tipo de error}
    
    B -->|Entrada inválida| C[InvalidInputError]
    B -->|Error en árbol| D[TreeSearchError]
    B -->|Error de configuración| E[ConfigurationError]
    B -->|Error de procesamiento| F[ProcessingError]
    
    C --> G[Log error]
    D --> G
    E --> G
    F --> G
    
    G --> H[Retornar error al usuario]
    G --> I[Registrar en log]
    
    style A fill:#ffebee
    style C fill:#ffcdd2
    style D fill:#ffcdd2
    style E fill:#ffcdd2
    style F fill:#ffcdd2
```

## 7. Optimizaciones

```mermaid
graph LR
    subgraph "Memoización"
        A[Cache de resultados]
        B[LRU eviction]
        C[Cache hit/miss tracking]
    end
    
    subgraph "Búsqueda Optimizada"
        D[Early termination]
        E[Pruning de ramas]
        F[Parallel processing]
    end
    
    subgraph "Preprocesamiento"
        G[Text normalization]
        H[Keyword indexing]
        I[Modifier detection]
    end
    
    A --> B
    B --> C
    D --> E
    E --> F
    G --> H
    H --> I
    
    style A fill:#e8f5e8
    style D fill:#e8f5e8
    style G fill:#e8f5e8
```

## 8. Configuración del Sistema

```mermaid
graph TD
    A[system_config.json] --> B[SystemConfig]
    B --> C[Parámetros de preprocesamiento]
    B --> D[Parámetros de búsqueda]
    B --> E[Parámetros de lógica difusa]
    B --> F[Parámetros de salida]
    B --> G[Configuración de logging]
    
    C --> H[TextPreprocessor]
    D --> I[TreeSearcher]
    E --> J[FuzzyLogicProcessor]
    F --> K[ScoreNormalizer]
    G --> L[Logging system]
    
    style A fill:#fff3e0
    style B fill:#f3e5f5
```

## 9. Métricas y Monitoreo

```mermaid
graph LR
    subgraph "Métricas de Rendimiento"
        A[Processing time]
        B[Cache hit rate]
        C[Memory usage]
        D[Error rate]
    end
    
    subgraph "Logging"
        E[File logging]
        F[Console logging]
        G[Error tracking]
    end
    
    subgraph "Monitoreo"
        H[Performance metrics]
        I[System health]
        J[Usage statistics]
    end
    
    A --> H
    B --> H
    C --> I
    D --> J
    E --> G
    F --> G
    
    style H fill:#e8f5e8
    style I fill:#e8f5e8
    style J fill:#e8f5e8
```

## 10. Resumen de Dependencias

| Módulo | Dependencias | Responsabilidad |
|--------|-------------|-----------------|
| `main.py` | `SentimentAnalyzer` | Punto de entrada |
| `SentimentAnalyzer` | Todos los módulos core | Orquestación del análisis |
| `TextPreprocessor` | `SystemConfig` | Preprocesamiento de texto |
| `TreeSearcher` | `SystemConfig`, `decision_tree_structure.json` | Búsqueda en árbol |
| `KeywordMatcher` | `sentiment_keywords.json` | Coincidencia de palabras |
| `FuzzyLogicProcessor` | `SystemConfig` | Aplicación de lógica difusa |
| `ScoreNormalizer` | `SystemConfig` | Normalización de puntuaciones |

## 11. Próximos Pasos de Implementación

1. **Crear estructura de directorios** según la arquitectura definida
2. **Implementar módulos core** siguiendo las interfaces especificadas
3. **Crear tests unitarios** para cada módulo
4. **Implementar integración** entre módulos
5. **Configurar logging y monitoreo**
6. **Optimizar rendimiento** con memoización
7. **Documentar API** y crear guías de uso 