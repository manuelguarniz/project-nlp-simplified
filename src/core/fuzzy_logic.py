"""
Procesador de Lógica Difusa
===========================

Módulo responsable de aplicar reglas de lógica difusa a las puntuaciones
de sentimientos, incluyendo intensificación, atenuación y negación.
"""

import math
from typing import Dict, List
from ..models.sentiment_result import SystemConfig
from ..models.exceptions import FuzzyLogicError


class FuzzyLogicProcessor:
    """Procesador de lógica difusa"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
        self.sentiments = ['alegria', 'tristeza', 'enojo', 'preocupacion', 'informacion', 'sorpresa']
    
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
        if not base_scores:
            return {}
        
        # Copiar puntuaciones base
        adjusted_scores = base_scores.copy()
        
        # Aplicar intensificación
        if modifiers.get('intensifiers'):
            for sentiment in adjusted_scores:
                adjusted_scores[sentiment] = self.intensify_sentiment(
                    adjusted_scores[sentiment], 
                    modifiers['intensifiers']
                )
        
        # Aplicar atenuación
        if modifiers.get('attenuators'):
            for sentiment in adjusted_scores:
                adjusted_scores[sentiment] = self.attenuate_sentiment(
                    adjusted_scores[sentiment], 
                    modifiers['attenuators']
                )
        
        # Aplicar negación
        if modifiers.get('negations'):
            adjusted_scores = self.apply_negation(adjusted_scores, modifiers['negations'])
        
        # Aplicar contexto
        adjusted_scores = self._apply_context_rules(adjusted_scores, modifiers)
        
        # Combinar emociones mixtas
        adjusted_scores = self.combine_emotions(adjusted_scores)
        
        # Limitar al rango [0, 1]
        return {k: max(0.0, min(1.0, v)) for k, v in adjusted_scores.items()}
    
    def intensify_sentiment(self, score: float, intensifiers: List[str]) -> float:
        """
        Intensifica un sentimiento basado en intensificadores
        
        Args:
            score: Puntuación base del sentimiento
            intensifiers: Lista de intensificadores encontrados
            
        Returns:
            Puntuación intensificada
        """
        if not intensifiers or score <= 0:
            return score
        
        # Factor de intensificación basado en configuración
        intensification_factor = self.config.fuzzy_parameters.get('intensification_factor', 1.5)
        
        # Calcular factor total
        factor = 1.0 + (len(intensifiers) * intensification_factor)
        
        # Aplicar intensificación
        intensified_score = score * factor
        
        # Limitar al máximo
        return min(1.0, intensified_score)
    
    def attenuate_sentiment(self, score: float, attenuators: List[str]) -> float:
        """
        Atenúa un sentimiento basado en atenuadores
        
        Args:
            score: Puntuación base del sentimiento
            attenuators: Lista de atenuadores encontrados
            
        Returns:
            Puntuación atenuada
        """
        if not attenuators or score <= 0:
            return score
        
        # Factor de atenuación basado en configuración
        attenuation_factor = self.config.fuzzy_parameters.get('attenuation_factor', 0.7)
        
        # Calcular factor total (exponencial)
        factor = attenuation_factor ** len(attenuators)
        
        # Aplicar atenuación
        attenuated_score = score * factor
        
        return attenuated_score
    
    def apply_negation(self, scores: Dict[str, float], negations: List[str]) -> Dict[str, float]:
        """
        Aplica negaciones a las puntuaciones
        
        Args:
            scores: Puntuaciones de sentimientos
            negations: Lista de negaciones encontradas
            
        Returns:
            Puntuaciones con negación aplicada
        """
        if not negations:
            return scores
        
        # Número impar de negaciones invierte las puntuaciones
        if len(negations) % 2 == 1:
            negated_scores = {}
            for sentiment, score in scores.items():
                negated_scores[sentiment] = 1.0 - score
            return negated_scores
        
        # Número par de negaciones mantiene las puntuaciones originales
        return scores
    
    def combine_emotions(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        Combina emociones mixtas usando operadores difusos
        
        Args:
            scores: Puntuaciones de sentimientos
            
        Returns:
            Puntuaciones combinadas
        """
        if not scores:
            return {}
        
        # Detectar emociones mixtas
        high_scores = {k: v for k, v in scores.items() if v > 0.6}
        
        if len(high_scores) <= 1:
            return scores
        
        # Aplicar operador difuso AND para emociones mixtas
        mixed_emotion_threshold = self.config.fuzzy_parameters.get('mixed_emotion_threshold', 0.6)
        
        combined_scores = scores.copy()
        
        # Reducir puntuaciones de emociones secundarias
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        for i, (sentiment, score) in enumerate(sorted_scores[1:], 1):
            if score > mixed_emotion_threshold:
                # Reducir puntuación de emociones secundarias
                reduction_factor = 1.0 - (i * 0.2)  # Reducir 20% por cada nivel
                combined_scores[sentiment] = score * max(0.3, reduction_factor)
        
        return combined_scores
    
    def _apply_context_rules(self, scores: Dict[str, float], modifiers: Dict[str, List[str]]) -> Dict[str, float]:
        """
        Aplica reglas de contexto basadas en modificadores
        
        Args:
            scores: Puntuaciones de sentimientos
            modifiers: Modificadores extraídos
            
        Returns:
            Puntuaciones ajustadas por contexto
        """
        context_weight = self.config.fuzzy_parameters.get('context_weight', 0.3)
        adjusted_scores = scores.copy()
        
        # Ajustar basado en emoticones
        if modifiers.get('emoticons'):
            emoticon_count = len(modifiers['emoticons'])
            # Aumentar alegría si hay emoticones positivos
            if 'alegria' in adjusted_scores:
                emoticon_boost = min(0.2, emoticon_count * 0.1)
                adjusted_scores['alegria'] = min(1.0, adjusted_scores['alegria'] + emoticon_boost)
        
        # Ajustar basado en exclamaciones
        if modifiers.get('exclamation_count', 0) > 0:
            exclamation_boost = min(0.15, modifiers['exclamation_count'] * 0.05)
            # Aumentar el sentimiento dominante
            dominant_sentiment = max(scores.items(), key=lambda x: x[1])[0]
            if dominant_sentiment in adjusted_scores:
                adjusted_scores[dominant_sentiment] = min(1.0, adjusted_scores[dominant_sentiment] + exclamation_boost)
        
        # Ajustar basado en interrogaciones
        if modifiers.get('question_count', 0) > 0:
            # Aumentar sorpresa e información
            question_boost = min(0.1, modifiers['question_count'] * 0.05)
            if 'sorpresa' in adjusted_scores:
                adjusted_scores['sorpresa'] = min(1.0, adjusted_scores['sorpresa'] + question_boost)
            if 'informacion' in adjusted_scores:
                adjusted_scores['informacion'] = min(1.0, adjusted_scores['informacion'] + question_boost)
        
        return adjusted_scores
    
    def fuzzy_and(self, a: float, b: float) -> float:
        """
        Operador difuso AND (mínimo)
        
        Args:
            a: Primer valor
            b: Segundo valor
            
        Returns:
            Resultado del operador AND difuso
        """
        return min(a, b)
    
    def fuzzy_or(self, a: float, b: float) -> float:
        """
        Operador difuso OR (máximo)
        
        Args:
            a: Primer valor
            b: Segundo valor
            
        Returns:
            Resultado del operador OR difuso
        """
        return max(a, b)
    
    def fuzzy_not(self, a: float) -> float:
        """
        Operador difuso NOT (complemento)
        
        Args:
            a: Valor de entrada
            
        Returns:
            Resultado del operador NOT difuso
        """
        return 1.0 - a
    
    def fuzzy_implication(self, antecedent: float, consequent: float) -> float:
        """
        Implicación difusa
        
        Args:
            antecedent: Antecedente
            consequent: Consecuente
            
        Returns:
            Resultado de la implicación difusa
        """
        return max(1.0 - antecedent, consequent)
    
    def calculate_membership(self, value: float, low: float, high: float) -> float:
        """
        Calcula el grado de pertenencia a un conjunto difuso
        
        Args:
            value: Valor a evaluar
            low: Límite inferior del conjunto
            high: Límite superior del conjunto
            
        Returns:
            Grado de pertenencia [0, 1]
        """
        if value <= low:
            return 0.0
        elif value >= high:
            return 1.0
        else:
            return (value - low) / (high - low)
    
    def defuzzify_centroid(self, membership_values: Dict[str, float]) -> float:
        """
        Defuzzificación por centroide
        
        Args:
            membership_values: Valores de pertenencia por categoría
            
        Returns:
            Valor defuzzificado
        """
        if not membership_values:
            return 0.0
        
        # Calcular centroide ponderado
        weighted_sum = sum(value * membership for value, membership in membership_values.items())
        total_membership = sum(membership_values.values())
        
        if total_membership == 0:
            return 0.0
        
        return weighted_sum / total_membership
    
    def validate_modifiers(self, modifiers: Dict[str, List[str]]) -> bool:
        """
        Valida que los modificadores sean correctos
        
        Args:
            modifiers: Modificadores a validar
            
        Returns:
            True si los modificadores son válidos
        """
        if not isinstance(modifiers, dict):
            return False
        
        valid_keys = {'intensifiers', 'attenuators', 'negations', 'emoticons', 
                     'exclamation_count', 'question_count'}
        
        for key in modifiers:
            if key not in valid_keys:
                return False
            
            if key in ['exclamation_count', 'question_count']:
                if not isinstance(modifiers[key], int):
                    return False
            else:
                if not isinstance(modifiers[key], list):
                    return False
        
        return True 