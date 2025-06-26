# Plan del Proyecto: Sistema de Detección de Sentimientos con Árboles

## Resumen del Proyecto

Crear un modelo simplificado de NLP que utilice algoritmos de búsqueda en árboles y lógica difusa para detectar sentimientos en textos cortos (≤50 palabras) sin utilizar librerías externas de IA.

## Objetivos

- **Entrada**: Texto corto (máximo 50 palabras)
- **Procesamiento**: Árbol de decisión + Lógica difusa + Lógica proposicional
- **Salida**: Porcentajes de sentimientos detectados (ej: 50% alegría, 20% preocupación, 30% informar)

## Arquitectura del Sistema

```
Sistema de Detección de Sentimientos
├── Preprocesamiento de texto
│   ├── Tokenización
│   ├── Normalización
│   └── Detección de negaciones
├── Árbol de decisión para clasificación inicial
│   ├── Nodos de decisión
│   └── Puntuación de confianza
├── Sistema de lógica difusa para puntuación
│   ├── Puntuación de intensidad (0-1)
│   └── Combinación de indicadores
└── Generación de resultados
    ├── Cálculo de porcentajes
    └── Formato de salida
```

## Sentimientos a Detectar

| Sentimiento             | Descripción                | Palabras Clave Ejemplo                      |
| ----------------------- | --------------------------- | ------------------------------------------- |
| **Alegría**      | Positivo, feliz, contento   | feliz, alegre, contento, divertido, genial  |
| **Tristeza**      | Negativo, triste, deprimido | triste, deprimido, melancólico, desanimado |
| **Enojo**         | Negativo, molesto, furioso  | enojado, molesto, furioso, irritado         |
| **Preocupación** | Neutral-negativo, ansioso   | preocupado, ansioso, inquieto, nervioso     |
| **Información**  | Neutral, informativo        | informar, explicar, describir, mencionar    |
| **Sorpresa**      | Neutral, sorprendido        | sorprendido, asombrado, increíble, wow     |

## Estructura de Archivos

```
sentiment_analyzer/
├── main.py              # Interfaz de consola principal
├── text_processor.py    # Preprocesamiento de texto
├── decision_tree.py     # Árbol de decisión y búsqueda
├── fuzzy_logic.py       # Lógica difusa y puntuación
├── sentiment_data.py    # Datos de palabras clave y reglas
├── utils.py            # Utilidades auxiliares
├── tests.py            # Casos de prueba
└── README.md           # Documentación del proyecto
```

## Cronograma Detallado

### **Semana 1: Análisis y Desarrollo Base**

#### **Día 1: Análisis y Diseño (2 horas)**

**Hora 1: Análisis de Requisitos (60 min)**

- [X] Definir estructura de datos para árbol de decisión: [decision_tree_structure.json](../resources/decision_tree_structure.json)
- [X] Diseñar diccionarios de palabras clave por sentimiento: [sentiment_keywords.json](../resources/sentiment_keywords.json)
- [X] Planificar algoritmo de búsqueda en árbol: [tree_search_algorithm.md](../docs/tree_search_algorithm.md)
- [X] Definir reglas de lógica difusa: [fuzzy_logic_rules.md](../docs/fuzzy_logic_rules.md)

**Hora 2: Diseño de Arquitectura (60 min)**

- [X] Crear diagrama de flujo del sistema: [flow_diagrams.md](../docs/flow_diagrams.md)
- [X] Definir interfaces entre módulos: [module_interfaces.md](../docs/module_interfaces.md) > [system_config.json](../resources/system_config.json)
- [X] Diseñar estructura de clases: [technical_specifications.md](../docs/technical_specifications.md) > [architecture_diagram.md](../docs/architecture_diagram.md)
- [X] Planificar casos de prueba: [test_cases.md](../docs/test_cases.md)

#### **Día 2: Implementación Base (2 horas)**

**Hora 1: Estructuras de Datos (60 min)**

- [ ] Crear archivo `sentiment_data.py` con diccionarios
- [ ] Implementar clase `DecisionTree` en `decision_tree.py`
- [ ] Definir estructura de nodos del árbol
- [ ] Crear utilidades básicas en `utils.py`

**Hora 2: Preprocesamiento (60 min)**

- [ ] Implementar `TextProcessor` en `text_processor.py`
- [ ] Funciones de tokenización y normalización
- [ ] Detección de negaciones
- [ ] Limpieza de texto (puntuación, espacios)

#### **Día 3: Lógica Difusa y Árbol (2 horas)**

**Hora 1: Sistema de Lógica Difusa (60 min)**

- [ ] Implementar `FuzzyLogic` en `fuzzy_logic.py`
- [ ] Algoritmo de puntuación de intensidad (0-1)
- [ ] Combinación de múltiples indicadores
- [ ] Reglas de lógica proposicional

