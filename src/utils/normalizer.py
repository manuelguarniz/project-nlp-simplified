"""
Normalizador de Puntuaciones
============================

Módulo responsable de normalizar y ajustar las puntuaciones
de sentimientos al rango [0, 1] y calcular la confianza del análisis.
"""

import math
from typing import Dict, List
from ..models.sentiment_result import SystemConfig
from ..models.exceptions import NormalizationError


class ScoreNormalizer:
    """Normalizador de puntuaciones"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
        self.sentiments = ['alegria', 'tristeza', 'enojo', 'preocupacion', 'informacion', 'sorpresa']
    
    def normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Normaliza las puntuaciones al rango [0, 1]
        
        Args:
            scores: Puntuaciones a normalizar
            
        Returns:
            Puntuaciones normalizadas
        """
        if not scores:
            return {}
        
        # Primero aplicar capped para limitar valores fuera de rango
        capped_scores = self.cap_scores(scores)
        
        # Aplicar normalización Min-Max
        normalized_scores = self._min_max_normalize(capped_scores)
        
        # Redondear según configuración
        decimals = self.config.output_format.get('round_decimals', 3)
        return {k: round(v, decimals) for k, v in normalized_scores.items()}
    
    def cap_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Limita las puntuaciones al rango [0, 1]
        
        Args:
            scores: Puntuaciones a limitar
            
        Returns:
            Puntuaciones limitadas
        """
        capped = {}
        
        for sentiment, score in scores.items():
            if not isinstance(score, (int, float)):
                raise NormalizationError(f"Puntuación inválida para {sentiment}: {score}")
            
            # Limitar al rango [0, 1]
            capped[sentiment] = max(0.0, min(1.0, score))
        
        return capped
    
    def calculate_confidence(self, scores: Dict[str, float], 
                           matched_keywords: Dict[str, List[str]]) -> float:
        """
        Calcula la confianza del análisis
        
        Args:
            scores: Puntuaciones de sentimientos
            matched_keywords: Palabras clave encontradas por sentimiento
            
        Returns:
            Valor de confianza entre 0 y 1
        """
        if not scores:
            return 0.0
        
        # Factor 1: Confianza basada en palabras clave encontradas
        keyword_confidence = self._calculate_keyword_confidence(matched_keywords)
        
        # Factor 2: Confianza basada en distribución de puntuaciones
        distribution_confidence = self._calculate_distribution_confidence(scores)
        
        # Factor 3: Confianza basada en consistencia
        consistency_confidence = self._calculate_consistency_confidence(scores)
        
        # Factor 4: Confianza basada en umbrales
        threshold_confidence = self._calculate_threshold_confidence(scores)
        
        # Promedio ponderado de todos los factores
        confidence = (
            keyword_confidence * 0.4 +
            distribution_confidence * 0.3 +
            consistency_confidence * 0.2 +
            threshold_confidence * 0.1
        )
        
        # Limitar al rango [0, 1]
        return max(0.0, min(1.0, confidence))
    
    def _min_max_normalize(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Aplica normalización Min-Max
        
        Args:
            scores: Puntuaciones a normalizar
            
        Returns:
            Puntuaciones normalizadas
        """
        if not scores:
            return {}
        
        min_score = min(scores.values())
        max_score = max(scores.values())
        
        # Evitar división por cero
        if max_score == min_score:
            return {k: 0.5 for k in scores.keys()}
        
        normalized = {}
        for sentiment, score in scores.items():
            normalized[sentiment] = (score - min_score) / (max_score - min_score)
        
        return normalized
    
    def _z_score_normalize(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Aplica normalización Z-Score
        
        Args:
            scores: Puntuaciones a normalizar
            
        Returns:
            Puntuaciones normalizadas
        """
        if not scores:
            return {}
        
        values = list(scores.values())
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std = math.sqrt(variance)
        
        if std == 0:
            return {k: 0.5 for k in scores.keys()}
        
        normalized = {}
        for sentiment, score in scores.items():
            z_score = (score - mean) / std
            # Convertir Z-score a probabilidad usando función sigmoide
            normalized[sentiment] = 1 / (1 + math.exp(-z_score))
        
        return normalized
    
    def _softmax_normalize(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Aplica normalización Softmax
        
        Args:
            scores: Puntuaciones a normalizar
            
        Returns:
            Puntuaciones normalizadas
        """
        if not scores:
            return {}
        
        values = list(scores.values())
        max_val = max(values)
        
        # Aplicar softmax para evitar overflow
        exp_values = [math.exp(v - max_val) for v in values]
        sum_exp = sum(exp_values)
        
        normalized = {}
        for i, sentiment in enumerate(scores.keys()):
            normalized[sentiment] = exp_values[i] / sum_exp
        
        return normalized
    
    def _calculate_keyword_confidence(self, matched_keywords: Dict[str, List[str]]) -> float:
        """
        Calcula confianza basada en palabras clave encontradas
        
        Args:
            matched_keywords: Palabras clave encontradas por sentimiento
            
        Returns:
            Confianza basada en palabras clave
        """
        total_keywords = sum(len(words) for words in matched_keywords.values())
        
        if total_keywords == 0:
            return 0.1  # Confianza mínima
        
        # Confianza aumenta con más palabras clave encontradas
        # pero se satura después de cierto punto
        confidence = min(1.0, total_keywords / 5.0)  # Máximo en 5 palabras
        
        return confidence
    
    def _calculate_distribution_confidence(self, scores: Dict[str, float]) -> float:
        """
        Calcula confianza basada en distribución de puntuaciones
        
        Args:
            scores: Puntuaciones de sentimientos
            
        Returns:
            Confianza basada en distribución
        """
        if not scores:
            return 0.0
        
        max_score = max(scores.values())
        min_score = min(scores.values())
        
        # Confianza alta si hay buena diferenciación entre sentimientos
        score_range = max_score - min_score
        confidence = min(1.0, score_range * 2)  # Factor 2 para ajustar escala
        
        return confidence
    
    def _calculate_consistency_confidence(self, scores: Dict[str, float]) -> float:
        """
        Calcula confianza basada en consistencia de sentimientos
        
        Args:
            scores: Puntuaciones de sentimientos
            
        Returns:
            Confianza basada en consistencia
        """
        if not scores:
            return 0.0
        
        # Contar sentimientos con puntuación alta
        high_scores = sum(1 for score in scores.values() if score > 0.6)
        total_sentiments = len(scores)
        
        # Confianza alta si hay pocos sentimientos dominantes
        if high_scores == 0:
            return 0.3  # Confianza baja si no hay sentimientos claros
        elif high_scores == 1:
            return 0.9  # Confianza alta si hay un sentimiento dominante
        else:
            # Confianza disminuye con múltiples sentimientos altos
            return max(0.3, 1.0 - (high_scores - 1) * 0.2)
    
    def _calculate_threshold_confidence(self, scores: Dict[str, float]) -> float:
        """
        Calcula confianza basada en umbrales de sentimientos
        
        Args:
            scores: Puntuaciones de sentimientos
            
        Returns:
            Confianza basada en umbrales
        """
        if not scores or not self.config.sentiment_thresholds:
            return 0.5
        
        threshold_matches = 0
        total_sentiments = 0
        
        for sentiment, score in scores.items():
            if sentiment in self.config.sentiment_thresholds:
                threshold = self.config.sentiment_thresholds[sentiment]
                if score >= threshold:
                    threshold_matches += 1
                total_sentiments += 1
        
        if total_sentiments == 0:
            return 0.5
        
        # Confianza basada en qué tan bien se superan los umbrales
        return threshold_matches / total_sentiments
    
    def validate_scores(self, scores: Dict[str, float]) -> bool:
        """
        Valida que las puntuaciones sean correctas
        
        Args:
            scores: Puntuaciones a validar
            
        Returns:
            True si las puntuaciones son válidas
        """
        if not isinstance(scores, dict):
            return False
        
        for sentiment, score in scores.items():
            if not isinstance(score, (int, float)):
                return False
            
            if score < 0 or score > 1:
                return False
        
        return True
    
    def get_dominant_sentiment(self, scores: Dict[str, float]) -> str:
        """
        Obtiene el sentimiento dominante
        
        Args:
            scores: Puntuaciones de sentimientos
            
        Returns:
            Sentimiento dominante
        """
        if not scores:
            return None
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def get_secondary_sentiments(self, scores: Dict[str, float], count: int = 2) -> List[str]:
        """
        Obtiene los sentimientos secundarios
        
        Args:
            scores: Puntuaciones de sentimientos
            count: Número de sentimientos secundarios a obtener
            
        Returns:
            Lista de sentimientos secundarios
        """
        if not scores:
            return []
        
        # Ordenar por puntuación descendente
        sorted_sentiments = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Tomar los siguientes después del dominante
        secondary = [sentiment for sentiment, _ in sorted_sentiments[1:count+1]]
        
        return secondary 