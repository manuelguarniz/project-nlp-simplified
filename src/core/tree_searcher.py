"""
Buscador en Árbol de Decisión
=============================

Módulo responsable de realizar búsquedas en el árbol de decisión
para determinar las puntuaciones base de sentimientos.
"""

import time
import json
from typing import Dict, List, Any, Optional
from ..models.sentiment_result import SystemConfig, DecisionTreeNode
from ..models.exceptions import TreeSearchError


class TreeSearcher:
    """Buscador en árbol de decisión"""
    
    def __init__(self, tree_data: Dict, config: SystemConfig):
        self.tree = self._build_tree(tree_data)
        self.config = config
        self.memoization_cache = {} if config.enable_memoization else None
        self.search_stats = {
            'nodes_visited': 0,
            'cache_hits': 0,
            'backtrack_count': 0,
            'search_time': 0.0
        }
    
    def search(self, preprocessed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza búsqueda en el árbol de decisión
        
        Args:
            preprocessed_data: Datos preprocesados del texto
            
        Returns:
            Dict con resultados de la búsqueda
        """
        start_time = time.time()
        self.search_stats['nodes_visited'] = 0
        self.search_stats['cache_hits'] = 0
        self.search_stats['backtrack_count'] = 0
        
        try:
            # Verificar cache si está habilitado
            cache_key = self._generate_cache_key(preprocessed_data)
            if self.memoization_cache and cache_key in self.memoization_cache:
                self.search_stats['cache_hits'] += 1
                cached_result = self.memoization_cache[cache_key]
                cached_result['cache_hits'] = self.search_stats['cache_hits']
                cached_result['search_time'] = time.time() - start_time
                return cached_result
            
            # Realizar búsqueda
            path = []
            current_node_id = 'root'
            max_depth = self.config.tree_search.get('max_depth', 10)
            timeout = self.config.tree_search.get('timeout_seconds', 5)
            
            while current_node_id and len(path) < max_depth:
                # Verificar timeout
                if time.time() - start_time > timeout:
                    raise TreeSearchError("Timeout en búsqueda del árbol")
                
                if current_node_id not in self.tree:
                    raise TreeSearchError(f"Nodo {current_node_id} no encontrado en el árbol")
                
                current_node = self.tree[current_node_id]
                path.append(current_node_id)
                self.search_stats['nodes_visited'] += 1
                
                # Si es nodo hoja, retornar puntuaciones
                if current_node.node_type == 'leaf':
                    result = {
                        'path': path,
                        'final_scores': current_node.sentiment_scores,
                        'matched_keywords': self._extract_keywords_from_path(path),
                        'confidence': self._calculate_path_confidence(path),
                        'search_depth': len(path),
                        'nodes_visited': self.search_stats['nodes_visited'],
                        'search_time': time.time() - start_time,
                        'cache_hits': self.search_stats['cache_hits'],
                        'backtrack_count': self.search_stats['backtrack_count']
                    }
                    
                    # Guardar en cache si está habilitado
                    if self.memoization_cache is not None:
                        self._add_to_cache(cache_key, result)
                    
                    return result
                
                # Evaluar condición del nodo
                if current_node.condition:
                    condition_result = self.evaluate_condition(
                        current_node.condition, 
                        preprocessed_data
                    )
                    
                    # Seguir rama correspondiente
                    branch_key = 'true' if condition_result else 'false'
                    current_node_id = current_node.branches.get(branch_key)
                else:
                    # Nodo sin condición, seguir rama por defecto
                    current_node_id = current_node.branches.get('default', current_node.branches.get('true'))
            
            # Si llegamos aquí, no se encontró nodo hoja
            raise TreeSearchError("No se pudo encontrar un nodo hoja en el árbol")
            
        except Exception as e:
            self.search_stats['search_time'] = time.time() - start_time
            raise TreeSearchError(f"Error en búsqueda del árbol: {str(e)}")
    
    def evaluate_condition(self, condition: str, data: Dict[str, Any]) -> bool:
        """
        Evalúa una condición del árbol
        
        Args:
            condition: Condición a evaluar
            data: Datos preprocesados
            
        Returns:
            True si la condición se cumple, False en caso contrario
        """
        try:
            # Reemplazar funciones con valores reales
            condition = self._replace_functions(condition, data)
            
            # Evaluar la condición
            return eval(condition)
            
        except Exception as e:
            raise TreeSearchError(f"Error al evaluar condición '{condition}': {str(e)}")
    
    def _build_tree(self, tree_data: Dict) -> Dict[str, DecisionTreeNode]:
        """
        Construye el árbol de decisión desde los datos JSON
        
        Args:
            tree_data: Datos del árbol en formato JSON
            
        Returns:
            Dict con nodos del árbol
        """
        tree = {}
        
        try:
            if isinstance(tree_data, str):
                # Si es un string, asumir que es un archivo JSON
                with open(tree_data, 'r', encoding='utf-8') as f:
                    tree_data = json.load(f)
            
            for node_id, node_data in tree_data.items():
                tree[node_id] = DecisionTreeNode(
                    id=node_id,
                    condition=node_data.get('condition'),
                    branches=node_data.get('branches', {}),
                    sentiment_scores=node_data.get('sentiment_scores', {}),
                    keywords=node_data.get('keywords', []),
                    description=node_data.get('description', ''),
                    node_type=node_data.get('node_type', 'decision'),
                    depth=node_data.get('depth', 0),
                    parent_id=node_data.get('parent_id'),
                    children_ids=node_data.get('children_ids', [])
                )
            
            return tree
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise TreeSearchError(f"Error al cargar árbol de decisión: {str(e)}")
    
    def _replace_functions(self, condition: str, data: Dict[str, Any]) -> str:
        """
        Reemplaza funciones en la condición con valores reales
        
        Args:
            condition: Condición con funciones
            data: Datos preprocesados
            
        Returns:
            Condición con valores reemplazados
        """
        # Reemplazar has_keyword(sentiment, word)
        if 'has_keyword(' in condition:
            condition = self._replace_has_keyword(condition, data)
        
        # Reemplazar word_count
        if 'word_count' in condition:
            condition = condition.replace('word_count', str(data.get('word_count', 0)))
        
        # Reemplazar has_intensifier()
        if 'has_intensifier()' in condition:
            has_intensifier = len(data.get('intensifiers', [])) > 0
            condition = condition.replace('has_intensifier()', str(has_intensifier))
        
        # Reemplazar has_negation()
        if 'has_negation()' in condition:
            has_negation = data.get('has_negation', False)
            condition = condition.replace('has_negation()', str(has_negation))
        
        # Reemplazar has_emoticon()
        if 'has_emoticon()' in condition:
            has_emoticon = len(data.get('emoticons', [])) > 0
            condition = condition.replace('has_emoticon()', str(has_emoticon))
        
        # Reemplazar is_question()
        if 'is_question()' in condition:
            is_question = data.get('question_count', 0) > 0
            condition = condition.replace('is_question()', str(is_question))
        
        # Reemplazar is_exclamation()
        if 'is_exclamation()' in condition:
            is_exclamation = data.get('exclamation_count', 0) > 0
            condition = condition.replace('is_exclamation()', str(is_exclamation))
        
        return condition
    
    def _replace_has_keyword(self, condition: str, data: Dict[str, Any]) -> str:
        """
        Reemplaza la función has_keyword con valores reales
        
        Args:
            condition: Condición con has_keyword
            data: Datos preprocesados
            
        Returns:
            Condición con has_keyword reemplazado
        """
        import re
        
        # Patrón para has_keyword(sentiment, word)
        pattern = r'has_keyword\([\'"]([^\'"]+)[\'"],\s*[\'"]([^\'"]+)[\'"]\)'
        
        def replace_match(match):
            sentiment = match.group(1)
            word = match.group(2)
            
            # Verificar si la palabra está en las palabras del texto
            words = data.get('words', [])
            has_word = word.lower() in [w.lower() for w in words]
            
            return str(has_word)
        
        return re.sub(pattern, replace_match, condition)
    
    def _extract_keywords_from_path(self, path: List[str]) -> Dict[str, List[str]]:
        """
        Extrae palabras clave de la ruta recorrida
        
        Args:
            path: Ruta recorrida en el árbol
            
        Returns:
            Dict con palabras clave por sentimiento
        """
        keywords = {
            'alegria': [],
            'tristeza': [],
            'enojo': [],
            'preocupacion': [],
            'informacion': [],
            'sorpresa': []
        }
        
        for node_id in path:
            if node_id in self.tree:
                node = self.tree[node_id]
                for keyword in node.keywords:
                    # Determinar sentimiento basado en la puntuación más alta
                    if node.sentiment_scores:
                        dominant_sentiment = max(
                            node.sentiment_scores.items(), 
                            key=lambda x: x[1]
                        )[0]
                        if dominant_sentiment in keywords:
                            keywords[dominant_sentiment].append(keyword)
        
        return keywords
    
    def _calculate_path_confidence(self, path: List[str]) -> float:
        """
        Calcula la confianza basada en la ruta recorrida
        
        Args:
            path: Ruta recorrida en el árbol
            
        Returns:
            Valor de confianza
        """
        if not path:
            return 0.0
        
        # Confianza base basada en la profundidad
        depth_confidence = min(1.0, len(path) / 5.0)
        
        # Confianza adicional por nodos visitados
        node_confidence = min(1.0, self.search_stats['nodes_visited'] / 10.0)
        
        # Confianza por eficiencia (menos backtracking = mejor)
        efficiency_confidence = max(0.5, 1.0 - (self.search_stats['backtrack_count'] / 5.0))
        
        # Promedio ponderado
        confidence = (
            depth_confidence * 0.4 +
            node_confidence * 0.3 +
            efficiency_confidence * 0.3
        )
        
        return min(1.0, confidence)
    
    def _generate_cache_key(self, preprocessed_data: Dict[str, Any]) -> str:
        """
        Genera una clave única para el cache
        
        Args:
            preprocessed_data: Datos preprocesados
            
        Returns:
            Clave única para el cache
        """
        # Usar palabras y modificadores como clave
        words = tuple(sorted(preprocessed_data.get('words', [])))
        intensifiers = tuple(sorted(preprocessed_data.get('intensifiers', [])))
        attenuators = tuple(sorted(preprocessed_data.get('attenuators', [])))
        negations = tuple(sorted(preprocessed_data.get('negations', [])))
        
        return f"{words}_{intensifiers}_{attenuators}_{negations}"
    
    def _add_to_cache(self, key: str, result: Dict[str, Any]):
        """
        Agrega resultado al cache
        
        Args:
            key: Clave del cache
            result: Resultado a cachear
        """
        if not self.memoization_cache:
            return
        
        cache_size = self.config.tree_search.get('cache_size', 1000)
        
        # Si el cache está lleno, remover elemento menos usado
        if len(self.memoization_cache) >= cache_size:
            self._evict_least_used()
        
        self.memoization_cache[key] = result
    
    def _evict_least_used(self):
        """Remueve el elemento menos usado del cache"""
        if not self.memoization_cache:
            return
        
        # Implementación simple: remover el primer elemento
        first_key = next(iter(self.memoization_cache))
        del self.memoization_cache[first_key]
    
    def get_tree_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el árbol
        
        Returns:
            Dict con información del árbol
        """
        if not self.tree:
            return {}
        
        node_count = len(self.tree)
        leaf_count = sum(1 for node in self.tree.values() if node.node_type == 'leaf')
        decision_count = sum(1 for node in self.tree.values() if node.node_type == 'decision')
        max_depth = max((node.depth for node in self.tree.values()), default=0)
        
        return {
            'total_nodes': node_count,
            'leaf_nodes': leaf_count,
            'decision_nodes': decision_count,
            'max_depth': max_depth,
            'cache_size': len(self.memoization_cache) if self.memoization_cache else 0
        } 