**Hora 2: Integración del Árbol (60 min)**

- [ ] Completar algoritmo de búsqueda en árbol
- [ ] Integrar puntuación de confianza
- [ ] Conectar preprocesamiento con árbol
- [ ] Pruebas básicas de funcionamiento

### **Semana 2: Integración y Refinamiento**

#### **Día 1: Integración de Componentes (2 horas)**

**Hora 1: Sistema Principal (60 min)**

- [ ] Crear `main.py` con interfaz de consola
- [ ] Integrar todos los módulos
- [ ] Implementar flujo principal del sistema
- [ ] Manejo de entrada/salida de usuario

**Hora 2: Cálculo de Resultados (60 min)**

- [ ] Algoritmo de cálculo de porcentajes
- [ ] Formato de salida (ej: "50% alegría, 20% preocupación")
- [ ] Manejo de casos edge (textos neutros, sin sentimientos)
- [ ] Validación de entrada

#### **Día 2: Pruebas y Optimización (2 horas)**

**Hora 1: Casos de Prueba (60 min)**

- [ ] Crear `tests.py` con casos de prueba
- [ ] Probar textos con sentimientos claros
- [ ] Probar textos ambiguos o mixtos
- [ ] Probar textos con negaciones

**Hora 2: Refinamiento (60 min)**

- [ ] Ajustar parámetros de lógica difusa
- [ ] Optimizar algoritmo de búsqueda
- [ ] Mejorar precisión de clasificación
- [ ] Documentar casos especiales

#### **Día 3: Finalización y Documentación (2 horas)**

**Hora 1: Pruebas Finales (60 min)**

- [ ] Pruebas exhaustivas del sistema completo
- [ ] Validación con diferentes tipos de texto
- [ ] Medición de tiempo de respuesta
- [ ] Corrección de bugs encontrados

**Hora 2: Documentación (60 min)**

- [ ] Crear `README.md` con instrucciones
- [ ] Documentar uso del sistema
- [ ] Explicar algoritmos implementados
- [ ] Preparar ejemplos de uso

## Algoritmos a Implementar

### 1. Búsqueda en Árbol de Decisión

```python
def search_tree(text_tokens, tree_node):
    # Recorrido recursivo del árbol
    # Evaluación de condiciones en cada nodo
    # Acumulación de puntuaciones
```

### 2. Lógica Difusa

```python
def calculate_fuzzy_score(word, sentiment_category):
    # Puntuación basada en intensidad de palabra
    # Factores: frecuencia, contexto, negaciones
    # Retorna valor entre 0 y 1
```

### 3. Lógica Proposicional

```python
def combine_sentiments(sentiment_scores):
    # Reglas para combinar múltiples sentimientos
    # Normalización de puntuaciones
    # Cálculo de porcentajes finales
```

## Casos de Prueba Planificados

### Casos Básicos

1. **"Estoy muy feliz hoy"** → 80% alegría, 20% información
2. **"Me siento triste y deprimido"** → 90% tristeza, 10% información
3. **"Estoy enojado contigo"** → 85% enojo, 15% información

### Casos Complejos

1. **"No estoy feliz pero tampoco triste"** → 40% tristeza, 30% información, 30% neutral
2. **"Me preocupa que no llegues a tiempo"** → 70% preocupación, 30% información
3. **"¡Increíble! No puedo creer lo que pasó"** → 60% sorpresa, 40% información

### Casos Edge

1. **"El clima está soleado"** → 100% información
2. **""** (texto vacío) → Error o 100% neutral
3. **"A B C D E"** (sin sentido) → 100% neutral

## Métricas de Éxito

- **Precisión**: >70% en clasificación correcta de sentimientos principales
- **Tiempo de respuesta**: <1 segundo para textos de 50 palabras
- **Cobertura**: Manejo de al menos 6 categorías de sentimientos
- **Robustez**: Funcionamiento correcto con textos ambiguos y negaciones

## Consideraciones Técnicas

### Restricciones

- ✅ Solo Python estándar (sin librerías externas)
- ✅ Estructuras de datos puras (listas, diccionarios, clases)
- ✅ Algoritmos simples pero efectivos
- ✅ Interfaz de consola simple

### Tecnologías Utilizadas

- **Estructuras de Datos**: Árboles, diccionarios, listas
- **Algoritmos**: Búsqueda en árbol, lógica difusa, lógica proposicional
- **Paradigmas**: Programación orientada a objetos, programación funcional

### Entregables

1. Código fuente completo y funcional
2. Documentación técnica
3. Casos de prueba
4. Ejemplos de uso
5. Análisis de resultados

---

**Nota**: Este plan está diseñado para ser flexible y puede ajustarse según el progreso y necesidades que surjan durante el desarrollo.
