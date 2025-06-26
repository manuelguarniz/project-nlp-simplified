"""
Analizador Principal de Sentimientos
===================================

Módulo principal que orquesta el análisis de sentimientos,
integrando todos los componentes del sistema.
"""

import time
import json
import logging
from typing import Dict, Any
from .sentiment_result import SentimentResult, SystemConfig
from .exceptions import SentimentAnalysisError, ConfigurationError
from ..core.text_preprocessor import TextPreprocessor
from ..core.tree_searcher import TreeSearcher
from ..core.fuzzy_logic import FuzzyLogicProcessor
from ..utils.keyword_matcher import KeywordMatcher
from ..utils.normalizer import ScoreNormalizer


class SentimentAnalyzer:
    """Analizador principal de sentimientos"""
    
    def __init__(self, config: SystemConfig = None):
        self.config = config or SystemConfig()
        self._setup_logging()
        self._load_resources()
        self._initialize_components()
    
    def analyze(self, text: str) -> SentimentResult:
        """
        Analiza el sentimiento de un texto
        
        Args:
            text: Texto a analizar
            
        Returns:
            Resultado del análisis de sentimientos
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Iniciando análisis de texto: '{text[:50]}...'")
            
            # 1. Preprocesamiento
            preprocessed_data = self.preprocessor.preprocess(text)
            self.logger.debug(f"Datos preprocesados: {preprocessed_data}")
            
            # 2. Coincidencia de palabras clave
            matched_keywords = self.keyword_matcher.find_matches(preprocessed_data['words'])
            self.logger.debug(f"Palabras clave encontradas: {matched_keywords}")
            
            # 3. Búsqueda en árbol de decisión
            tree_results = self.tree_searcher.search(preprocessed_data)
            self.logger.debug(f"Resultados del árbol: {tree_results}")
            
            # 4. Aplicar lógica difusa si está habilitada
            if self.config.enable_fuzzy_logic:
                modifiers = {
                    'intensifiers': preprocessed_data.get('intensifiers', []),
                    'attenuators': preprocessed_data.get('attenuators', []),
                    'negations': preprocessed_data.get('negations', []),
                    'emoticons': preprocessed_data.get('emoticons', []),
                    'exclamation_count': preprocessed_data.get('exclamation_count', 0),
                    'question_count': preprocessed_data.get('question_count', 0)
                }
                
                adjusted_scores = self.fuzzy_processor.apply_fuzzy_rules(
                    tree_results['final_scores'], 
                    modifiers
                )
                self.logger.debug(f"Puntuaciones ajustadas por lógica difusa: {adjusted_scores}")
            else:
                adjusted_scores = tree_results['final_scores']
            
            # 5. Normalización de puntuaciones
            normalized_scores = self.normalizer.normalize_scores(adjusted_scores)
            self.logger.debug(f"Puntuaciones normalizadas: {normalized_scores}")
            
            # 6. Cálculo de confianza
            confidence = self.normalizer.calculate_confidence(normalized_scores, matched_keywords)
            
            # 7. Crear resultado
            processing_time = time.time() - start_time
            
            result = SentimentResult(
                text=text,
                sentiments=normalized_scores,
                confidence=confidence,
                processing_time=processing_time,
                matched_keywords=matched_keywords,
                tree_path=tree_results.get('path', []),
                modifiers_applied=modifiers if self.config.enable_fuzzy_logic else {},
                dominant_sentiment=self.normalizer.get_dominant_sentiment(normalized_scores),
                secondary_sentiments=self.normalizer.get_secondary_sentiments(normalized_scores),
                analysis_quality=self._determine_analysis_quality(confidence, processing_time)
            )
            
            self.logger.info(f"Análisis completado en {processing_time:.3f}s. "
                           f"Sentimiento dominante: {result.dominant_sentiment}, "
                           f"Confianza: {confidence:.3f}")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"Error en análisis: {str(e)}")
            raise SentimentAnalysisError(f"Error durante el análisis: {str(e)}")
    
    def _setup_logging(self):
        """Configura el sistema de logging"""
        log_config = self.config.logging
        
        # Configurar nivel de logging
        log_level = getattr(logging, log_config.get('level', 'INFO').upper())
        
        # Configurar formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Configurar logger principal
        self.logger = logging.getLogger('SentimentAnalyzer')
        self.logger.setLevel(log_level)
        
        # Evitar duplicación de handlers
        if not self.logger.handlers:
            # Handler para consola
            if log_config.get('enable_console_logging', True):
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)
            
            # Handler para archivo
            if log_config.get('enable_file_logging', True):
                file_handler = logging.FileHandler(
                    log_config.get('log_file', 'sentiment_analysis.log')
                )
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
    
    def _load_resources(self):
        """Carga los recursos necesarios"""
        try:
            # Cargar configuración del sistema
            self.system_config = self._load_system_config()
            
            # Cargar árbol de decisión
            self.tree_data = self._load_tree_data()
            
            # Cargar palabras clave
            self.keywords_data = self._load_keywords_data()
            
        except Exception as e:
            raise ConfigurationError(f"Error al cargar recursos: {str(e)}")
    
    def _initialize_components(self):
        """Inicializa todos los componentes del sistema"""
        try:
            # Inicializar preprocesador
            self.preprocessor = TextPreprocessor(self.config)
            
            # Inicializar buscador de árbol
            self.tree_searcher = TreeSearcher(self.tree_data, self.config)
            
            # Inicializar procesador de lógica difusa
            self.fuzzy_processor = FuzzyLogicProcessor(self.config)
            
            # Inicializar coincidencia de palabras clave
            self.keyword_matcher = KeywordMatcher(self.keywords_data)
            
            # Inicializar normalizador
            self.normalizer = ScoreNormalizer(self.config)
            
            self.logger.info("Todos los componentes inicializados correctamente")
            
        except Exception as e:
            raise ConfigurationError(f"Error al inicializar componentes: {str(e)}")
    
    def _load_system_config(self) -> Dict[str, Any]:
        """Carga la configuración del sistema"""
        try:
            with open('resources/system_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("Archivo de configuración no encontrado, usando configuración por defecto")
            return {}
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Error al parsear configuración: {str(e)}")
    
    def _load_tree_data(self) -> Dict[str, Any]:
        """Carga los datos del árbol de decisión"""
        try:
            with open('resources/decision_tree_structure.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ConfigurationError("Archivo de árbol de decisión no encontrado")
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Error al parsear árbol de decisión: {str(e)}")
    
    def _load_keywords_data(self) -> Dict[str, Any]:
        """Carga los datos de palabras clave"""
        try:
            with open('resources/sentiment_keywords.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ConfigurationError("Archivo de palabras clave no encontrado")
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Error al parsear palabras clave: {str(e)}")
    
    def _determine_analysis_quality(self, confidence: float, processing_time: float) -> str:
        """
        Determina la calidad del análisis basado en confianza y tiempo
        
        Args:
            confidence: Confianza del análisis
            processing_time: Tiempo de procesamiento
            
        Returns:
            Calidad del análisis ('high', 'medium', 'low')
        """
        # Factor de confianza
        confidence_factor = confidence
        
        # Factor de tiempo (menor tiempo = mejor calidad)
        time_factor = max(0.0, 1.0 - (processing_time / 1.0))  # Normalizar a 1 segundo
        
        # Calcular calidad combinada
        quality_score = (confidence_factor * 0.7) + (time_factor * 0.3)
        
        if quality_score >= 0.8:
            return 'high'
        elif quality_score >= 0.6:
            return 'medium'
        else:
            return 'low'
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Obtiene información del sistema
        
        Returns:
            Dict con información del sistema
        """
        tree_info = self.tree_searcher.get_tree_info()
        
        return {
            'version': '1.0.0',
            'config': {
                'max_text_length': self.config.max_text_length,
                'enable_fuzzy_logic': self.config.enable_fuzzy_logic,
                'enable_memoization': self.config.enable_memoization
            },
            'tree_info': tree_info,
            'cache_info': {
                'enabled': self.config.enable_memoization,
                'size': tree_info.get('cache_size', 0)
            },
            'components': {
                'text_preprocessor': 'initialized',
                'tree_searcher': 'initialized',
                'fuzzy_logic_processor': 'initialized',
                'keyword_matcher': 'initialized',
                'score_normalizer': 'initialized'
            }
        }
    
    def clear_cache(self):
        """Limpia el cache del sistema"""
        if hasattr(self, 'tree_searcher') and self.tree_searcher.memoization_cache:
            self.tree_searcher.memoization_cache.clear()
            self.logger.info("Cache limpiado")
    
    def validate_text(self, text: str) -> bool:
        """
        Valida si un texto puede ser analizado
        
        Args:
            text: Texto a validar
            
        Returns:
            True si el texto es válido
        """
        return self.preprocessor.validate_input(text)
    
    def batch_analyze(self, texts: list) -> list:
        """
        Analiza múltiples textos en lote
        
        Args:
            texts: Lista de textos a analizar
            
        Returns:
            Lista de resultados de análisis
        """
        results = []
        
        for i, text in enumerate(texts):
            try:
                result = self.analyze(text)
                results.append(result)
                self.logger.info(f"Procesado texto {i+1}/{len(texts)}")
            except Exception as e:
                self.logger.error(f"Error al procesar texto {i+1}: {str(e)}")
                # Crear resultado de error
                error_result = SentimentResult(
                    text=text,
                    sentiments={},
                    confidence=0.0,
                    processing_time=0.0,
                    matched_keywords={},
                    tree_path=[],
                    modifiers_applied={},
                    dominant_sentiment=None,
                    secondary_sentiments=[],
                    analysis_quality='low'
                )
                results.append(error_result)
        
        return results 