"""
Pruebas de Integración
=====================

Pruebas de integración para el sistema completo de análisis de sentimientos.
"""

import pytest
import json
import tempfile
import os
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.models.sentiment_result import SystemConfig
from src.models.exceptions import SentimentAnalysisError


class TestIntegration:
    """Pruebas de integración del sistema completo"""
    
    def test_full_analysis_pipeline(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-001: Pipeline completo de análisis"""
        # Crear archivos temporales para recursos
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_keywords_data, f)
            keywords_file = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_tree_data, f)
            tree_file = f.name
        
        try:
            # Mock de carga de recursos
            original_load_keywords = SentimentAnalyzer._load_keywords_data
            original_load_tree = SentimentAnalyzer._load_tree_data
            
            def mock_load_keywords(self):
                return sample_keywords_data
            
            def mock_load_tree(self):
                return sample_tree_data
            
            SentimentAnalyzer._load_keywords_data = mock_load_keywords
            SentimentAnalyzer._load_tree_data = mock_load_tree
            
            # Crear analizador
            analyzer = SentimentAnalyzer(sample_config)
            
            # Analizar texto
            result = analyzer.analyze("Estoy muy feliz hoy")
            
            # Verificar resultado completo
            assert result.text == "Estoy muy feliz hoy"
            assert result.dominant_sentiment == "alegria"
            assert result.confidence > 0.0
            assert result.processing_time > 0.0
            assert len(result.sentiments) > 0
            assert len(result.matched_keywords) > 0
            assert len(result.tree_path) > 0
            assert result.analysis_quality in ['high', 'medium', 'low']
            
        finally:
            # Restaurar métodos originales
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
            
            # Limpiar archivos temporales
            os.unlink(keywords_file)
            os.unlink(tree_file)
    
    def test_positive_sentiment_analysis(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-002: Análisis de sentimiento positivo"""
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            result = analyzer.analyze("¡Estoy extremadamente feliz!")
            
            assert result.dominant_sentiment == "alegria"
            assert result.sentiments['alegria'] > 0.5
            assert result.confidence > 0.5
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_negative_sentiment_analysis(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-003: Análisis de sentimiento negativo"""
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            result = analyzer.analyze("Me siento muy triste")
            
            assert result.dominant_sentiment == "tristeza"
            assert result.sentiments['tristeza'] > 0.5
            assert result.confidence > 0.5
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_mixed_sentiment_analysis(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-004: Análisis de sentimientos mixtos"""
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            result = analyzer.analyze("Estoy feliz pero también preocupado")
            
            # Debería detectar múltiples sentimientos
            assert result.sentiments['alegria'] > 0.0
            assert result.sentiments['preocupacion'] > 0.0
            assert len(result.secondary_sentiments) > 0
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_neutral_sentiment_analysis(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-005: Análisis de sentimiento neutral"""
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            result = analyzer.analyze("El clima está bien")
            
            # Debería tener puntuaciones más balanceadas
            max_score = max(result.sentiments.values())
            min_score = min(result.sentiments.values())
            assert max_score - min_score < 0.5  # No muy polarizado
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_batch_analysis(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-006: Análisis en lote"""
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            texts = [
                "Estoy muy feliz",
                "Me siento triste",
                "Estoy enojado",
                "Estoy preocupado"
            ]
            
            results = analyzer.batch_analyze(texts)
            
            assert len(results) == 4
            assert results[0].dominant_sentiment == "alegria"
            assert results[1].dominant_sentiment == "tristeza"
            assert results[2].dominant_sentiment == "enojo"
            assert results[3].dominant_sentiment == "preocupacion"
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_error_handling_invalid_text(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-007: Manejo de errores con texto inválido"""
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            
            # Texto muy largo
            long_text = "palabra " * 100
            with pytest.raises(SentimentAnalysisError):
                analyzer.analyze(long_text)
            
            # Texto vacío
            with pytest.raises(SentimentAnalysisError):
                analyzer.analyze("")
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_fuzzy_logic_integration(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-008: Integración de lógica difusa"""
        # Habilitar lógica difusa
        sample_config.enable_fuzzy_logic = True
        
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            
            # Texto con intensificadores y negaciones
            result = analyzer.analyze("No estoy muy triste")
            
            # Debería aplicar lógica difusa
            assert len(result.modifiers_applied) > 0
            assert result.dominant_sentiment != "tristeza"  # Negación aplicada
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_cache_integration(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-009: Integración del cache"""
        # Habilitar cache
        sample_config.enable_memoization = True
        
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            
            # Primera búsqueda
            result1 = analyzer.analyze("Estoy feliz")
            
            # Segunda búsqueda (debería usar cache)
            result2 = analyzer.analyze("Estoy feliz")
            
            # Los resultados deberían ser iguales
            assert result1.sentiments == result2.sentiments
            assert result1.confidence == result2.confidence
            
            # Verificar información del sistema
            system_info = analyzer.get_system_info()
            assert system_info['cache_info']['enabled'] == True
            assert system_info['cache_info']['size'] > 0
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_system_info_integration(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-010: Información del sistema"""
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            
            info = analyzer.get_system_info()
            
            assert 'version' in info
            assert 'config' in info
            assert 'tree_info' in info
            assert 'cache_info' in info
            assert 'components' in info
            
            assert info['version'] == '1.0.0'
            assert info['config']['enable_fuzzy_logic'] == sample_config.enable_fuzzy_logic
            assert info['config']['enable_memoization'] == sample_config.enable_memoization
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_text_validation_integration(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-011: Validación de texto integrada"""
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            
            # Textos válidos
            assert analyzer.validate_text("Texto válido") == True
            assert analyzer.validate_text("¡Hola!") == True
            
            # Textos inválidos
            assert analyzer.validate_text("") == False
            assert analyzer.validate_text("   ") == False
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree
    
    def test_complex_modifier_integration(self, sample_config, sample_keywords_data, sample_tree_data):
        """TC-INT-012: Integración de modificadores complejos"""
        # Habilitar lógica difusa
        sample_config.enable_fuzzy_logic = True
        
        # Mock de carga de recursos
        def mock_load_keywords(self):
            return sample_keywords_data
        
        def mock_load_tree(self):
            return sample_tree_data
        
        original_load_keywords = SentimentAnalyzer._load_keywords_data
        original_load_tree = SentimentAnalyzer._load_tree_data
        
        SentimentAnalyzer._load_keywords_data = mock_load_keywords
        SentimentAnalyzer._load_tree_data = mock_load_tree
        
        try:
            analyzer = SentimentAnalyzer(sample_config)
            
            # Texto con múltiples modificadores
            result = analyzer.analyze("¡No estoy muy extremadamente feliz! 😊 ¿Crees?")
            
            # Verificar que se aplicaron modificadores
            assert len(result.modifiers_applied) > 0
            assert result.processing_time > 0.0
            assert result.confidence > 0.0
            
        finally:
            SentimentAnalyzer._load_keywords_data = original_load_keywords
            SentimentAnalyzer._load_tree_data = original_load_tree 