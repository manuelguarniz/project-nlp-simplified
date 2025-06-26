"""
Pruebas Unitarias para TreeSearcher
==================================

Pruebas para el módulo de búsqueda en árbol de decisión.
"""

import pytest
import time
from src.core.tree_searcher import TreeSearcher
from src.models.exceptions import TreeSearchError


class TestTreeSearcher:
    """Pruebas para TreeSearcher"""
    
    def test_basic_tree_search(self, tree_searcher, sample_preprocessed_data):
        """TC-TREE-001: Búsqueda básica con palabra clave de alegría"""
        # Modificar datos para que coincida con la condición del árbol
        sample_preprocessed_data['words'] = ['estoy', 'muy', 'feliz', 'hoy']
        
        result = tree_searcher.search(sample_preprocessed_data)
        
        assert 'path' in result
        assert 'final_scores' in result
        assert 'matched_keywords' in result
        assert 'confidence' in result
        assert result['confidence'] > 0.0
        assert result['confidence'] <= 1.0
    
    def test_tree_search_with_intensifier(self, tree_searcher, sample_preprocessed_data):
        """TC-TREE-002: Búsqueda con intensificador"""
        sample_preprocessed_data['words'] = ['estoy', 'muy', 'feliz']
        sample_preprocessed_data['intensifiers'] = ['muy']
        
        result = tree_searcher.search(sample_preprocessed_data)
        
        assert 'leaf_1' in result['path']  # Debería llegar a la hoja con intensificador
        assert result['final_scores']['alegria'] > 0.8  # Puntuación alta
    
    def test_tree_search_without_intensifier(self, tree_searcher, sample_preprocessed_data):
        """TC-TREE-003: Búsqueda sin intensificador"""
        sample_preprocessed_data['words'] = ['estoy', 'feliz']
        sample_preprocessed_data['intensifiers'] = []
        
        result = tree_searcher.search(sample_preprocessed_data)
        
        assert 'leaf_2' in result['path']  # Debería llegar a la hoja sin intensificador
        assert result['final_scores']['alegria'] < 0.9  # Puntuación menor
    
    def test_tree_search_sadness_keyword(self, tree_searcher, sample_preprocessed_data):
        """TC-TREE-004: Búsqueda con palabra clave de tristeza"""
        sample_preprocessed_data['words'] = ['estoy', 'triste']
        sample_preprocessed_data['intensifiers'] = []
        
        result = tree_searcher.search(sample_preprocessed_data)
        
        assert 'leaf_3' in result['path']  # Debería llegar a la hoja de tristeza
        assert result['final_scores']['tristeza'] > 0.7  # Puntuación alta de tristeza
    
    def test_tree_search_no_keywords(self, tree_searcher, sample_preprocessed_data):
        """TC-TREE-005: Búsqueda sin palabras clave"""
        sample_preprocessed_data['words'] = ['estoy', 'bien']
        sample_preprocessed_data['intensifiers'] = []
        
        result = tree_searcher.search(sample_preprocessed_data)
        
        assert 'leaf_4' in result['path']  # Debería llegar a la hoja neutral
        # Puntuaciones más balanceadas
        assert result['final_scores']['alegria'] > 0.0
        assert result['final_scores']['tristeza'] > 0.0
    
    def test_evaluate_condition_true(self, tree_searcher, sample_preprocessed_data):
        """Prueba evaluación de condición verdadera"""
        condition = "has_keyword('alegria', 'feliz')"
        sample_preprocessed_data['words'] = ['estoy', 'feliz']
        
        result = tree_searcher.evaluate_condition(condition, sample_preprocessed_data)
        
        assert result == True
    
    def test_evaluate_condition_false(self, tree_searcher, sample_preprocessed_data):
        """Prueba evaluación de condición falsa"""
        condition = "has_keyword('alegria', 'feliz')"
        sample_preprocessed_data['words'] = ['estoy', 'triste']
        
        result = tree_searcher.evaluate_condition(condition, sample_preprocessed_data)
        
        assert result == False
    
    def test_evaluate_condition_with_intensifier(self, tree_searcher, sample_preprocessed_data):
        """Prueba evaluación de condición con intensificador"""
        condition = "has_intensifier()"
        sample_preprocessed_data['intensifiers'] = ['muy']
        
        result = tree_searcher.evaluate_condition(condition, sample_preprocessed_data)
        
        assert result == True
    
    def test_evaluate_condition_without_intensifier(self, tree_searcher, sample_preprocessed_data):
        """Prueba evaluación de condición sin intensificador"""
        condition = "has_intensifier()"
        sample_preprocessed_data['intensifiers'] = []
        
        result = tree_searcher.evaluate_condition(condition, sample_preprocessed_data)
        
        assert result == False
    
    def test_evaluate_condition_with_negation(self, tree_searcher, sample_preprocessed_data):
        """Prueba evaluación de condición con negación"""
        condition = "has_negation()"
        sample_preprocessed_data['has_negation'] = True
        
        result = tree_searcher.evaluate_condition(condition, sample_preprocessed_data)
        
        assert result == True
    
    def test_evaluate_condition_word_count(self, tree_searcher, sample_preprocessed_data):
        """Prueba evaluación de condición con conteo de palabras"""
        condition = "word_count > 3"
        sample_preprocessed_data['word_count'] = 5
        
        result = tree_searcher.evaluate_condition(condition, sample_preprocessed_data)
        
        assert result == True
    
    def test_evaluate_condition_invalid(self, tree_searcher, sample_preprocessed_data):
        """Prueba evaluación de condición inválida"""
        condition = "invalid_function()"
        
        with pytest.raises(TreeSearchError):
            tree_searcher.evaluate_condition(condition, sample_preprocessed_data)
    
    def test_build_tree_from_dict(self, sample_config, sample_tree_data):
        """Prueba construcción de árbol desde diccionario"""
        searcher = TreeSearcher(sample_tree_data, sample_config)
        
        assert 'root' in searcher.tree
        assert 'leaf_1' in searcher.tree
        assert searcher.tree['root'].node_type == 'root'
        assert searcher.tree['leaf_1'].node_type == 'leaf'
    
    def test_build_tree_from_file(self, sample_config, temp_tree_file):
        """Prueba construcción de árbol desde archivo"""
        searcher = TreeSearcher(temp_tree_file, sample_config)
        
        assert 'root' in searcher.tree
        assert len(searcher.tree) > 0
    
    def test_build_tree_invalid_file(self, sample_config):
        """Prueba construcción de árbol con archivo inválido"""
        with pytest.raises(TreeSearchError):
            TreeSearcher("archivo_inexistente.json", sample_config)
    
    def test_extract_keywords_from_path(self, tree_searcher):
        """Prueba extracción de palabras clave de la ruta"""
        path = ['root', 'node_1', 'leaf_1']
        
        keywords = tree_searcher._extract_keywords_from_path(path)
        
        assert 'alegria' in keywords
        assert isinstance(keywords['alegria'], list)
    
    def test_calculate_path_confidence(self, tree_searcher):
        """Prueba cálculo de confianza de la ruta"""
        path = ['root', 'node_1', 'leaf_1']
        
        confidence = tree_searcher._calculate_path_confidence(path)
        
        assert confidence > 0.0
        assert confidence <= 1.0
    
    def test_calculate_path_confidence_empty(self, tree_searcher):
        """Prueba cálculo de confianza con ruta vacía"""
        path = []
        
        confidence = tree_searcher._calculate_path_confidence(path)
        
        assert confidence == 0.0
    
    def test_generate_cache_key(self, tree_searcher, sample_preprocessed_data):
        """Prueba generación de clave de cache"""
        key = tree_searcher._generate_cache_key(sample_preprocessed_data)
        
        assert isinstance(key, str)
        assert len(key) > 0
    
    def test_cache_functionality(self, sample_config, sample_tree_data):
        """Prueba funcionalidad del cache"""
        searcher = TreeSearcher(sample_tree_data, sample_config)
        sample_data = {
            'words': ['estoy', 'feliz'],
            'intensifiers': ['muy'],
            'attenuators': [],
            'negations': []
        }
        
        # Primera búsqueda
        result1 = searcher.search(sample_data)
        
        # Segunda búsqueda (debería usar cache)
        result2 = searcher.search(sample_data)
        
        # Los resultados deberían ser iguales
        assert result1['final_scores'] == result2['final_scores']
        assert result2['cache_hits'] > 0
    
    def test_cache_disabled(self, sample_config, sample_tree_data):
        """Prueba cache deshabilitado"""
        sample_config.enable_memoization = False
        searcher = TreeSearcher(sample_tree_data, sample_config)
        
        assert searcher.memoization_cache is None
    
    def test_timeout_functionality(self, sample_config, sample_tree_data):
        """Prueba funcionalidad de timeout"""
        # Configurar timeout muy corto
        sample_config.tree_search['timeout_seconds'] = 0.001
        searcher = TreeSearcher(sample_tree_data, sample_config)
        
        sample_data = {
            'words': ['estoy', 'feliz'],
            'intensifiers': [],
            'attenuators': [],
            'negations': []
        }
        
        # Agregar delay artificial para simular procesamiento lento
        original_evaluate = searcher.evaluate_condition
        def slow_evaluate(*args, **kwargs):
            time.sleep(0.01)  # Delay de 10ms
            return original_evaluate(*args, **kwargs)
        
        searcher.evaluate_condition = slow_evaluate
        
        with pytest.raises(TreeSearchError, match="Timeout"):
            searcher.search(sample_data)
    
    def test_max_depth_limit(self, sample_config, sample_tree_data):
        """Prueba límite de profundidad máxima"""
        # Configurar profundidad máxima muy baja
        sample_config.tree_search['max_depth'] = 1
        searcher = TreeSearcher(sample_tree_data, sample_config)
        
        sample_data = {
            'words': ['estoy', 'feliz'],
            'intensifiers': [],
            'attenuators': [],
            'negations': []
        }
        
        with pytest.raises(TreeSearchError, match="No se pudo encontrar un nodo hoja"):
            searcher.search(sample_data)
    
    def test_get_tree_info(self, tree_searcher):
        """Prueba obtención de información del árbol"""
        info = tree_searcher.get_tree_info()
        
        assert 'total_nodes' in info
        assert 'leaf_nodes' in info
        assert 'decision_nodes' in info
        assert 'max_depth' in info
        assert 'cache_size' in info
        
        assert info['total_nodes'] > 0
        assert info['leaf_nodes'] > 0
        assert info['decision_nodes'] > 0
    
    def test_replace_has_keyword_function(self, tree_searcher, sample_preprocessed_data):
        """Prueba reemplazo de función has_keyword"""
        condition = "has_keyword('alegria', 'feliz')"
        sample_preprocessed_data['words'] = ['estoy', 'feliz']
        
        replaced = tree_searcher._replace_has_keyword(condition, sample_preprocessed_data)
        
        assert replaced == "True"  # Debería ser True ya que 'feliz' está en las palabras
    
    def test_replace_has_keyword_function_not_found(self, tree_searcher, sample_preprocessed_data):
        """Prueba reemplazo de función has_keyword sin coincidencia"""
        condition = "has_keyword('alegria', 'xyz')"
        sample_preprocessed_data['words'] = ['estoy', 'feliz']
        
        replaced = tree_searcher._replace_has_keyword(condition, sample_preprocessed_data)
        
        assert replaced == "False"  # Debería ser False ya que 'xyz' no está en las palabras
    
    def test_replace_functions_complex(self, tree_searcher, sample_preprocessed_data):
        """Prueba reemplazo de múltiples funciones"""
        condition = "has_keyword('alegria', 'feliz') and has_intensifier() and word_count > 2"
        sample_preprocessed_data['words'] = ['estoy', 'muy', 'feliz']
        sample_preprocessed_data['intensifiers'] = ['muy']
        sample_preprocessed_data['word_count'] = 3
        
        replaced = tree_searcher._replace_functions(condition, sample_preprocessed_data)
        
        # Debería reemplazar todas las funciones
        assert "has_keyword" not in replaced
        assert "has_intensifier" not in replaced
        assert "word_count" not in replaced
    
    def test_search_stats_tracking(self, tree_searcher, sample_preprocessed_data):
        """Prueba seguimiento de estadísticas de búsqueda"""
        sample_preprocessed_data['words'] = ['estoy', 'feliz']
        
        result = tree_searcher.search(sample_preprocessed_data)
        
        assert result['nodes_visited'] > 0
        assert result['search_time'] > 0.0
        assert result['search_depth'] > 0
    
    def test_error_handling_invalid_node(self, tree_searcher, sample_preprocessed_data):
        """Prueba manejo de errores con nodo inválido"""
        # Modificar el árbol para tener una rama inválida
        tree_searcher.tree['root'].branches['true'] = 'invalid_node'
        
        sample_preprocessed_data['words'] = ['estoy', 'feliz']
        
        with pytest.raises(TreeSearchError, match="no encontrado"):
            tree_searcher.search(sample_preprocessed_data)
    
    def test_error_handling_missing_leaf(self, sample_config, sample_tree_data):
        """Prueba manejo de errores sin nodo hoja"""
        # Modificar el árbol para que no tenga nodos hoja
        sample_tree_data['root']['branches']['true'] = 'node_1'
        sample_tree_data['node_1']['branches']['true'] = 'node_1'  # Loop infinito
        
        searcher = TreeSearcher(sample_tree_data, sample_config)
        sample_data = {
            'words': ['estoy', 'feliz'],
            'intensifiers': [],
            'attenuators': [],
            'negations': []
        }
        
        with pytest.raises(TreeSearchError, match="No se pudo encontrar un nodo hoja"):
            searcher.search(sample_data)
    
    def test_cache_eviction(self, sample_config, sample_tree_data):
        """Prueba expulsión del cache"""
        sample_config.tree_search['cache_size'] = 1
        searcher = TreeSearcher(sample_tree_data, sample_config)
        
        sample_data1 = {
            'words': ['estoy', 'feliz'],
            'intensifiers': [],
            'attenuators': [],
            'negations': []
        }
        
        sample_data2 = {
            'words': ['estoy', 'triste'],
            'intensifiers': [],
            'attenuators': [],
            'negations': []
        }
        
        # Primera búsqueda
        searcher.search(sample_data1)
        
        # Segunda búsqueda (debería expulsar la primera)
        searcher.search(sample_data2)
        
        # El cache debería tener solo un elemento
        assert len(searcher.memoization_cache) == 1 