"""
Pruebas Unitarias para FuzzyLogicProcessor
=========================================

Pruebas para el módulo de lógica difusa.
"""

import pytest
from src.core.fuzzy_logic import FuzzyLogicProcessor


class TestFuzzyLogicProcessor:
    """Pruebas para FuzzyLogicProcessor"""
    
    def test_basic_intensification(self, fuzzy_logic_processor):
        """TC-FUZZY-001: Intensificación simple"""
        base_scores = {'alegria': 0.6, 'tristeza': 0.2}
        modifiers = {
            'intensifiers': ['muy'],
            'negations': [],
            'attenuators': []
        }
        
        adjusted = fuzzy_logic_processor.apply_fuzzy_rules(base_scores, modifiers)
        
        assert adjusted['alegria'] > 0.6  # Debería estar intensificado
        assert adjusted['tristeza'] == 0.2  # Sin cambios
        assert adjusted['alegria'] <= 1.0  # No debería exceder 1.0
    
    def test_basic_negation(self, fuzzy_logic_processor):
        """TC-FUZZY-002: Negación simple"""
        base_scores = {'alegria': 0.6, 'tristeza': 0.2}
        modifiers = {
            'intensifiers': [],
            'negations': ['no'],
            'attenuators': []
        }
        
        adjusted = fuzzy_logic_processor.apply_fuzzy_rules(base_scores, modifiers)
        
        assert adjusted['alegria'] == 0.4  # 1.0 - 0.6
        assert adjusted['tristeza'] == 0.8  # 1.0 - 0.2
    
    def test_basic_attenuation(self, fuzzy_logic_processor):
        """TC-FUZZY-003: Atenuación"""
        base_scores = {'alegria': 0.6, 'tristeza': 0.2}
        modifiers = {
            'intensifiers': [],
            'negations': [],
            'attenuators': ['un', 'poco']
        }
        
        adjusted = fuzzy_logic_processor.apply_fuzzy_rules(base_scores, modifiers)
        
        assert adjusted['alegria'] < 0.6  # Debería estar atenuado
        assert adjusted['tristeza'] < 0.2  # Debería estar atenuado
        assert adjusted['alegria'] > 0.0  # No debería ser cero
    
    def test_multiple_intensifiers_with_negation(self, fuzzy_logic_processor):
        """TC-FUZZY-004: Múltiples intensificadores + negación"""
        base_scores = {'alegria': 0.6, 'tristeza': 0.2}
        modifiers = {
            'intensifiers': ['muy', 'extremadamente'],
            'negations': ['no'],
            'attenuators': []
        }
        
        adjusted = fuzzy_logic_processor.apply_fuzzy_rules(base_scores, modifiers)
        
        # Primero se intensifica, luego se niega
        assert adjusted['alegria'] < 0.4  # Negación de intensificación
        assert adjusted['tristeza'] > 0.8  # Negación de atenuación
    
    def test_double_negation(self, fuzzy_logic_processor):
        """TC-FUZZY-005: Doble negación (cancelan)"""
        base_scores = {'alegria': 0.6, 'tristeza': 0.2}
        modifiers = {
            'intensifiers': [],
            'negations': ['no', 'no'],
            'attenuators': []
        }
        
        adjusted = fuzzy_logic_processor.apply_fuzzy_rules(base_scores, modifiers)
        
        # Doble negación debería cancelarse
        assert adjusted['alegria'] == 0.6
        assert adjusted['tristeza'] == 0.2
    
    def test_intensification_at_maximum(self, fuzzy_logic_processor):
        """TC-FUZZY-006: Intensificación en máximo"""
        base_scores = {'alegria': 1.0, 'tristeza': 0.0}
        modifiers = {
            'intensifiers': ['muy'],
            'negations': [],
            'attenuators': []
        }
        
        adjusted = fuzzy_logic_processor.apply_fuzzy_rules(base_scores, modifiers)
        
        # No debería exceder 1.0
        assert adjusted['alegria'] == 1.0
        assert adjusted['tristeza'] == 0.0
    
    def test_intensify_sentiment(self, fuzzy_logic_processor):
        """Prueba función intensify_sentiment"""
        score = 0.5
        intensifiers = ['muy', 'extremadamente']
        
        intensified = fuzzy_logic_processor.intensify_sentiment(score, intensifiers)
        
        assert intensified > score
        assert intensified <= 1.0
    
    def test_intensify_sentiment_zero_score(self, fuzzy_logic_processor):
        """Prueba intensificación con puntuación cero"""
        score = 0.0
        intensifiers = ['muy']
        
        intensified = fuzzy_logic_processor.intensify_sentiment(score, intensifiers)
        
        assert intensified == 0.0  # No debería cambiar
    
    def test_intensify_sentiment_no_intensifiers(self, fuzzy_logic_processor):
        """Prueba intensificación sin intensificadores"""
        score = 0.5
        intensifiers = []
        
        intensified = fuzzy_logic_processor.intensify_sentiment(score, intensifiers)
        
        assert intensified == score  # No debería cambiar
    
    def test_attenuate_sentiment(self, fuzzy_logic_processor):
        """Prueba función attenuate_sentiment"""
        score = 0.8
        attenuators = ['un', 'poco']
        
        attenuated = fuzzy_logic_processor.attenuate_sentiment(score, attenuators)
        
        assert attenuated < score
        assert attenuated > 0.0
    
    def test_attenuate_sentiment_zero_score(self, fuzzy_logic_processor):
        """Prueba atenuación con puntuación cero"""
        score = 0.0
        attenuators = ['poco']
        
        attenuated = fuzzy_logic_processor.attenuate_sentiment(score, attenuators)
        
        assert attenuated == 0.0  # No debería cambiar
    
    def test_apply_negation_odd_count(self, fuzzy_logic_processor):
        """Prueba negación con número impar de negaciones"""
        scores = {'alegria': 0.7, 'tristeza': 0.3}
        negations = ['no', 'nunca', 'jamás']  # 3 negaciones (impar)
        
        negated = fuzzy_logic_processor.apply_negation(scores, negations)
        
        assert negated['alegria'] == 0.3  # 1.0 - 0.7
        assert negated['tristeza'] == 0.7  # 1.0 - 0.3
    
    def test_apply_negation_even_count(self, fuzzy_logic_processor):
        """Prueba negación con número par de negaciones"""
        scores = {'alegria': 0.7, 'tristeza': 0.3}
        negations = ['no', 'nunca']  # 2 negaciones (par)
        
        negated = fuzzy_logic_processor.apply_negation(scores, negations)
        
        # Debería mantener las puntuaciones originales
        assert negated['alegria'] == 0.7
        assert negated['tristeza'] == 0.3
    
    def test_apply_negation_no_negations(self, fuzzy_logic_processor):
        """Prueba negación sin negaciones"""
        scores = {'alegria': 0.7, 'tristeza': 0.3}
        negations = []
        
        negated = fuzzy_logic_processor.apply_negation(scores, negations)
        
        # Debería mantener las puntuaciones originales
        assert negated['alegria'] == 0.7
        assert negated['tristeza'] == 0.3
    
    def test_combine_emotions_single_high(self, fuzzy_logic_processor):
        """Prueba combinación con un solo sentimiento alto"""
        scores = {'alegria': 0.8, 'tristeza': 0.3, 'enojo': 0.2}
        
        combined = fuzzy_logic_processor.combine_emotions(scores)
        
        # Debería mantener las puntuaciones originales
        assert combined['alegria'] == 0.8
        assert combined['tristeza'] == 0.3
        assert combined['enojo'] == 0.2
    
    def test_combine_emotions_multiple_high(self, fuzzy_logic_processor):
        """Prueba combinación con múltiples sentimientos altos"""
        scores = {'alegria': 0.8, 'tristeza': 0.7, 'enojo': 0.2}
        
        combined = fuzzy_logic_processor.combine_emotions(scores)
        
        # El segundo sentimiento alto debería estar reducido
        assert combined['alegria'] == 0.8  # El más alto se mantiene
        assert combined['tristeza'] < 0.7  # Debería estar reducido
        assert combined['enojo'] == 0.2  # Sin cambios
    
    def test_combine_emotions_empty(self, fuzzy_logic_processor):
        """Prueba combinación con puntuaciones vacías"""
        scores = {}
        
        combined = fuzzy_logic_processor.combine_emotions(scores)
        
        assert combined == {}
    
    def test_fuzzy_operators(self, fuzzy_logic_processor):
        """Prueba operadores difusos básicos"""
        a, b = 0.7, 0.3
        
        # Operador AND (mínimo)
        and_result = fuzzy_logic_processor.fuzzy_and(a, b)
        assert and_result == 0.3
        
        # Operador OR (máximo)
        or_result = fuzzy_logic_processor.fuzzy_or(a, b)
        assert or_result == 0.7
        
        # Operador NOT (complemento)
        not_result = fuzzy_logic_processor.fuzzy_not(a)
        assert not_result == 0.3
    
    def test_fuzzy_implication(self, fuzzy_logic_processor):
        """Prueba implicación difusa"""
        antecedent, consequent = 0.8, 0.6
        
        implication = fuzzy_logic_processor.fuzzy_implication(antecedent, consequent)
        
        # max(1 - antecedent, consequent) = max(0.2, 0.6) = 0.6
        assert implication == 0.6
    
    def test_calculate_membership(self, fuzzy_logic_processor):
        """Prueba cálculo de grado de pertenencia"""
        value, low, high = 0.5, 0.0, 1.0
        
        membership = fuzzy_logic_processor.calculate_membership(value, low, high)
        
        assert membership == 0.5
    
    def test_calculate_membership_below_range(self, fuzzy_logic_processor):
        """Prueba pertenencia por debajo del rango"""
        value, low, high = -0.5, 0.0, 1.0
        
        membership = fuzzy_logic_processor.calculate_membership(value, low, high)
        
        assert membership == 0.0
    
    def test_calculate_membership_above_range(self, fuzzy_logic_processor):
        """Prueba pertenencia por encima del rango"""
        value, low, high = 1.5, 0.0, 1.0
        
        membership = fuzzy_logic_processor.calculate_membership(value, low, high)
        
        assert membership == 1.0
    
    def test_defuzzify_centroid(self, fuzzy_logic_processor):
        """Prueba defuzzificación por centroide"""
        membership_values = {'bajo': 0.3, 'medio': 0.7, 'alto': 0.5}
        
        centroid = fuzzy_logic_processor.defuzzify_centroid(membership_values)
        
        assert centroid > 0.0
        assert centroid <= 1.0
    
    def test_defuzzify_centroid_empty(self, fuzzy_logic_processor):
        """Prueba defuzzificación con valores vacíos"""
        membership_values = {}
        
        centroid = fuzzy_logic_processor.defuzzify_centroid(membership_values)
        
        assert centroid == 0.0
    
    def test_validate_modifiers_valid(self, fuzzy_logic_processor):
        """Prueba validación de modificadores válidos"""
        modifiers = {
            'intensifiers': ['muy'],
            'negations': ['no'],
            'attenuators': ['poco'],
            'emoticons': ['😊'],
            'exclamation_count': 1,
            'question_count': 0
        }
        
        assert fuzzy_logic_processor.validate_modifiers(modifiers) == True
    
    def test_validate_modifiers_invalid_type(self, fuzzy_logic_processor):
        """Prueba validación con tipo inválido"""
        modifiers = "invalid"
        
        assert fuzzy_logic_processor.validate_modifiers(modifiers) == False
    
    def test_validate_modifiers_invalid_key(self, fuzzy_logic_processor):
        """Prueba validación con clave inválida"""
        modifiers = {
            'intensifiers': ['muy'],
            'invalid_key': ['value']
        }
        
        assert fuzzy_logic_processor.validate_modifiers(modifiers) == False
    
    def test_validate_modifiers_invalid_count_type(self, fuzzy_logic_processor):
        """Prueba validación con tipo inválido para conteos"""
        modifiers = {
            'intensifiers': ['muy'],
            'exclamation_count': 'invalid'
        }
        
        assert fuzzy_logic_processor.validate_modifiers(modifiers) == False
    
    def test_context_rules_emoticons(self, fuzzy_logic_processor):
        """Prueba reglas de contexto con emoticones"""
        scores = {'alegria': 0.5, 'tristeza': 0.3}
        modifiers = {
            'emoticons': ['😊', '😄'],
            'exclamation_count': 0,
            'question_count': 0
        }
        
        adjusted = fuzzy_logic_processor._apply_context_rules(scores, modifiers)
        
        assert adjusted['alegria'] > 0.5  # Debería aumentar por emoticones
    
    def test_context_rules_exclamations(self, fuzzy_logic_processor):
        """Prueba reglas de contexto con exclamaciones"""
        scores = {'alegria': 0.6, 'tristeza': 0.4}
        modifiers = {
            'emoticons': [],
            'exclamation_count': 2,
            'question_count': 0
        }
        
        adjusted = fuzzy_logic_processor._apply_context_rules(scores, modifiers)
        
        # El sentimiento dominante (alegría) debería aumentar
        assert adjusted['alegria'] > 0.6
    
    def test_context_rules_questions(self, fuzzy_logic_processor):
        """Prueba reglas de contexto con preguntas"""
        scores = {'alegria': 0.3, 'sorpresa': 0.2, 'informacion': 0.1}
        modifiers = {
            'emoticons': [],
            'exclamation_count': 0,
            'question_count': 1
        }
        
        adjusted = fuzzy_logic_processor._apply_context_rules(scores, modifiers)
        
        assert adjusted['sorpresa'] > 0.2  # Debería aumentar
        assert adjusted['informacion'] > 0.1  # Debería aumentar
    
    def test_complex_modifier_combination(self, fuzzy_logic_processor):
        """Prueba combinación compleja de modificadores"""
        base_scores = {'alegria': 0.6, 'tristeza': 0.3}
        modifiers = {
            'intensifiers': ['muy'],
            'negations': ['no'],
            'attenuators': ['poco'],
            'emoticons': ['😊'],
            'exclamation_count': 1,
            'question_count': 0
        }
        
        adjusted = fuzzy_logic_processor.apply_fuzzy_rules(base_scores, modifiers)
        
        # Debería aplicar todos los modificadores
        assert 0.0 <= adjusted['alegria'] <= 1.0
        assert 0.0 <= adjusted['tristeza'] <= 1.0
    
    def test_configuration_parameters(self, fuzzy_logic_processor):
        """Prueba parámetros de configuración"""
        # Cambiar parámetros de configuración
        fuzzy_logic_processor.config.fuzzy_parameters['intensification_factor'] = 2.0
        fuzzy_logic_processor.config.fuzzy_parameters['attenuation_factor'] = 0.5
        
        score = 0.5
        intensifiers = ['muy']
        attenuators = ['poco']
        
        intensified = fuzzy_logic_processor.intensify_sentiment(score, intensifiers)
        attenuated = fuzzy_logic_processor.attenuate_sentiment(score, attenuators)
        
        # Debería usar los nuevos parámetros
        assert intensified > 0.5
        assert attenuated < 0.5 