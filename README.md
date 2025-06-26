# Sistema de Análisis de Sentimientos Académico

Un sistema académico para análisis de sentimientos en textos cortos (≤50 palabras) basado en árboles de decisión, lógica proposicional y lógica difusa, sin usar librerías de IA.

## 🎯 Características

- **Análisis de 6 sentimientos**: Alegría, Tristeza, Enojo, Preocupación, Información, Sorpresa
- **Arquitectura modular**: Componentes independientes y reutilizables
- **Lógica difusa**: Manejo de intensificadores, atenuadores y negaciones
- **Árbol de decisión**: Búsqueda eficiente con memoización
- **Validación robusta**: Manejo de errores y validaciones de entrada
- **Pruebas completas**: Cobertura de pruebas unitarias e integración
- **Configuración flexible**: Parámetros ajustables por archivo JSON

## 📁 Estructura del Proyecto

```
├── src/
│   ├── core/                    # Módulos principales
│   │   ├── text_preprocessor.py # Preprocesamiento de texto
│   │   ├── tree_searcher.py     # Búsqueda en árbol de decisión
│   │   └── fuzzy_logic.py       # Lógica difusa
│   ├── models/                  # Modelos de datos
│   │   ├── sentiment_result.py  # Estructuras de resultados
│   │   ├── sentiment_analyzer.py # Analizador principal
│   │   └── exceptions.py        # Excepciones personalizadas
│   └── utils/                   # Utilidades
│       ├── keyword_matcher.py   # Coincidencia de palabras clave
│       └── normalizer.py        # Normalización de puntuaciones
├── tests/                       # Pruebas unitarias e integración
├── docs/                        # Documentación técnica
├── resources/                   # Archivos de configuración y datos
├── main.py                      # Punto de entrada principal
├── requirements.txt             # Dependencias
└── README.md                    # Este archivo
```

## 🚀 Instalación

1. **Clonar el repositorio**:

```bash
git clone <url-del-repositorio>
cd sistema-analisis-sentimientos
```

2. **Crear entorno virtual**:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

4. **Configurar recursos**:

```bash
mkdir -p resources
# Copiar archivos de configuración y datos a resources/
```

## 📖 Uso

### Uso Básico

```python
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.models.sentiment_result import SystemConfig

# Crear configuración
config = SystemConfig()

# Inicializar analizador
analyzer = SentimentAnalyzer(config)

# Analizar texto
result = analyzer.analyze("¡Estoy muy feliz hoy!")

# Ver resultados
print(f"Sentimiento dominante: {result.dominant_sentiment}")
print(f"Confianza: {result.confidence:.3f}")
print(f"Puntuaciones: {result.sentiments}")
```

### Uso desde Línea de Comandos

```bash
# Análisis de texto único
python main.py "Estoy muy feliz hoy"

# Modo interactivo
python main.py --interactive

# Análisis desde archivo
python main.py --file textos.txt

# Con configuración personalizada
python main.py --config mi_config.json --verbose

# Mostrar información del sistema
python main.py --info
```

### Análisis en Lote

```python
texts = [
    "Estoy muy feliz",
    "Me siento triste",
    "Estoy enojado",
    "Estoy preocupado"
]

results = analyzer.batch_analyze(texts)

for i, result in enumerate(results):
    print(f"Texto {i+1}: {result.dominant_sentiment}")
```

## ⚙️ Configuración

El sistema se configura mediante archivos JSON:

### Configuración del Sistema (`resources/system_config.json`)

```json
{
  "max_text_length": 50,
  "min_confidence": 0.3,
  "enable_fuzzy_logic": true,
  "enable_memoization": true,
  "preprocessing": {
    "convert_to_lowercase": true,
    "remove_punctuation": true,
    "max_word_length": 20
  },
  "fuzzy_parameters": {
    "intensification_factor": 1.5,
    "attenuation_factor": 0.7,
    "mixed_emotion_threshold": 0.6
  },
  "tree_search": {
    "max_depth": 10,
    "timeout_seconds": 5,
    "cache_size": 1000
  }
}
```

### Árbol de Decisión (`resources/decision_tree_structure.json`)

```json
{
  "root": {
    "condition": "has_keyword('alegria', 'feliz')",
    "branches": {
      "true": "node_1",
      "false": "node_2"
    },
    "sentiment_scores": {
      "alegria": 0.5,
      "tristeza": 0.1,
      "enojo": 0.0,
      "preocupacion": 0.0,
      "informacion": 0.2,
      "sorpresa": 0.2
    }
  }
}
```

### Palabras Clave (`resources/sentiment_keywords.json`)

```json
{
  "alegria": {
    "keywords": ["feliz", "contento", "alegre"],
    "synonyms": [["gozoso", "radiante", "eufórico"]],
    "verb_forms": [["alegrarse", "regocijarse"]]
  }
}
```

## 🧪 Pruebas

### Ejecutar Todas las Pruebas

```bash
pytest tests/ -v
```

### Ejecutar Pruebas con Cobertura

```bash
pytest tests/ --cov=src --cov-report=html
```

### Ejecutar Pruebas Específicas

```bash
# Solo pruebas unitarias
pytest tests/test_text_preprocessor.py -v

# Solo pruebas de integración
pytest tests/test_integration.py -v

# Pruebas con marcadores específicos
pytest -m "not slow" -v
```

### Tipos de Pruebas

