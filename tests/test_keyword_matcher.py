"""
Pruebas Unitarias para KeywordMatcher
====================================

Pruebas para el módulo de coincidencia de palabras clave.
"""

import pytest
from src.utils.keyword_matcher import KeywordMatcher
from src.models.exceptions import KeywordMatchError


class TestKeywordMatcher:
    """Pruebas para KeywordMatcher"""
    
    def test_basic_keyword_match(self, keyword_matcher):
        """TC-KW-001: Palabra clave de alegría"""
        words = ['estoy', 'muy', 'feliz', 'hoy']
        matches = keyword_matcher.find_matches(words)
        
        assert 'feliz' in matches['alegria']
        assert len(matches['tristeza']) == 0
        assert len(matches['enojo']) == 0
    
    def test_sadness_keyword_match(self, keyword_matcher):
        """TC-KW-002: Palabra clave de tristeza"""
        words = ['me', 'siento', 'triste']
        matches = keyword_matcher.find_matches(words)
        
        assert 'triste' in matches['tristeza']
        assert len(matches['alegria']) == 0
        assert len(matches['enojo']) == 0
    
    def test_multiple_sentiments(self, keyword_matcher):
        """TC-KW-003: Múltiples sentimientos"""
        words = ['estoy', 'enojado', 'y', 'triste']
        matches = keyword_matcher.find_matches(words)
        
        assert 'enojado' in matches['enojo']
        assert 'triste' in matches['tristeza']
        assert len(matches['alegria']) == 0
    
    def test_empty_word_list(self, keyword_matcher):
        """TC-KW-004: Lista vacía"""
        words = []
        matches = keyword_matcher.find_matches(words)
        
        for sentiment in matches:
            assert len(matches[sentiment]) == 0
    
    def test_no_keywords_found(self, keyword_matcher):
        """TC-KW-005: Sin palabras clave"""
        words = ['xyz', 'abc', 'def']
        matches = keyword_matcher.find_matches(words)
        
        for sentiment in matches:
            assert len(matches[sentiment]) == 0
    
    def test_uppercase_keywords(self, keyword_matcher):
        """TC-KW-006: Palabras en mayúsculas"""
        words = ['FELIZ', 'TRISTE', 'ENOJADO']
        matches = keyword_matcher.find_matches(words)
        
        assert 'FELIZ' in matches['alegria']
        assert 'TRISTE' in matches['tristeza']
        assert 'ENOJADO' in matches['enojo']
    
    def test_synonym_matching(self, keyword_matcher):
        """Prueba coincidencia de sinónimos"""
        words = ['gozoso', 'radiante', 'eufórico']
        matches = keyword_matcher.find_matches(words)
        
        assert 'gozoso' in matches['alegria']
        assert 'radiante' in matches['alegria']
        assert 'eufórico' in matches['alegria']
    
    def test_verb_form_matching(self, keyword_matcher):
        """Prueba coincidencia de formas verbales"""
        words = ['alegrarse', 'regocijarse', 'celebrar']
        matches = keyword_matcher.find_matches(words)
        
        assert 'alegrarse' in matches['alegria']
        assert 'regocijarse' in matches['alegria']
        assert 'celebrar' in matches['alegria']
    
    def test_mixed_keyword_types(self, keyword_matcher):
        """Prueba mezcla de tipos de palabras clave"""
        words = ['feliz', 'gozoso', 'alegrarse']
        matches = keyword_matcher.find_matches(words)
        
        assert len(matches['alegria']) == 3
        assert 'feliz' in matches['alegria']
        assert 'gozoso' in matches['alegria']
        assert 'alegrarse' in matches['alegria']
    
    def test_case_insensitive_matching(self, keyword_matcher):
        """Prueba coincidencia insensible a mayúsculas"""
        words = ['Feliz', 'TRISTE', 'enojado']
        matches = keyword_matcher.find_matches(words)
        
        assert 'Feliz' in matches['alegria']
        assert 'TRISTE' in matches['tristeza']
        assert 'enojado' in matches['enojo']
    
    def test_calculate_word_scores(self, keyword_matcher):
        """Prueba cálculo de puntuaciones de palabras"""
        matches = {
            'alegria': ['feliz', 'gozoso'],
            'tristeza': ['triste'],
            'enojo': [],
            'preocupacion': [],
            'informacion': [],
            'sorpresa': []
        }
        
        scores = keyword_matcher.calculate_word_scores(matches)
        
        assert scores['alegria'] > scores['tristeza']
        assert scores['enojo'] == 0.0
        assert scores['preocupacion'] == 0.0
    
    def test_calculate_word_scores_empty(self, keyword_matcher):
        """Prueba cálculo de puntuaciones sin coincidencias"""
        matches = {sentiment: [] for sentiment in keyword_matcher.sentiments}
        
        scores = keyword_matcher.calculate_word_scores(matches)
        
        for sentiment in scores:
            assert scores[sentiment] == 0.0
    
    def test_calculate_word_scores_single_match(self, keyword_matcher):
        """Prueba cálculo de puntuaciones con una sola coincidencia"""
        matches = {
            'alegria': ['feliz'],
            'tristeza': [],
            'enojo': [],
            'preocupacion': [],
            'informacion': [],
            'sorpresa': []
        }
        
        scores = keyword_matcher.calculate_word_scores(matches)
        
        assert scores['alegria'] > 0.0
        assert scores['alegria'] <= 1.0
        for sentiment in ['tristeza', 'enojo', 'preocupacion', 'informacion', 'sorpresa']:
            assert scores[sentiment] == 0.0
    
    def test_get_keyword_info(self, keyword_matcher):
        """Prueba obtención de información de palabra clave"""
        info = keyword_matcher.get_keyword_info('feliz')
        
        assert info['sentiment'] == 'alegria'
        assert info['type'] == 'keyword'
        assert info['word'] == 'feliz'
        assert info['weight'] == 0.3
    
    def test_get_keyword_info_synonym(self, keyword_matcher):
        """Prueba información de sinónimo"""
        info = keyword_matcher.get_keyword_info('gozoso')
        
        assert info['sentiment'] == 'alegria'
        assert info['type'] == 'synonym'
        assert info['weight'] == 0.2
    
    def test_get_keyword_info_verb_form(self, keyword_matcher):
        """Prueba información de forma verbal"""
        info = keyword_matcher.get_keyword_info('alegrarse')
        
        assert info['sentiment'] == 'alegria'
        assert info['type'] == 'verb_form'
        assert info['weight'] == 0.25
    
    def test_get_keyword_info_unknown(self, keyword_matcher):
        """Prueba información de palabra desconocida"""
        info = keyword_matcher.get_keyword_info('xyz')
        
        assert info['sentiment'] is None
        assert info['type'] == 'unknown'
        assert info['weight'] == 0.0
    
    def test_get_sentiment_keywords(self, keyword_matcher):
        """Prueba obtención de palabras clave por sentimiento"""
        keywords = keyword_matcher.get_sentiment_keywords('alegria')
        
        assert 'feliz' in keywords
        assert 'contento' in keywords
        assert 'gozoso' in keywords
        assert 'alegrarse' in keywords
    
    def test_get_sentiment_keywords_empty(self, keyword_matcher):
        """Prueba obtención de palabras clave para sentimiento inexistente"""
        keywords = keyword_matcher.get_sentiment_keywords('inexistente')
        
        assert len(keywords) == 0
    
    def test_load_keywords_from_file(self, temp_keywords_file):
        """Prueba carga de palabras clave desde archivo"""
        matcher = KeywordMatcher(temp_keywords_file)
        
        words = ['feliz', 'triste']
        matches = matcher.find_matches(words)
        
        assert 'feliz' in matches['alegria']
        assert 'triste' in matches['tristeza']
    
    def test_load_keywords_invalid_format(self):
        """Prueba carga con formato inválido"""
        with pytest.raises(KeywordMatchError):
            KeywordMatcher("archivo_inexistente.json")
    
    def test_weighted_score_calculation(self, keyword_matcher):
        """Prueba cálculo de puntuación ponderada"""
        words = ['feliz', 'gozoso', 'alegrarse']
        weighted_score = keyword_matcher._calculate_weighted_score('alegria', words)
        
        # Debería ser mayor que 0 y menor o igual a 0.5
        assert weighted_score > 0.0
        assert weighted_score <= 0.5
    
    def test_weighted_score_unknown_sentiment(self, keyword_matcher):
        """Prueba puntuación ponderada para sentimiento desconocido"""
        words = ['feliz']
        weighted_score = keyword_matcher._calculate_weighted_score('inexistente', words)
        
        assert weighted_score == 0.0
    
    def test_all_sentiments_covered(self, keyword_matcher):
        """Prueba que todos los sentimientos estén cubiertos"""
        words = ['feliz', 'triste', 'enojado', 'preocupado', 'informar', 'sorprendido']
        matches = keyword_matcher.find_matches(words)
        
        for sentiment in keyword_matcher.sentiments:
            assert sentiment in matches
            assert isinstance(matches[sentiment], list)
    
    def test_duplicate_keywords(self, keyword_matcher):
        """Prueba manejo de palabras clave duplicadas"""
        words = ['feliz', 'feliz', 'triste', 'triste']
        matches = keyword_matcher.find_matches(words)
        
        # Debería contar cada ocurrencia
        assert matches['alegria'].count('feliz') == 2
        assert matches['tristeza'].count('triste') == 2
    
    def test_special_characters_in_keywords(self, keyword_matcher):
        """Prueba palabras clave con caracteres especiales"""
        # Agregar palabras clave con caracteres especiales al fixture
        keyword_matcher.keywords['alegria']['keywords'].append('¡feliz!')
        
        words = ['¡feliz!', 'triste']
        matches = keyword_matcher.find_matches(words)
        
        assert '¡feliz!' in matches['alegria']
        assert 'triste' in matches['tristeza']
    
    def test_empty_synonym_groups(self, keyword_matcher):
        """Prueba grupos de sinónimos vacíos"""
        # Agregar grupo de sinónimos vacío
        keyword_matcher.keywords['alegria']['synonyms'].append([])
        
        words = ['feliz']
        matches = keyword_matcher.find_matches(words)
        
        # No debería causar errores
        assert 'feliz' in matches['alegria']
    
    def test_empty_verb_forms(self, keyword_matcher):
        """Prueba formas verbales vacías"""
        # Agregar forma verbal vacía
        keyword_matcher.keywords['alegria']['verb_forms'].append([])
        
        words = ['feliz']
        matches = keyword_matcher.find_matches(words)
        
        # No debería causar errores
        assert 'feliz' in matches['alegria'] 