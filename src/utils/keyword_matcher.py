"""
Coincidencia de Palabras Clave
==============================

Módulo responsable de encontrar coincidencias de palabras clave
por sentimiento en el texto preprocesado.
"""

import json
from typing import Dict, List
from ..models.exceptions import KeywordMatchError


class KeywordMatcher:
    """Coincidencia de palabras clave"""
    
    def __init__(self, keywords_data: Dict):
        self.keywords = self._load_keywords(keywords_data)
        self.sentiments = ['alegria', 'tristeza', 'enojo', 'preocupacion', 'informacion', 'sorpresa']
    
    def find_matches(self, words: List[str]) -> Dict[str, List[str]]:
        """
        Encuentra coincidencias de palabras clave por sentimiento
        
        Args:
            words: Lista de palabras del texto
            
        Returns:
            Dict con sentimientos como claves y listas de palabras encontradas
        """
        matches = {sentiment: [] for sentiment in self.sentiments}
        
        if not words:
            return matches
        
        # Normalizar palabras para búsqueda
        normalized_words = [word.lower().strip() for word in words]
        
        # Buscar coincidencias exactas
        for sentiment in self.sentiments:
            if sentiment in self.keywords:
                sentiment_keywords = self.keywords[sentiment]
                
                for word in normalized_words:
                    if word in sentiment_keywords.get('keywords', []):
                        matches[sentiment].append(word)
                    
                    # Buscar en sinónimos
                    for synonym_group in sentiment_keywords.get('synonyms', []):
                        if word in synonym_group:
                            matches[sentiment].append(word)
                            break
                    
                    # Buscar en conjugaciones verbales
                    for verb_form in sentiment_keywords.get('verb_forms', []):
                        if word in verb_form:
                            matches[sentiment].append(word)
                            break
        
        return matches
    
    def calculate_word_scores(self, matches: Dict[str, List[str]]) -> Dict[str, float]:
        """
        Calcula puntuaciones basadas en palabras encontradas
        
        Args:
            matches: Coincidencias de palabras por sentimiento
            
        Returns:
            Dict con puntuaciones por sentimiento
        """
        scores = {sentiment: 0.0 for sentiment in self.sentiments}
        total_matches = sum(len(words) for words in matches.values())
        
        if total_matches == 0:
            return scores
        
        # Calcular puntuaciones basadas en frecuencia
        for sentiment, words in matches.items():
            if words:
                # Puntuación base por número de palabras encontradas
                base_score = len(words) / total_matches
                
                # Ajustar por peso de las palabras clave
                weighted_score = self._calculate_weighted_score(sentiment, words)
                
                scores[sentiment] = min(1.0, base_score + weighted_score)
        
        return scores
    
    def _load_keywords(self, keywords_data: Dict) -> Dict[str, Dict[str, List[str]]]:
        """
        Carga las palabras clave desde el archivo JSON
        
        Args:
            keywords_data: Datos de palabras clave
            
        Returns:
            Dict con palabras clave organizadas por sentimiento
        """
        try:
            if isinstance(keywords_data, str):
                # Si es un string, asumir que es un archivo JSON
                with open(keywords_data, 'r', encoding='utf-8') as f:
                    return json.load(f)
            elif isinstance(keywords_data, dict):
                # Si ya es un diccionario, usarlo directamente
                return keywords_data
            else:
                raise KeywordMatchError("Formato de datos de palabras clave inválido")
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise KeywordMatchError(f"Error al cargar palabras clave: {str(e)}")
    
    def _calculate_weighted_score(self, sentiment: str, words: List[str]) -> float:
        """
        Calcula puntuación ponderada basada en el tipo de palabra clave
        
        Args:
            sentiment: Sentimiento
            words: Palabras encontradas
            
        Returns:
            Puntuación ponderada
        """
        if sentiment not in self.keywords:
            return 0.0
        
        sentiment_data = self.keywords[sentiment]
        weighted_score = 0.0
        
        for word in words:
            word_lower = word.lower()
            
            # Verificar si es palabra clave principal
            if word_lower in sentiment_data.get('keywords', []):
                weighted_score += 0.3
            
            # Verificar si es sinónimo
            for synonym_group in sentiment_data.get('synonyms', []):
                if word_lower in synonym_group:
                    weighted_score += 0.2
                    break
            
            # Verificar si es forma verbal
            for verb_form in sentiment_data.get('verb_forms', []):
                if word_lower in verb_form:
                    weighted_score += 0.25
                    break
        
        return min(0.5, weighted_score)  # Limitar a 0.5 para no dominar
    
    def get_keyword_info(self, word: str) -> Dict[str, any]:
        """
        Obtiene información sobre una palabra clave específica
        
        Args:
            word: Palabra a buscar
            
        Returns:
            Dict con información de la palabra clave
        """
        word_lower = word.lower()
        
        for sentiment in self.sentiments:
            if sentiment in self.keywords:
                sentiment_data = self.keywords[sentiment]
                
                # Buscar en palabras clave principales
                if word_lower in sentiment_data.get('keywords', []):
                    return {
                        'sentiment': sentiment,
                        'type': 'keyword',
                        'word': word,
                        'weight': 0.3
                    }
                
                # Buscar en sinónimos
                for synonym_group in sentiment_data.get('synonyms', []):
                    if word_lower in synonym_group:
                        return {
                            'sentiment': sentiment,
                            'type': 'synonym',
                            'word': word,
                            'weight': 0.2
                        }
                
                # Buscar en formas verbales
                for verb_form in sentiment_data.get('verb_forms', []):
                    if word_lower in verb_form:
                        return {
                            'sentiment': sentiment,
                            'type': 'verb_form',
                            'word': word,
                            'weight': 0.25
                        }
        
        return {
            'sentiment': None,
            'type': 'unknown',
            'word': word,
            'weight': 0.0
        }
    
    def get_sentiment_keywords(self, sentiment: str) -> List[str]:
        """
        Obtiene todas las palabras clave para un sentimiento específico
        
        Args:
            sentiment: Sentimiento del cual obtener palabras clave
            
        Returns:
            Lista de palabras clave
        """
        if sentiment not in self.keywords:
            return []
        
        sentiment_data = self.keywords[sentiment]
        all_keywords = []
        
        # Agregar palabras clave principales
        all_keywords.extend(sentiment_data.get('keywords', []))
        
        # Agregar sinónimos
        for synonym_group in sentiment_data.get('synonyms', []):
            all_keywords.extend(synonym_group)
        
        # Agregar formas verbales
        for verb_form in sentiment_data.get('verb_forms', []):
            all_keywords.extend(verb_form)
        
        return list(set(all_keywords))  # Remover duplicados 