- **Pruebas Unitarias**: Cada módulo individual
- **Pruebas de Integración**: Sistema completo
- **Pruebas de Rendimiento**: Tiempo de respuesta
- **Pruebas de Validación**: Casos límite y errores

## 📊 Resultados del Análisis

El sistema devuelve un objeto `SentimentResult` con:

```python
@dataclass
class SentimentResult:
    text: str                           # Texto original
    sentiments: Dict[str, float]        # Puntuaciones por sentimiento
    confidence: float                   # Confianza del análisis (0-1)
    processing_time: float              # Tiempo de procesamiento
    matched_keywords: Dict[str, List[str]] # Palabras clave encontradas
    tree_path: List[str]                # Ruta en el árbol de decisión
    modifiers_applied: Dict[str, List[str]] # Modificadores aplicados
    dominant_sentiment: Optional[str]   # Sentimiento dominante
    secondary_sentiments: List[str]     # Sentimientos secundarios
    analysis_quality: str               # Calidad del análisis
```

### Ejemplo de Salida

```
Texto: ¡Estoy muy feliz hoy!
Sentimiento dominante: alegria
Confianza: 0.850
Tiempo de procesamiento: 0.023s
Calidad del análisis: high

Puntuaciones por sentimiento:
  alegria: 0.850
  tristeza: 0.050
  enojo: 0.000
  preocupacion: 0.000
  informacion: 0.050
  sorpresa: 0.050

Palabras clave encontradas:
  alegria: ['feliz']
  tristeza: []
  enojo: []

Ruta en el árbol: root -> node_1 -> leaf_1

Modificadores aplicados:
  intensifiers: ['muy']
  negations: []
  attenuators: []
```

## 🔧 Arquitectura

### Flujo de Procesamiento

1. **Preprocesamiento**: Limpieza y extracción de modificadores
2. **Coincidencia**: Búsqueda de palabras clave por sentimiento
3. **Árbol de Decisión**: Búsqueda para puntuaciones base
4. **Lógica Difusa**: Aplicación de modificadores
5. **Normalización**: Ajuste de puntuaciones al rango [0,1]
6. **Resultado**: Generación del objeto de resultado

### Módulos Principales

- **TextPreprocessor**: Limpieza, tokenización, extracción de modificadores
- **KeywordMatcher**: Coincidencia de palabras clave y sinónimos
- **TreeSearcher**: Búsqueda eficiente en árbol de decisión
- **FuzzyLogicProcessor**: Aplicación de reglas de lógica difusa
- **ScoreNormalizer**: Normalización y cálculo de confianza
- **SentimentAnalyzer**: Orquestador principal del sistema

## 🎛️ Configuración Avanzada

### Parámetros de Lógica Difusa

```python
config.fuzzy_parameters = {
    'intensification_factor': 1.5,    # Factor de intensificación
    'attenuation_factor': 0.7,        # Factor de atenuación
    'mixed_emotion_threshold': 0.6,   # Umbral para emociones mixtas
    'context_weight': 0.3             # Peso del contexto
}
```

### Parámetros de Búsqueda en Árbol

```python
config.tree_search = {
    'max_depth': 10,                  # Profundidad máxima
    'timeout_seconds': 5,             # Timeout de búsqueda
    'cache_size': 1000,               # Tamaño del cache
    'enable_backtracking': True       # Habilitar backtracking
}
```

### Parámetros de Preprocesamiento

```python
config.preprocessing = {
    'convert_to_lowercase': True,     # Convertir a minúsculas
    'remove_punctuation': True,       # Remover puntuación
    'max_word_length': 20,            # Longitud máxima de palabra
    'remove_stopwords': False         # Remover palabras vacías
}
```

## 📈 Rendimiento

### Métricas Típicas

- **Tiempo de procesamiento**: < 50ms por texto
- **Precisión**: > 80% en textos claros
- **Cobertura**: 6 sentimientos principales
- **Escalabilidad**: Procesamiento en lote eficiente

### Optimizaciones

- **Memoización**: Cache de resultados de búsqueda
- **Búsqueda eficiente**: Algoritmos optimizados en árbol
- **Procesamiento paralelo**: Análisis en lote
- **Validación temprana**: Rechazo de entradas inválidas

## 🐛 Solución de Problemas

### Errores Comunes

1. **Archivo de configuración no encontrado**:

   ```bash
   # Verificar que existe resources/system_config.json
   ls resources/
   ```
2. **Error de importación**:

   ```bash
   # Verificar que el entorno virtual está activado
   source venv/bin/activate
   ```
3. **Pruebas fallando**:

   ```bash
   # Ejecutar con más verbosidad
   pytest tests/ -v -s
   ```

### Logs y Debugging

```python
import logging

# Configurar logging detallado
logging.basicConfig(level=logging.DEBUG)

# El analizador generará logs detallados
analyzer = SentimentAnalyzer(config)
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código

- **Formato**: Black
- **Linting**: Flake8
- **Tipos**: MyPy
- **Pruebas**: pytest con cobertura > 90%

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **Manuel Guarniz**

## 🙏 Agradecimientos

- Universidad Tecnológica del Perú
- Departamento de Matemática Discreta
- Profesores y compañeros del curso

## 📞 Contacto

Para preguntas o soporte:

- Email: cruzemg95@gmail.com
- GitHub Issues: https://github.com/manuelguarniz/project-nlp-simplified/issues

---

**Nota**: Este es un sistema académico diseñado para fines educativos. Para uso en producción, se recomienda realizar validaciones adicionales y ajustes de configuración según el dominio específico.
