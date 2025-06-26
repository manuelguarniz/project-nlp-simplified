"""
Modelos de Resultados de Análisis de Sentimientos
================================================
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import time


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
    dominant_sentiment: Optional[str] = None  # Sentimiento dominante
    secondary_sentiments: List[str] = None    # Sentimientos secundarios
    analysis_quality: str = "medium"          # 'high', 'medium', 'low'
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if self.secondary_sentiments is None:
            self.secondary_sentiments = []
        
        # Determinar sentimiento dominante si no se especifica
        if self.dominant_sentiment is None:
            self._determine_dominant_sentiment()
        
        # Determinar sentimientos secundarios
        if not self.secondary_sentiments:
            self._determine_secondary_sentiments()
        
        # Determinar calidad del análisis
        self._determine_analysis_quality()
    
    def _determine_dominant_sentiment(self):
        """Determina el sentimiento dominante basado en las puntuaciones"""
        if not self.sentiments:
            self.dominant_sentiment = None
            return
        
        max_score = max(self.sentiments.values())
        dominant_sentiments = [
            sentiment for sentiment, score in self.sentiments.items() 
            if score == max_score
        ]
        
        self.dominant_sentiment = dominant_sentiments[0] if dominant_sentiments else None
    
    def _determine_secondary_sentiments(self):
        """Determina los sentimientos secundarios"""
        if not self.sentiments:
            self.secondary_sentiments = []
            return
        
        # Ordenar sentimientos por puntuación descendente
        sorted_sentiments = sorted(
            self.sentiments.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Tomar los siguientes 2 sentimientos después del dominante
        self.secondary_sentiments = [
            sentiment for sentiment, _ in sorted_sentiments[1:3]
        ]
    
    def _determine_analysis_quality(self):
        """Determina la calidad del análisis basado en la confianza"""
        if self.confidence >= 0.8:
            self.analysis_quality = "high"
        elif self.confidence >= 0.6:
            self.analysis_quality = "medium"
        else:
            self.analysis_quality = "low"
    
    def to_dict(self) -> Dict:
        """Convierte el resultado a diccionario"""
        return {
            'text': self.text,
            'sentiments': self.sentiments,
            'confidence': self.confidence,
            'processing_time': self.processing_time,
            'matched_keywords': self.matched_keywords,
            'tree_path': self.tree_path,
            'modifiers_applied': self.modifiers_applied,
            'dominant_sentiment': self.dominant_sentiment,
            'secondary_sentiments': self.secondary_sentiments,
            'analysis_quality': self.analysis_quality
        }
    
    def __str__(self) -> str:
        """Representación en string del resultado"""
        return f"SentimentResult(dominant='{self.dominant_sentiment}', confidence={self.confidence:.3f})"


@dataclass
class DecisionTreeNode:
    """Nodo del árbol de decisión"""
    id: str
    condition: Optional[str]      # Condición a evaluar (None para nodos hoja)
    branches: Dict[str, str]      # {'true': 'node_id', 'false': 'node_id'}
    sentiment_scores: Dict[str, float]  # Puntuaciones de sentimientos
    keywords: List[str]           # Palabras clave asociadas al nodo
    description: str              # Descripción del nodo
    node_type: str = "decision"   # 'decision', 'leaf', 'root'
    depth: int = 0                # Profundidad en el árbol
    parent_id: Optional[str] = None  # Nodo padre
    children_ids: List[str] = None   # Nodos hijos
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if self.children_ids is None:
            self.children_ids = []
        
        # Validar tipo de nodo
        valid_types = ['decision', 'leaf', 'root']
        if self.node_type not in valid_types:
            raise ValueError(f"Tipo de nodo inválido: {self.node_type}. Debe ser uno de {valid_types}")
        
        # Validar puntuaciones
        for sentiment, score in self.sentiment_scores.items():
            if not 0 <= score <= 1:
                raise ValueError(f"Puntuación inválida para {sentiment}: {score}. Debe estar entre 0 y 1")


@dataclass
class SystemConfig:
    """Configuración del sistema"""
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
    
    def __post_init__(self):
        """Inicializar valores por defecto"""
        if self.sentiment_thresholds is None:
            self.sentiment_thresholds = {
                'alegria': 0.4,
                'tristeza': 0.4,
                'enojo': 0.4,
                'preocupacion': 0.4,
                'informacion': 0.3,
                'sorpresa': 0.4
            }
        
        if self.fuzzy_parameters is None:
            self.fuzzy_parameters = {
                'intensification_factor': 1.5,
                'attenuation_factor': 0.7,
                'negation_factor': 0.3,
                'mixed_emotion_threshold': 0.6,
                'context_weight': 0.3
            }
        
        if self.preprocessing is None:
            self.preprocessing = {
                'remove_punctuation': True,
                'convert_to_lowercase': True,
                'remove_stopwords': False,
                'stemming': False,
                'max_word_length': 20
            }
        
        if self.tree_search is None:
            self.tree_search = {
                'max_depth': 10,
                'timeout_seconds': 5,
                'enable_backtracking': True,
                'cache_size': 1000
            }
        
        if self.output_format is None:
            self.output_format = {
                'include_confidence': True,
                'include_processing_time': True,
                'include_matched_keywords': True,
                'include_tree_path': True,
                'include_modifiers': True,
                'round_decimals': 3
            }
        
        if self.logging is None:
            self.logging = {
                'level': 'INFO',
                'enable_file_logging': True,
                'log_file': 'sentiment_analysis.log',
                'enable_console_logging': True
            } 