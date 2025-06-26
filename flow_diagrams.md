# Diagramas de Flujo del Sistema de Análisis de Sentimientos

## 1. Flujo Principal del Sistema

```mermaid
flowchart TD
    A[Entrada de Texto] --> B{Validar Texto}
    B -->|Válido| C[Preprocesamiento]
    B -->|Inválido| D[Error: Texto inválido]
  
    C --> E[Tokenización]
    E --> F[Normalización]
    F --> G[Detección de Negaciones]
  
    G --> H[Árbol de Decisión]
    H --> I[Evaluar Condiciones]
    I --> J[Acumular Puntuaciones]
  
    J --> K[Lógica Difusa]
    K --> L[Aplicar Intensificadores]
    L --> M[Aplicar Negaciones]
    M --> N[Combinar Sentimientos]
  
    N --> O[Normalizar Resultados]
    O --> P[Formatear Salida]
    P --> Q[Mostrar Porcentajes]
  
    Q --> R{¿Nuevo Texto?}
    R -->|Sí| A
    R -->|No| S[Fin]
  
    D --> S
```

## 2. Algoritmo de Búsqueda en Árbol

```mermaid
flowchart TD
    A[Iniciar en Nodo Raíz] --> B[Acumular Puntuaciones del Nodo]
    B --> C{¿Es Nodo Hoja?}
  
    C -->|Sí| D[Retornar Puntuaciones Finales]
    C -->|No| E[Evaluar Condición del Nodo]
  
    E --> F{¿Condición Verdadera?}
    F -->|Sí| G[Ir a Rama Verdadera]
    F -->|No| H[Ir a Rama Falsa]
  
    G --> I{¿Nodo Existe?}
    H --> I
  
    I -->|Sí| B
    I -->|No| J[Error: Nodo no encontrado]
  
    J --> K[Retornar Puntuaciones Actuales]
    D --> L[Fin]
    K --> L
```

## 3. Proceso de Preprocesamiento

```mermaid
flowchart TD
    A[Texto Original] --> B[Convertir a Minúsculas]
    B --> C[Eliminar Puntuación]
    C --> D[Eliminar Espacios Extra]
    D --> E[Tokenizar por Espacios]
  
    E --> F[Filtrar Tokens Vacíos]
    F --> G[Detectar Negaciones]
  
    G --> H{¿Hay Negaciones?}
    H -->|Sí| I[Marcar Tokens Negados]
    H -->|No| J[Continuar]
  
    I --> K[Detectar Intensificadores]
    J --> K
  
    K --> L{¿Hay Intensificadores?}
    L -->|Sí| M[Marcar Tokens Intensificados]
    L -->|No| N[Continuar]
  
    M --> O[Tokens Preprocesados]
    N --> O
    O --> P[Fin Preprocesamiento]
```

## 4. Lógica Difusa - Aplicación de Reglas

```mermaid
flowchart TD
    A[Puntuaciones Base] --> B[Regla 1: Intensificadores]
    B --> C{¿Hay Intensificadores?}
  
    C -->|Sí| D[Aplicar ×1.5]
    C -->|No| E[Continuar]
  
    D --> F[Regla 2: Atenuadores]
    E --> F
  
    F --> G{¿Hay Atenuadores?}
    G -->|Sí| H[Aplicar ×0.7]
    G -->|No| I[Continuar]
  
    H --> J[Regla 3: Negaciones]
    I --> J
  
    J --> K{¿Hay Negaciones?}
    K -->|Sí| L[Aplicar ×(- 0.8)]
    K -->|No| M[Continuar]
  
    L --> N[Regla 4: Combinación]
    M --> N
  
    N --> O{¿Múltiples Sentimientos?}
    O -->|Sí| P[Aplicar Factor 0.8]
    O -->|No| Q[Continuar]
  
    P --> R[Aplicar Cap]
    Q --> R
  
    R --> S[Puntuaciones Finales]
```

