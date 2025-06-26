# Sistema de Puntuación Científica para Sentimientos

## Problema Identificado
Los valores de score en `decision_tree_structure.json` son estimaciones subjetivas sin base científica.

## Solución: Sistema Basado en Datos

### 1. Análisis de Frecuencia de Palabras

#### Metodología
```python
# Para cada palabra emocional, calcular:
word_score = (frequency_in_category / total_words_in_category) * intensity_multiplier
```

#### Ejemplo de Cálculo
```
Palabra: "feliz"
- Frecuencia en textos alegres: 150/1000 = 0.15
- Intensidad base: 0.8
- Score final: 0.15 * 0.8 = 0.12

Palabra: "muy feliz" 
- Frecuencia: 50/1000 = 0.05
- Intensidad: 1.0 (intensificador "muy")
- Score final: 0.05 * 1.0 = 0.05
```

### 2. Factores de Puntuación Objetivos

#### A. Frecuencia de Palabra
- **Alta frecuencia** (0.1-0.3): Palabras comunes como "feliz", "triste"
- **Media frecuencia** (0.05-0.1): Palabras específicas como "eufórico", "melancólico"
- **Baja frecuencia** (0.01-0.05): Palabras raras como "extasiado", "abatido"

#### B. Intensidad de Palabra
- **Débil** (0.3-0.5): "contento", "triste"
- **Moderada** (0.6-0.8): "feliz", "deprimido"
- **Fuerte** (0.9-1.0): "eufórico", "devastado"

#### C. Contexto y Modificadores
- **Intensificadores**: "muy", "extremadamente" → ×1.5
- **Atenuadores**: "un poco", "algo" → ×0.7
- **Negaciones**: "no feliz" → ×(-0.8)

### 3. Datos de Entrenamiento Necesarios

#### Corpus de Textos Etiquetados
```json
{
  "training_data": [
    {
      "text": "Estoy muy feliz hoy",
      "sentiments": {
        "alegria": 0.85,
        "tristeza": 0.0,
        "enojo": 0.0,
        "preocupacion": 0.0,
        "informacion": 0.1,
        "sorpresa": 0.0
      }
    },
    {
      "text": "Me siento un poco triste",
      "sentiments": {
        "alegria": 0.0,
        "tristeza": 0.4,
        "enojo": 0.0,
        "preocupacion": 0.0,
        "informacion": 0.3,
        "sorpresa": 0.0
      }
    }
  ]
}
```

### 4. Algoritmo de Cálculo Propuesto

#### Paso 1: Análisis de Palabras
```python
def calculate_word_score(word, category):
    base_frequency = get_word_frequency(word, category)
    intensity = get_word_intensity(word)
    context_modifier = get_context_modifier(word)
    
    return base_frequency * intensity * context_modifier
```

#### Paso 2: Combinación de Sentimientos
```python
def combine_sentiments(word_scores):
    # Usar lógica difusa para combinar múltiples indicadores
    # Aplicar reglas de lógica proposicional
    # Normalizar a porcentajes
```

#### Paso 3: Validación
```python
def validate_scores(predicted, actual):
    # Calcular precisión, recall, F1-score
    # Ajustar parámetros basado en resultados
```

### 5. Métricas de Evaluación

#### Precisión por Categoría
- **Alegría**: Precisión objetivo >75%
- **Tristeza**: Precisión objetivo >75%
- **Enojo**: Precisión objetivo >70%
- **Preocupación**: Precisión objetivo >70%

#### Métricas Generales
- **Accuracy general**: >70%
- **F1-score promedio**: >0.7
- **Tiempo de respuesta**: <1 segundo

### 6. Implementación Práctica

#### Fase 1: Datos de Referencia
1. Crear diccionario de palabras con frecuencias
2. Definir intensidades basadas en análisis lingüístico
3. Establecer reglas de contexto

#### Fase 2: Validación
1. Probar con corpus de textos conocidos
2. Ajustar parámetros iterativamente
3. Validar con casos edge

#### Fase 3: Optimización
1. Refinar reglas de combinación
2. Optimizar para velocidad
3. Documentar resultados

### 7. Ejemplo de Cálculo Real

#### Texto: "Estoy muy feliz hoy"
```
"estoy" → información (0.1)
"muy" → intensificador (×1.5)
"feliz" → alegría base (0.6)
"hoy" → información (0.05)

Cálculo:
- Alegría: 0.6 × 1.5 = 0.9
- Información: 0.1 + 0.05 = 0.15

Resultado: 85% alegría, 15% información
```

### 8. Ventajas del Enfoque Científico

✅ **Objetivo**: Basado en datos reales
✅ **Validable**: Métricas medibles
✅ **Escalable**: Fácil agregar nuevas palabras
✅ **Transparente**: Cada cálculo es explicable
✅ **Mejorable**: Iterativo basado en resultados

### 9. Próximos Pasos

1. **Crear corpus de entrenamiento** con textos etiquetados
2. **Implementar análisis de frecuencia** de palabras
3. **Desarrollar algoritmo de cálculo** basado en datos
4. **Validar con casos de prueba** conocidos
5. **Refinar parámetros** iterativamente

---

**Conclusión**: Los valores actuales son aproximaciones iniciales. Para un sistema robusto, necesitamos implementar el enfoque basado en datos descrito arriba. 