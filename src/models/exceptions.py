"""
Excepciones Personalizadas del Sistema
=====================================
"""


class SentimentAnalysisError(Exception):
    """Excepción base para errores de análisis de sentimientos"""
    pass


class InvalidInputError(SentimentAnalysisError):
    """Error de entrada inválida"""
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message)


class TreeSearchError(SentimentAnalysisError):
    """Error en búsqueda del árbol"""
    def __init__(self, message: str, node_id: str = None):
        self.node_id = node_id
        super().__init__(message)


class ConfigurationError(SentimentAnalysisError):
    """Error de configuración"""
    pass


class ProcessingError(SentimentAnalysisError):
    """Error durante el procesamiento"""
    pass


class KeywordMatchError(SentimentAnalysisError):
    """Error en coincidencia de palabras clave"""
    pass


class FuzzyLogicError(SentimentAnalysisError):
    """Error en lógica difusa"""
    pass


class NormalizationError(SentimentAnalysisError):
    """Error en normalización de puntuaciones"""
    pass


# Códigos de error
ERROR_CODES = {
    'INVALID_INPUT': 'E001',
    'TEXT_TOO_LONG': 'E002',
    'EMPTY_TEXT': 'E003',
    'INVALID_CHARACTERS': 'E004',
    'TREE_NOT_FOUND': 'E005',
    'INVALID_TREE_STRUCTURE': 'E006',
    'NODE_NOT_FOUND': 'E007',
    'INVALID_CONDITION': 'E008',
    'KEYWORDS_NOT_FOUND': 'E009',
    'INVALID_KEYWORDS_FORMAT': 'E010',
    'CONFIGURATION_ERROR': 'E011',
    'PROCESSING_TIMEOUT': 'E012',
    'MEMORY_ERROR': 'E013'
} 