## 5. Evaluación de Condiciones del Árbol

```mermaid
flowchart TD
    A[Tokens del Texto] --> B[has_emotion_words]
    B --> C{¿Contiene Palabras Emocionales?}
  
    C -->|Sí| D[has_positive_words]
    C -->|No| E[has_informational_words]
  
    D --> F{¿Contiene Palabras Positivas?}
    F -->|Sí| G[has_high_intensity_joy]
    F -->|No| H[has_negative_words]
  
    G --> I{¿Alta Intensidad de Alegría?}
    I -->|Sí| J[very_happy]
    I -->|No| K[moderately_happy]
  
    H --> L{¿Contiene Palabras Negativas?}
    L -->|Sí| M[has_sadness_words]
    L -->|No| N[neutral_emotion]
  
    M --> O{¿Contiene Palabras de Tristeza?}
    O -->|Sí| P[has_high_intensity_sadness]
    O -->|No| Q[has_anger_words]
  
    E --> R{¿Contiene Palabras Informativas?}
    R -->|Sí| S[informational]
    R -->|No| T[neutral_emotion]
  
    J --> U[Resultado: Muy Feliz]
    K --> V[Resultado: Moderadamente Feliz]
    P --> W[Resultado: Muy Triste]
    Q --> X[Resultado: Enojado]
    S --> Y[Resultado: Informativo]
    T --> Z[Resultado: Neutral]
    N --> Z
```

## 6. Cálculo de Puntuaciones con Cap

```mermaid
flowchart TD
    A[Puntuación Calculada] --> B{¿Valor > 1.0?}
    B -->|Sí| C[CAPPED a 1.0]
    B -->|No| D{¿Valor < 0.0?}
  
    D -->|Sí| E[CAPPED a 0.0]
    D -->|No| F[Mantener Valor]
  
    C --> G[Puntuación Final]
    E --> G
    F --> G
  
    G --> H[Normalizar si es necesario]
    H --> I[Resultado Final]
```

## 7. Flujo de Normalización

```mermaid
flowchart TD
    A[Puntuaciones con Cap] --> B[Calcular Suma Total]
    B --> C{¿Suma Total > 0?}
  
    C -->|Sí| D[Dividir cada puntuación por total]
    C -->|No| E[Mantener puntuaciones originales]
  
    D --> F[Convertir a Porcentajes]
    E --> F
  
    F --> G[Formatear Resultados]
    G --> H[Mostrar: X% Sentimiento]
    H --> I[Fin]
```

## 8. Detección de Negaciones

```mermaid
flowchart TD
    A[Tokens del Texto] --> B[Buscar Palabras de Negación]
    B --> C{¿Encontró Negación?}
  
    C -->|Sí| D[Identificar Palabra Siguiente]
    C -->|No| E[No hay Negaciones]
  
    D --> F{¿Palabra Siguiente es Emocional?}
    F -->|Sí| G[Marcar como Negada]
    F -->|No| H[Ignorar Negación]
  
    G --> I[Aplicar Factor -0.8]
    H --> J[Continuar Normal]
    E --> J
  
    I --> K[Puntuación Negada]
    J --> L[Puntuación Normal]
    K --> M[Resultado Final]
    L --> M
```

## 9. Aplicación de Intensificadores

```mermaid
flowchart TD
    A[Tokens del Texto] --> B[Buscar Intensificadores]
    B --> C{¿Encontró Intensificador?}
  
    C -->|Sí| D[Identificar Palabra Siguiente]
    C -->|No| E[No hay Intensificadores]
  
    D --> F{¿Palabra Siguiente es Emocional?}
    F -->|Sí| G[Determinar Tipo de Intensificador]
    F -->|No| H[Ignorar Intensificador]
  
    G --> I{¿Tipo de Intensificador?}
    I -->|"muy"| J[Aplicar ×1.5]
    I -->|"extremadamente"| K[Aplicar ×1.8]
    I -->|"un poco"| L[Aplicar ×0.7]
    I -->|Otro| M[Aplicar ×1.2]
  
    J --> N[Puntuación Intensificada]
    K --> N
    L --> N
    M --> N
    H --> O[Puntuación Normal]
    E --> O
  
    N --> P[Aplicar Cap]
    O --> P
    P --> Q[Resultado Final]
```

