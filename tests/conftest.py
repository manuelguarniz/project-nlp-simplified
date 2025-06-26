"""
Configuración de Pruebas
=======================

Configuración y fixtures comunes para todas las pruebas del sistema.
"""

import pytest
import json
import tempfile
import os
from src.models.sentiment_result import SystemConfig, SentimentResult
from src.core.text_preprocessor import TextPreprocessor
from src.utils.keyword_matcher import KeywordMatcher
from src.utils.normalizer import ScoreNormalizer
from src.core.fuzzy_logic import FuzzyLogicProcessor
from src.core.tree_searcher import TreeSearcher


@pytest.fixture
def sample_config():
    """Configuración de ejemplo para pruebas"""
    return SystemConfig(
        max_text_length=50,
        min_confidence=0.3,
        enable_fuzzy_logic=True,
        enable_memoization=True
    )


@pytest.fixture
def sample_keywords_data():
    """Datos de palabras clave de ejemplo"""
    return {
        "alegria": {
            "keywords": ["feliz", "contento", "alegre", "dichoso"],
            "synonyms": [["gozoso", "radiante", "eufórico"]],
            "verb_forms": [["alegrarse", "regocijarse", "celebrar"]]
        },
        "tristeza": {
            "keywords": ["triste", "melancólico", "deprimido", "abatido"],
            "synonyms": [["apenado", "desconsolado", "abatido"]],
            "verb_forms": [["entristecerse", "lamentarse", "llorar"]]
        },
        "enojo": {
            "keywords": ["enojado", "furioso", "irritado", "molesto"],
            "synonyms": [["airado", "colérico", "rabioso"]],
            "verb_forms": [["enojarse", "enfurecerse", "irritarse"]]
        },
        "preocupacion": {
            "keywords": ["preocupado", "inquieto", "nervioso", "ansioso"],
            "synonyms": [["inquieto", "agitado", "tenso"]],
            "verb_forms": [["preocuparse", "inquietarse", "nerviosearse"]]
        },
        "informacion": {
            "keywords": ["informar", "explicar", "describir", "detallar"],
            "synonyms": [["comunicar", "transmitir", "expresar"]],
            "verb_forms": [["informar", "explicar", "describir"]]
        },
        "sorpresa": {
            "keywords": ["sorprendido", "asombrado", "impresionado", "maravillado"],
            "synonyms": [["estupefacto", "pasmado", "deslumbrado"]],
            "verb_forms": [["sorprenderse", "asombrarse", "maravillarse"]]
        }
    }


@pytest.fixture
def sample_tree_data():
    """Datos de árbol de decisión de ejemplo"""
    return {
        "root": {
            "condition": "has_keyword('alegria', 'feliz')",
            "branches": {
                "true": "node_1",
                "false": "node_2"
            },
            "sentiment_scores": {
                "alegria": 0.5,
                "tristeza": 0.1,
                "enojo": 0.0,
                "preocupacion": 0.0,
                "informacion": 0.2,
                "sorpresa": 0.2
            },
            "keywords": [],
            "description": "Nodo raíz",
            "node_type": "root",
            "depth": 0
        },
        "node_1": {
            "condition": "has_intensifier()",
            "branches": {
                "true": "leaf_1",
                "false": "leaf_2"
            },
            "sentiment_scores": {
                "alegria": 0.8,
                "tristeza": 0.05,
                "enojo": 0.0,
                "preocupacion": 0.0,
                "informacion": 0.1,
                "sorpresa": 0.05
            },
            "keywords": ["feliz"],
            "description": "Nodo con intensificador",
            "node_type": "decision",
            "depth": 1
        },
        "node_2": {
            "condition": "has_keyword('tristeza', 'triste')",
            "branches": {
                "true": "leaf_3",
                "false": "leaf_4"
            },
            "sentiment_scores": {
                "alegria": 0.1,
                "tristeza": 0.7,
                "enojo": 0.1,
                "preocupacion": 0.0,
                "informacion": 0.1,
                "sorpresa": 0.0
            },
            "keywords": [],
            "description": "Nodo de tristeza",
            "node_type": "decision",
            "depth": 1
        },
        "leaf_1": {
            "condition": None,
            "branches": {},
            "sentiment_scores": {
                "alegria": 0.9,
                "tristeza": 0.02,
                "enojo": 0.0,
                "preocupacion": 0.0,
                "informacion": 0.05,
                "sorpresa": 0.03
            },
            "keywords": ["feliz", "muy"],
            "description": "Hoja de alegría intensificada",
            "node_type": "leaf",
            "depth": 2
        },
        "leaf_2": {
            "condition": None,
            "branches": {},
            "sentiment_scores": {
                "alegria": 0.75,
                "tristeza": 0.1,
                "enojo": 0.0,
                "preocupacion": 0.0,
                "informacion": 0.1,
                "sorpresa": 0.05
            },
            "keywords": ["feliz"],
            "description": "Hoja de alegría normal",
            "node_type": "leaf",
            "depth": 2
        },
        "leaf_3": {
            "condition": None,
            "branches": {},
            "sentiment_scores": {
                "alegria": 0.05,
                "tristeza": 0.8,
                "enojo": 0.05,
                "preocupacion": 0.05,
                "informacion": 0.05,
                "sorpresa": 0.0
            },
            "keywords": ["triste"],
            "description": "Hoja de tristeza",
            "node_type": "leaf",
            "depth": 2
        },
        "leaf_4": {
            "condition": None,
            "branches": {},
            "sentiment_scores": {
                "alegria": 0.3,
                "tristeza": 0.3,
                "enojo": 0.1,
                "preocupacion": 0.1,
                "informacion": 0.2,
                "sorpresa": 0.0
            },
            "keywords": [],
            "description": "Hoja neutral",
            "node_type": "leaf",
            "depth": 2
        }
    }


