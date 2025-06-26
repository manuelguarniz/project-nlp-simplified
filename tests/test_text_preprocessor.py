"""
Pruebas Unitarias para TextPreprocessor
======================================

Pruebas para el módulo de preprocesamiento de texto.
"""

import pytest
from src.core.text_preprocessor import TextPreprocessor
from src.models.exceptions import InvalidInputError


class TestTextPreprocessor:
    """Pruebas para TextPreprocessor"""
    
    def test_basic_preprocessing(self, text_preprocessor):
        """TC-PREP-001: Texto positivo con intensificador"""
        result = text_preprocessor.preprocess("¡Estoy muy feliz hoy!")
        
        assert result['cleaned_text'] == 'estoy muy feliz hoy'
        assert result['words'] == ['estoy', 'muy', 'feliz', 'hoy']
        assert result['word_count'] == 4
        assert result['has_negation'] == False
        assert result['intensifiers'] == ['muy']
        assert result['exclamation_count'] == 1
    
    def test_negation_preprocessing(self, text_preprocessor):
        """TC-PREP-002: Texto con negación"""
        result = text_preprocessor.preprocess("No estoy triste")
        
        assert result['cleaned_text'] == 'no estoy triste'
        assert result['words'] == ['no', 'estoy', 'triste']
        assert result['word_count'] == 3
        assert result['has_negation'] == True
        assert result['intensifiers'] == []
        assert result['negations'] == ['no']
    
    def test_question_preprocessing(self, text_preprocessor):
        """TC-PREP-003: Pregunta informativa"""
        result = text_preprocessor.preprocess("¿Qué hora es?")
        
        assert result['cleaned_text'] == 'que hora es'
        assert result['words'] == ['que', 'hora', 'es']
        assert result['word_count'] == 3
        assert result['has_negation'] == False
        assert result['question_count'] == 1
        assert result['exclamation_count'] == 0
    
    def test_empty_text(self, text_preprocessor):
        """TC-PREP-004: Texto vacío"""
        with pytest.raises(InvalidInputError, match="El texto no cumple con los requisitos de validación"):
            text_preprocessor.preprocess("")
    
    def test_whitespace_only(self, text_preprocessor):
        """TC-PREP-005: Solo espacios en blanco"""
        with pytest.raises(InvalidInputError, match="El texto no cumple con los requisitos de validación"):
            text_preprocessor.preprocess("   ")
    
    def test_text_too_long(self, text_preprocessor):
        """TC-PREP-006: Texto muy largo (>50 palabras)"""
        long_text = "palabra " * 51
        with pytest.raises(InvalidInputError, match="El texto no cumple con los requisitos de validación"):
            text_preprocessor.preprocess(long_text)
    
    def test_multiple_exclamations(self, text_preprocessor):
        """TC-PREP-007: Texto con múltiples exclamaciones y mayúsculas"""
        result = text_preprocessor.preprocess("¡¡¡MUY FELIZ!!!")
        
        assert result['cleaned_text'] == 'muy feliz'
        assert result['words'] == ['muy', 'feliz']
        assert result['word_count'] == 2
        assert result['has_negation'] == False
        assert result['intensifiers'] == ['muy']
        assert result['exclamation_count'] == 3
        assert result['uppercase_words'] == ['MUY', 'FELIZ']
    
    def test_emoticons(self, text_preprocessor):
        """TC-PREP-008: Texto con emoticones"""
        result = text_preprocessor.preprocess("😊 Estoy contento 😊")
        
        assert result['cleaned_text'] == 'estoy contento'
        assert result['words'] == ['estoy', 'contento']
        assert result['word_count'] == 2
        assert result['has_negation'] == False
        assert result['emoticons'] == ['😊', '😊']
    
    def test_none_input(self, text_preprocessor):
        """TC-ERR-001: Entrada nula"""
        with pytest.raises(InvalidInputError):
            text_preprocessor.preprocess(None)
    
    def test_invalid_characters(self, text_preprocessor):
        """TC-ERR-004: Caracteres inválidos"""
        with pytest.raises(InvalidInputError):
            text_preprocessor.preprocess("Texto con caracteres inválidos \x00")
    
    def test_validate_input_valid(self, text_preprocessor):
        """Prueba validación de entrada válida"""
        assert text_preprocessor.validate_input("Texto válido") == True
        assert text_preprocessor.validate_input("Palabra") == True
        assert text_preprocessor.validate_input("¡Hola!") == True
    
    def test_validate_input_invalid(self, text_preprocessor):
        """Prueba validación de entrada inválida"""
        assert text_preprocessor.validate_input("") == False
        assert text_preprocessor.validate_input("   ") == False
        assert text_preprocessor.validate_input(None) == False
    
    def test_extract_modifiers(self, text_preprocessor):
        """Prueba extracción de modificadores"""
        words = ['estoy', 'muy', 'feliz', 'pero', 'no', 'triste']
        modifiers = text_preprocessor.extract_modifiers(words)
        
        assert 'muy' in modifiers['intensifiers']
        assert 'no' in modifiers['negations']
        assert len(modifiers['attenuators']) == 0
    
    def test_multiple_intensifiers(self, text_preprocessor):
        """Prueba múltiples intensificadores"""
        result = text_preprocessor.preprocess("Estoy muy extremadamente feliz")
        
        assert len(result['intensifiers']) == 2
        assert 'muy' in result['intensifiers']
        assert 'extremadamente' in result['intensifiers']
    
    def test_multiple_negations(self, text_preprocessor):
        """Prueba múltiples negaciones"""
        result = text_preprocessor.preprocess("No nunca estoy triste")
        
        assert result['has_negation'] == True
        assert len(result['negations']) == 2
        assert 'no' in result['negations']
        assert 'nunca' in result['negations']
    
    def test_attenuators(self, text_preprocessor):
        """Prueba atenuadores"""
        result = text_preprocessor.preprocess("Estoy un poco triste")
        
        assert len(result['attenuators']) == 2
        assert 'un' in result['attenuators']
        assert 'poco' in result['attenuators']
    
    def test_punctuation_counting(self, text_preprocessor):
        """Prueba conteo de puntuación"""
        result = text_preprocessor.preprocess("¡Hola! ¿Cómo estás?")
        
        assert result['punctuation_count'] > 0
        assert result['exclamation_count'] == 1
        assert result['question_count'] == 1
    
    def test_uppercase_detection(self, text_preprocessor):
        """Prueba detección de mayúsculas"""
        result = text_preprocessor.preprocess("Estoy MUY FELIZ")
        
        assert len(result['uppercase_words']) == 2
        assert 'MUY' in result['uppercase_words']
        assert 'FELIZ' in result['uppercase_words']
    
    def test_emoticon_detection(self, text_preprocessor):
        """Prueba detección de emoticones"""
        result = text_preprocessor.preprocess("😊 😄 😃")
        
        assert len(result['emoticons']) == 3
        assert '😊' in result['emoticons']
        assert '😄' in result['emoticons']
        assert '😃' in result['emoticons']
    
    def test_mixed_content(self, text_preprocessor):
        """Prueba contenido mixto"""
        result = text_preprocessor.preprocess("¡Estoy MUY feliz! 😊 ¿No crees?")
        
        assert result['exclamation_count'] == 1
        assert result['question_count'] == 1
        assert len(result['uppercase_words']) > 0
        assert len(result['emoticons']) > 0
        assert result['has_negation'] == True
    
    def test_word_length_filtering(self, text_preprocessor):
        """Prueba filtrado por longitud de palabras"""
        # Crear configuración con límite de longitud de palabra
        config = text_preprocessor.config
        config.preprocessing['max_word_length'] = 5
        
        result = text_preprocessor.preprocess("Esta es una palabra muy larga")
        
        # Las palabras muy largas deberían ser filtradas
        assert 'muy' in result['words']  # Palabra corta
        assert 'larga' not in result['words']  # Palabra larga filtrada
    
    def test_case_sensitivity_config(self, text_preprocessor):
        """Prueba configuración de sensibilidad a mayúsculas"""
        # Crear configuración sin conversión a minúsculas
        config = text_preprocessor.config
        config.preprocessing['convert_to_lowercase'] = False
        
        result = text_preprocessor.preprocess("Estoy MUY Feliz")
        
        # El texto debería mantener las mayúsculas
        assert 'MUY' in result['words']
        assert 'Feliz' in result['words']
    
    def test_punctuation_removal_config(self, text_preprocessor):
        """Prueba configuración de remoción de puntuación"""
        # Crear configuración sin remoción de puntuación
        config = text_preprocessor.config
        config.preprocessing['remove_punctuation'] = False
        
        result = text_preprocessor.preprocess("¡Hola! ¿Cómo estás?")
        
        # La puntuación debería mantenerse en las palabras
        assert '¡Hola!' in result['words']
        assert '¿Cómo' in result['words']
        assert 'estás?' in result['words'] 