"""
Pruebas Unitarias para ScoreNormalizer
=====================================

Pruebas para el módulo de normalización de puntuaciones.
"""

import pytest
from src.utils.normalizer import ScoreNormalizer
from src.models.exceptions import NormalizationError


class TestScoreNormalizer:
    """Pruebas para ScoreNormalizer"""
    
    def test_basic_normalization(self, score_normalizer):
        """TC-NORM-001: Normalización con capped"""
        scores = {'alegria': 0.8, 'tristeza': 0.3, 'enojo': 1.2}
        normalized = score_normalizer.normalize_scores(scores)
        
        assert normalized['alegria'] == 0.8  # Ya está en rango
        assert normalized['tristeza'] == 0.3  # Ya está en rango
        assert normalized['enojo'] == 1.0  # Capped a 1.0
    
    def test_already_normalized_scores(self, score_normalizer):
        """TC-NORM-002: Valores ya normalizados"""
        scores = {'alegria': 0.5, 'tristeza': 0.5, 'enojo': 0.5}
        normalized = score_normalizer.normalize_scores(scores)
        
        assert normalized['alegria'] == 0.5
        assert normalized['tristeza'] == 0.5
        assert normalized['enojo'] == 0.5
    
    def test_zero_scores(self, score_normalizer):
        """TC-NORM-003: Todos en cero"""
        scores = {'alegria': 0.0, 'tristeza': 0.0, 'enojo': 0.0}
        normalized = score_normalizer.normalize_scores(scores)
        
        assert normalized['alegria'] == 0.0
        assert normalized['tristeza'] == 0.0
        assert normalized['enojo'] == 0.0
    
    def test_out_of_range_scores(self, score_normalizer):
        """TC-NORM-004: Valores fuera de rango"""
        scores = {'alegria': -0.5, 'tristeza': 2.0, 'enojo': 0.8}
        normalized = score_normalizer.normalize_scores(scores)
        
        assert normalized['alegria'] == 0.0  # Capped a 0.0
        assert normalized['tristeza'] == 1.0  # Capped a 1.0
        assert normalized['enojo'] == 0.8  # Ya está en rango
    
    def test_empty_scores(self, score_normalizer):
        """TC-NORM-005: Diccionario vacío"""
        scores = {}
        normalized = score_normalizer.normalize_scores(scores)
        
        assert normalized == {}
    
    def test_cap_scores(self, score_normalizer):
        """Prueba función cap_scores"""
        scores = {'alegria': -0.5, 'tristeza': 1.5, 'enojo': 0.8}
        capped = score_normalizer.cap_scores(scores)
        
        assert capped['alegria'] == 0.0
        assert capped['tristeza'] == 1.0
        assert capped['enojo'] == 0.8
    
    def test_cap_scores_invalid_type(self, score_normalizer):
        """Prueba cap_scores con tipo inválido"""
        scores = {'alegria': 'invalid', 'tristeza': 0.5}
        
        with pytest.raises(NormalizationError):
            score_normalizer.cap_scores(scores)
    
    def test_calculate_confidence(self, score_normalizer):
        """Prueba cálculo de confianza"""
        scores = {'alegria': 0.8, 'tristeza': 0.2, 'enojo': 0.0}
        matched_keywords = {
            'alegria': ['feliz'],
            'tristeza': [],
            'enojo': [],
            'preocupacion': [],
            'informacion': [],
            'sorpresa': []
        }
        
        confidence = score_normalizer.calculate_confidence(scores, matched_keywords)
        
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.0  # Debería tener alguna confianza
    
    def test_calculate_confidence_no_keywords(self, score_normalizer):
        """Prueba confianza sin palabras clave"""
        scores = {'alegria': 0.5, 'tristeza': 0.5}
        matched_keywords = {sentiment: [] for sentiment in score_normalizer.sentiments}
        
        confidence = score_normalizer.calculate_confidence(scores, matched_keywords)
        
        assert confidence > 0.0  # Confianza mínima
        assert confidence < 0.5  # Confianza baja sin palabras clave
    
    def test_calculate_confidence_empty_scores(self, score_normalizer):
        """Prueba confianza con puntuaciones vacías"""
        scores = {}
        matched_keywords = {sentiment: [] for sentiment in score_normalizer.sentiments}
        
        confidence = score_normalizer.calculate_confidence(scores, matched_keywords)
        
        assert confidence == 0.0
    
    def test_min_max_normalize(self, score_normalizer):
        """Prueba normalización Min-Max"""
        scores = {'alegria': 0.2, 'tristeza': 0.8, 'enojo': 0.5}
        normalized = score_normalizer._min_max_normalize(scores)
        
        # El mínimo debería ser 0 y el máximo 1
        assert min(normalized.values()) == 0.0
        assert max(normalized.values()) == 1.0
    
    def test_min_max_normalize_same_values(self, score_normalizer):
        """Prueba Min-Max con valores iguales"""
        scores = {'alegria': 0.5, 'tristeza': 0.5, 'enojo': 0.5}
        normalized = score_normalizer._min_max_normalize(scores)
        
        # Todos deberían ser 0.5
        for value in normalized.values():
            assert value == 0.5
    
    def test_z_score_normalize(self, score_normalizer):
        """Prueba normalización Z-Score"""
        scores = {'alegria': 0.2, 'tristeza': 0.8, 'enojo': 0.5}
        normalized = score_normalizer._z_score_normalize(scores)
        
        # Todos deberían estar entre 0 y 1
        for value in normalized.values():
            assert 0.0 <= value <= 1.0
    
    def test_softmax_normalize(self, score_normalizer):
        """Prueba normalización Softmax"""
        scores = {'alegria': 0.2, 'tristeza': 0.8, 'enojo': 0.5}
        normalized = score_normalizer._softmax_normalize(scores)
        
        # La suma debería ser 1.0
        assert abs(sum(normalized.values()) - 1.0) < 0.001
        
        # Todos deberían ser positivos
        for value in normalized.values():
            assert value > 0.0
    
    def test_validate_scores_valid(self, score_normalizer):
        """Prueba validación de puntuaciones válidas"""
        scores = {'alegria': 0.5, 'tristeza': 0.8, 'enojo': 0.2}
        
        assert score_normalizer.validate_scores(scores) == True
    
    def test_validate_scores_invalid_type(self, score_normalizer):
        """Prueba validación con tipo inválido"""
        scores = {'alegria': 'invalid'}
        
        assert score_normalizer.validate_scores(scores) == False
    
    def test_validate_scores_out_of_range(self, score_normalizer):
        """Prueba validación con valores fuera de rango"""
        scores = {'alegria': 1.5, 'tristeza': -0.5}
        
        assert score_normalizer.validate_scores(scores) == False
    
    def test_get_dominant_sentiment(self, score_normalizer):
        """Prueba obtención de sentimiento dominante"""
        scores = {'alegria': 0.3, 'tristeza': 0.8, 'enojo': 0.5}
        
        dominant = score_normalizer.get_dominant_sentiment(scores)
        
        assert dominant == 'tristeza'
    
    def test_get_dominant_sentiment_empty(self, score_normalizer):
        """Prueba sentimiento dominante con puntuaciones vacías"""
        scores = {}
        
        dominant = score_normalizer.get_dominant_sentiment(scores)
        
        assert dominant is None
    
    def test_get_secondary_sentiments(self, score_normalizer):
        """Prueba obtención de sentimientos secundarios"""
        scores = {'alegria': 0.3, 'tristeza': 0.8, 'enojo': 0.5, 'preocupacion': 0.2}
        
        secondary = score_normalizer.get_secondary_sentiments(scores, count=2)
        
        assert len(secondary) == 2
        assert 'enojo' in secondary  # Segundo más alto
        assert 'alegria' in secondary  # Tercero más alto
    
    def test_get_secondary_sentiments_insufficient(self, score_normalizer):
        """Prueba sentimientos secundarios con pocos sentimientos"""
        scores = {'alegria': 0.8, 'tristeza': 0.5}
        
        secondary = score_normalizer.get_secondary_sentiments(scores, count=3)
        
        assert len(secondary) == 1  # Solo hay un sentimiento secundario
        assert 'tristeza' in secondary
    
    def test_keyword_confidence_calculation(self, score_normalizer):
        """Prueba cálculo de confianza basada en palabras clave"""
        matched_keywords = {
            'alegria': ['feliz', 'contento'],
            'tristeza': ['triste'],
            'enojo': [],
            'preocupacion': [],
            'informacion': [],
            'sorpresa': []
        }
        
        confidence = score_normalizer._calculate_keyword_confidence(matched_keywords)
        
        assert confidence > 0.0
        assert confidence <= 1.0
    
    def test_distribution_confidence_calculation(self, score_normalizer):
        """Prueba cálculo de confianza basada en distribución"""
        scores = {'alegria': 0.9, 'tristeza': 0.1, 'enojo': 0.0}
        
        confidence = score_normalizer._calculate_distribution_confidence(scores)
        
        assert confidence > 0.0
        assert confidence <= 1.0
    
    def test_consistency_confidence_calculation(self, score_normalizer):
        """Prueba cálculo de confianza basada en consistencia"""
        scores = {'alegria': 0.8, 'tristeza': 0.1, 'enojo': 0.1}
        
        confidence = score_normalizer._calculate_consistency_confidence(scores)
        
        assert confidence > 0.0
        assert confidence <= 1.0
    
    def test_threshold_confidence_calculation(self, score_normalizer):
        """Prueba cálculo de confianza basada en umbrales"""
        scores = {'alegria': 0.6, 'tristeza': 0.3, 'enojo': 0.1}
        
        confidence = score_normalizer._calculate_threshold_confidence(scores)
        
        assert confidence > 0.0
        assert confidence <= 1.0
    
    def test_rounding_configuration(self, score_normalizer):
        """Prueba configuración de redondeo"""
        # Cambiar configuración de redondeo
        score_normalizer.config.output_format['round_decimals'] = 2
        
        scores = {'alegria': 0.123456, 'tristeza': 0.987654}
        normalized = score_normalizer.normalize_scores(scores)
        
        # Verificar que esté redondeado a 2 decimales
        for value in normalized.values():
            decimal_places = len(str(value).split('.')[-1])
            assert decimal_places <= 2
    
    def test_all_sentiments_covered(self, score_normalizer):
        """Prueba que todos los sentimientos estén cubiertos"""
        scores = {'alegria': 0.5, 'tristeza': 0.3, 'enojo': 0.2}
        normalized = score_normalizer.normalize_scores(scores)
        
        # Debería mantener todos los sentimientos originales
        for sentiment in scores:
            assert sentiment in normalized
    
    def test_confidence_with_mixed_emotions(self, score_normalizer):
        """Prueba confianza con emociones mixtas"""
        scores = {'alegria': 0.7, 'tristeza': 0.6, 'enojo': 0.1}
        matched_keywords = {
            'alegria': ['feliz'],
            'tristeza': ['triste'],
            'enojo': [],
            'preocupacion': [],
            'informacion': [],
            'sorpresa': []
        }
        
        confidence = score_normalizer.calculate_confidence(scores, matched_keywords)
        
        # Confianza debería ser menor con emociones mixtas
        assert confidence < 0.9
    
    def test_confidence_with_clear_dominant(self, score_normalizer):
        """Prueba confianza con sentimiento dominante claro"""
        scores = {'alegria': 0.9, 'tristeza': 0.1, 'enojo': 0.0}
        matched_keywords = {
            'alegria': ['feliz', 'contento'],
            'tristeza': [],
            'enojo': [],
            'preocupacion': [],
            'informacion': [],
            'sorpresa': []
        }
        
        confidence = score_normalizer.calculate_confidence(scores, matched_keywords)
        
        # Confianza debería ser alta con sentimiento dominante claro
        assert confidence > 0.7 