@pytest.fixture
def sample_preprocessed_data():
    """Datos preprocesados de ejemplo"""
    return {
        'cleaned_text': 'estoy muy feliz hoy',
        'words': ['estoy', 'muy', 'feliz', 'hoy'],
        'word_count': 4,
        'has_negation': False,
        'intensifiers': ['muy'],
        'attenuators': [],
        'punctuation_count': 0,
        'exclamation_count': 0,
        'question_count': 0,
        'uppercase_words': [],
        'emoticons': [],
        'processing_errors': []
    }


@pytest.fixture
def sample_sentiment_result():
    """Resultado de sentimiento de ejemplo"""
    return SentimentResult(
        text="Estoy muy feliz hoy",
        sentiments={
            'alegria': 0.85,
            'tristeza': 0.05,
            'enojo': 0.0,
            'preocupacion': 0.0,
            'informacion': 0.05,
            'sorpresa': 0.05
        },
        confidence=0.82,
        processing_time=0.15,
        matched_keywords={
            'alegria': ['feliz'],
            'tristeza': [],
            'enojo': [],
            'preocupacion': [],
            'informacion': [],
            'sorpresa': []
        },
        tree_path=['root', 'node_1', 'leaf_1'],
        modifiers_applied={
            'intensifiers': ['muy'],
            'negations': [],
            'attenuators': []
        },
        dominant_sentiment='alegria',
        secondary_sentiments=['informacion', 'sorpresa'],
        analysis_quality='high'
    )


@pytest.fixture
def temp_config_file():
    """Archivo de configuración temporal para pruebas"""
    config_data = {
        "max_text_length": 30,
        "min_confidence": 0.4,
        "enable_fuzzy_logic": True,
        "enable_memoization": False,
        "sentiment_thresholds": {
            "alegria": 0.5,
            "tristeza": 0.5,
            "enojo": 0.5,
            "preocupacion": 0.5,
            "informacion": 0.4,
            "sorpresa": 0.5
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        temp_file = f.name
    
    yield temp_file
    
    # Limpiar archivo temporal
    os.unlink(temp_file)


@pytest.fixture
def temp_keywords_file(sample_keywords_data):
    """Archivo de palabras clave temporal para pruebas"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_keywords_data, f)
        temp_file = f.name
    
    yield temp_file
    
    # Limpiar archivo temporal
    os.unlink(temp_file)


@pytest.fixture
def temp_tree_file(sample_tree_data):
    """Archivo de árbol temporal para pruebas"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_tree_data, f)
        temp_file = f.name
    
    yield temp_file
    
    # Limpiar archivo temporal
    os.unlink(temp_file)


@pytest.fixture
def text_preprocessor(sample_config):
    """Instancia de TextPreprocessor para pruebas"""
    return TextPreprocessor(sample_config)


@pytest.fixture
def keyword_matcher(sample_keywords_data):
    """Instancia de KeywordMatcher para pruebas"""
    return KeywordMatcher(sample_keywords_data)


@pytest.fixture
def score_normalizer(sample_config):
    """Instancia de ScoreNormalizer para pruebas"""
    return ScoreNormalizer(sample_config)


@pytest.fixture
def fuzzy_logic_processor(sample_config):
    """Instancia de FuzzyLogicProcessor para pruebas"""
    return FuzzyLogicProcessor(sample_config)


@pytest.fixture
def tree_searcher(sample_tree_data, sample_config):
    """Instancia de TreeSearcher para pruebas"""
    return TreeSearcher(sample_tree_data, sample_config) 