"""
Preprocesador de Texto
=====================

Módulo responsable del preprocesamiento de texto de entrada,
incluyendo limpieza, extracción de modificadores y validaciones.
"""

import re
import unicodedata
from typing import Dict, List, Any
from ..models.sentiment_result import SystemConfig
from ..models.exceptions import InvalidInputError


class TextPreprocessor:
    """Preprocesador de texto"""
    
    def __init__(self, config: SystemConfig):
        self.config = config
        self._setup_modifiers()
    
    def _setup_modifiers(self):
        """Configura las listas de modificadores"""
        # Intensificadores
        self.intensifiers = {
            'muy', 'extremadamente', 'increíblemente', 'sumamente', 
            'completamente', 'totalmente', 'absolutamente', 'realmente',
            'verdaderamente', 'genuinamente', 'profundamente'
        }
        
        # Atenuadores
        self.attenuators = {
            'un', 'poco', 'ligeramente', 'levemente', 'moderadamente',
            'relativamente', 'bastante', 'algo', 'medianamente'
        }
        
        # Negaciones
        self.negations = {
            'no', 'nunca', 'jamás', 'tampoco', 'ni', 'nada', 'ningún',
            'ninguna', 'ninguno', 'ningunos', 'ningunas'
        }
        
        # Emoticones básicos
        self.emoticons = {
            '😊', '😄', '😃', '😀', '😁', '😆', '😅', '😂', '🤣', '😉', '😋', '😎',
            '😍', '🥰', '😘', '😗', '😙', '😚', '🙂', '🤗', '🤔', '🤨', '😐', '😑',
            '😶', '🙄', '😏', '😣', '😥', '😮', '🤐', '😯', '😪', '😫', '😴', '😌',
            '😛', '😜', '😝', '🤤', '😒', '😓', '😔', '😕', '🙃', '🤑', '😲', '😷',
            '🤒', '🤕', '🤢', '🤮', '🤧', '😈', '👿', '👹', '👺', '💀', '👻', '👽',
            '🤖', '💩', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾'
        }
    
    def preprocess(self, text: str) -> Dict[str, Any]:
        """
        Preprocesa el texto de entrada
        
        Args:
            text: Texto a preprocesar
            
        Returns:
            Dict con datos preprocesados
            
        Raises:
            InvalidInputError: Si el texto no es válido
        """
        # Validar entrada
        if not self.validate_input(text):
            raise InvalidInputError("El texto no cumple con los requisitos de validación")
        
        # Limpiar texto
        cleaned_text = self._clean_text(text)
        
        # Tokenizar
        words = self._tokenize(cleaned_text)
        
        # Extraer modificadores
        modifiers = self.extract_modifiers(words)
        
        # Contar elementos
        punctuation_count = self._count_punctuation(text)
        exclamation_count = self._count_exclamations(text)
        question_count = self._count_questions(text)
        
        # Detectar palabras en mayúsculas
        uppercase_words = self._detect_uppercase_words(text)
        
        # Detectar emoticones
        emoticons = self._detect_emoticons(text)
        
        return {
            'cleaned_text': cleaned_text,
            'words': words,
            'word_count': len(words),
            'has_negation': len(modifiers['negations']) > 0,
            'intensifiers': modifiers['intensifiers'],
            'attenuators': modifiers['attenuators'],
            'punctuation_count': punctuation_count,
            'exclamation_count': exclamation_count,
            'question_count': question_count,
            'uppercase_words': uppercase_words,
            'emoticons': emoticons,
            'processing_errors': []
        }
    
    def validate_input(self, text: str) -> bool:
        """
        Valida que el texto cumpla con los requisitos
        
        Args:
            text: Texto a validar
            
        Returns:
            True si el texto es válido, False en caso contrario
        """
        # Verificar que no sea None
        if text is None:
            return False
        
        # Verificar que no esté vacío después de limpiar espacios
        if not text.strip():
            return False
        
        # Verificar longitud (número de palabras)
        words = text.split()
        if len(words) > self.config.max_text_length:
            return False
        
        # Verificar caracteres válidos (UTF-8)
        try:
            text.encode('utf-8')
        except UnicodeEncodeError:
            return False
        
        # Verificar que no contenga caracteres de control
        for char in text:
            if unicodedata.category(char).startswith('C'):
                return False
        
        return True
    
    def extract_modifiers(self, words: List[str]) -> Dict[str, List[str]]:
        """
        Extrae modificadores del texto
        
        Args:
            words: Lista de palabras del texto
            
        Returns:
            Dict con modificadores encontrados
        """
        found_intensifiers = []
        found_attenuators = []
        found_negations = []
        
        for word in words:
            word_lower = word.lower()
            
            if word_lower in self.intensifiers:
                found_intensifiers.append(word)
            elif word_lower in self.attenuators:
                found_attenuators.append(word)
            elif word_lower in self.negations:
                found_negations.append(word)
        
        return {
            'intensifiers': found_intensifiers,
            'attenuators': found_attenuators,
            'negations': found_negations
        }
    
    def _clean_text(self, text: str) -> str:
        """Limpia el texto de entrada"""
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Convertir a minúsculas si está configurado
        if self.config.preprocessing.get('convert_to_lowercase', True):
            text = text.lower()
        
        # Remover puntuación si está configurado
        if self.config.preprocessing.get('remove_punctuation', True):
            text = re.sub(r'[^\w\s]', '', text)
        
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokeniza el texto en palabras"""
        words = text.split()
        
        # Filtrar palabras muy largas
        max_length = self.config.preprocessing.get('max_word_length', 20)
        words = [word for word in words if len(word) <= max_length]
        
        return words
    
    def _count_punctuation(self, text: str) -> int:
        """Cuenta los signos de puntuación"""
        return len(re.findall(r'[^\w\s]', text))
    
    def _count_exclamations(self, text: str) -> int:
        """Cuenta las exclamaciones"""
        return len(re.findall(r'!+', text))
    
    def _count_questions(self, text: str) -> int:
        """Cuenta las interrogaciones"""
        return len(re.findall(r'\?+', text))
    
    def _detect_uppercase_words(self, text: str) -> List[str]:
        """Detecta palabras en mayúsculas"""
        words = text.split()
        uppercase_words = []
        
        for word in words:
            if word.isupper() and len(word) > 1:
                uppercase_words.append(word)
        
        return uppercase_words
    
    def _detect_emoticons(self, text: str) -> List[str]:
        """Detecta emoticones en el texto"""
        found_emoticons = []
        
        for emoticon in self.emoticons:
            if emoticon in text:
                count = text.count(emoticon)
                found_emoticons.extend([emoticon] * count)
        
        return found_emoticons 