## 10. Flujo Completo de Análisis

```mermaid
flowchart TD
    A[Usuario Ingresa Texto] --> B[Validar Longitud ≤ 50 palabras]
    B --> C{¿Texto Válido?}
  
    C -->|Sí| D[Preprocesar Texto]
    C -->|No| E[Error: Texto muy largo]
  
    D --> F[Cargar Árbol de Decisión]
    F --> G[Iniciar Búsqueda en Árbol]
  
    G --> H[Recorrer Nodos]
    H --> I[Evaluar Condiciones]
    I --> J[Acumular Puntuaciones]
  
    J --> K{¿Llegó a Nodo Hoja?}
    K -->|No| H
    K -->|Sí| L[Aplicar Lógica Difusa]
  
    L --> M[Detectar Modificadores]
    M --> N[Aplicar Reglas]
    N --> O[Normalizar Resultados]
  
    O --> P[Formatear Salida]
    P --> Q[Mostrar: "X% Alegría, Y% Tristeza..."]
  
    Q --> R{¿Analizar Otro Texto?}
    R -->|Sí| A
    R -->|No| S[Terminar Programa]
  
    E --> S
```

## 11. Manejo de Errores

```mermaid
flowchart TD
    A[Entrada del Usuario] --> B{¿Texto Vacío?}
    B -->|Sí| C[Error: Texto vacío]
    B -->|No| D{¿Texto Muy Largo?}
  
    D -->|Sí| E[Error: Máximo 50 palabras]
    D -->|No| F{¿Contiene Caracteres Inválidos?}
  
    F -->|Sí| G[Error: Caracteres no permitidos]
    F -->|No| H{¿No Encuentra Palabras Clave?}
  
    H -->|Sí| I[Resultado: 100% Información]
    H -->|No| J[Procesar Normalmente]
  
    C --> K[Mostrar Mensaje de Error]
    E --> K
    G --> K
  
    K --> L{¿Reintentar?}
    L -->|Sí| A
    L -->|No| M[Salir]
  
    I --> N[Mostrar Resultado]
    J --> N
    N --> O[Continuar]
```

## 12. Optimización con Memoización

```mermaid
flowchart TD
    A[Evaluar Condición] --> B{¿Ya Calculada?}
    B -->|Sí| C[Retornar Resultado Cacheado]
    B -->|No| D[Ejecutar Cálculo]
  
    D --> E[Guardar en Cache]
    E --> F[Retornar Resultado]
  
    C --> G[Continuar]
    F --> G
  
    G --> H{¿Cache Lleno?}
    H -->|Sí| I[Limpiar Cache Antiguo]
    H -->|No| J[Continuar]
  
    I --> J
    J --> K[Fin]
```

---

## Notas sobre los Diagramas

### **Símbolos Utilizados:**

- **Rectángulos**: Procesos/Acciones
- **Diamantes**: Decisiones/Condiciones
- **Óvalos**: Inicio/Fin
- **Flechas**: Flujo de ejecución

### **Colores Sugeridos:**

- **Verde**: Procesos exitosos
- **Rojo**: Errores/Excepciones
- **Amarillo**: Decisiones
- **Azul**: Procesos normales

### **Ventajas de estos Diagramas:**

✅ **Claridad visual**: Fácil de entender el flujo
✅ **Documentación**: Ayuda a explicar el sistema
✅ **Debugging**: Facilita identificar problemas
✅ **Mantenimiento**: Fácil de actualizar y modificar

Estos diagramas proporcionan una visión completa del sistema de análisis de sentimientos, desde la entrada del texto hasta la generación de resultados finales.
