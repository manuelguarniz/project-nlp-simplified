#!/usr/bin/env python3
"""
Sistema de Análisis de Sentimientos
===================================

Punto de entrada principal del sistema de análisis de sentimientos.
Permite analizar textos desde la línea de comandos o como módulo.
"""

import sys
import argparse
import json
from typing import Dict, Any
from src.models.sentiment_analyzer import SentimentAnalyzer
from src.models.sentiment_result import SystemConfig
from src.models.exceptions import SentimentAnalysisError


def main():
    """Función principal del programa"""
    parser = argparse.ArgumentParser(
        description='Sistema de Análisis de Sentimientos Académico',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py "Estoy muy feliz hoy"
  python main.py --file textos.txt
  python main.py --interactive
  python main.py --config custom_config.json
        """
    )
    
    parser.add_argument(
        'text',
        nargs='?',
        help='Texto a analizar'
    )
    
    parser.add_argument(
        '--file', '-f',
        help='Archivo con textos a analizar (uno por línea)'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Modo interactivo'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Archivo de configuración personalizada'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Archivo de salida para resultados (formato JSON)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo verbose con información detallada'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Mostrar información del sistema'
    )
    
    args = parser.parse_args()
    
    try:
        # Cargar configuración
        config = load_config(args.config)
        
        # Inicializar analizador
        analyzer = SentimentAnalyzer(config)
        
        # Mostrar información del sistema si se solicita
        if args.info:
            show_system_info(analyzer)
            return
        
        # Procesar según el modo
        if args.interactive:
            interactive_mode(analyzer, args.verbose, args.output)
        elif args.file:
            file_mode(analyzer, args.file, args.verbose, args.output)
        elif args.text:
            single_text_mode(analyzer, args.text, args.verbose, args.output)
        else:
            # Modo por defecto: interactivo
            interactive_mode(analyzer, args.verbose, args.output)
    
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def load_config(config_file: str = None) -> SystemConfig:
    """
    Carga la configuración del sistema
    
    Args:
        config_file: Archivo de configuración personalizada
        
    Returns:
        Configuración del sistema
    """
    config = SystemConfig()
    
    if config_file:
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                custom_config = json.load(f)
            
            # Actualizar configuración con valores personalizados
            for key, value in custom_config.items():
                if hasattr(config, key):
                    setattr(config, key, value)
                    
        except FileNotFoundError:
            print(f"Advertencia: Archivo de configuración '{config_file}' no encontrado")
        except json.JSONDecodeError as e:
            print(f"Error al parsear archivo de configuración: {str(e)}")
    
    return config


def show_system_info(analyzer: SentimentAnalyzer):
    """Muestra información del sistema"""
    info = analyzer.get_system_info()
    
    print("=== INFORMACIÓN DEL SISTEMA ===")
    print(f"Versión: {info['version']}")
    print(f"Longitud máxima de texto: {info['config']['max_text_length']} palabras")
    print(f"Lógica difusa habilitada: {info['config']['enable_fuzzy_logic']}")
    print(f"Memoización habilitada: {info['config']['enable_memoization']}")
    
    print("\n=== INFORMACIÓN DEL ÁRBOL ===")
    tree_info = info['tree_info']
    print(f"Nodos totales: {tree_info.get('total_nodes', 0)}")
    print(f"Nodos hoja: {tree_info.get('leaf_nodes', 0)}")
    print(f"Nodos de decisión: {tree_info.get('decision_nodes', 0)}")
    print(f"Profundidad máxima: {tree_info.get('max_depth', 0)}")
    
    print("\n=== INFORMACIÓN DEL CACHE ===")
    cache_info = info['cache_info']
    print(f"Cache habilitado: {cache_info['enabled']}")
    print(f"Elementos en cache: {cache_info['size']}")
    
    print("\n=== COMPONENTES ===")
    for component, status in info['components'].items():
        print(f"{component}: {status}")


def interactive_mode(analyzer: SentimentAnalyzer, verbose: bool, output_file: str = None):
    """Modo interactivo"""
    print("=== MODO INTERACTIVO ===")
    print("Escribe textos para analizar (escribe 'salir' para terminar)")
    print("Escribe 'limpiar' para limpiar el cache")
    print("Escribe 'info' para mostrar información del sistema")
    print("-" * 50)
    
    results = []
    
    while True:
        try:
            text = input("\nTexto a analizar: ").strip()
            
            if not text:
                continue
            
            if text.lower() == 'salir':
                break
            elif text.lower() == 'limpiar':
                analyzer.clear_cache()
                print("Cache limpiado")
                continue
            elif text.lower() == 'info':
                show_system_info(analyzer)
                continue
            
            # Analizar texto
            result = analyzer.analyze(text)
            results.append(result)
            
            # Mostrar resultado
            display_result(result, verbose)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Guardar resultados si se especifica archivo de salida
    if output_file and results:
        save_results(results, output_file)
        print(f"\nResultados guardados en '{output_file}'")


def file_mode(analyzer: SentimentAnalyzer, file_path: str, verbose: bool, output_file: str = None):
    """Modo de archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        
        print(f"Analizando {len(texts)} textos desde '{file_path}'...")
        
        results = analyzer.batch_analyze(texts)
        
        # Mostrar resultados
        for i, result in enumerate(results):
            print(f"\n--- Texto {i+1} ---")
            display_result(result, verbose)
        
        # Guardar resultados
        if output_file:
            save_results(results, output_file)
            print(f"\nResultados guardados en '{output_file}'")
        else:
            save_results(results, 'resultados_analisis.json')
            print("\nResultados guardados en 'resultados_analisis.json'")
            
    except FileNotFoundError:
        print(f"Error: Archivo '{file_path}' no encontrado")
    except Exception as e:
        print(f"Error al procesar archivo: {str(e)}")


def single_text_mode(analyzer: SentimentAnalyzer, text: str, verbose: bool, output_file: str = None):
    """Modo de texto único"""
    try:
        result = analyzer.analyze(text)
        
        print("=== RESULTADO DEL ANÁLISIS ===")
        display_result(result, verbose)
        
        # Guardar resultado
        if output_file:
            save_results([result], output_file)
            print(f"\nResultado guardado en '{output_file}'")
            
    except Exception as e:
        print(f"Error: {str(e)}")


def display_result(result, verbose: bool):
    """Muestra el resultado del análisis"""
    print(f"Texto: {result.text}")
    print(f"Sentimiento dominante: {result.dominant_sentiment}")
    print(f"Confianza: {result.confidence:.3f}")
    print(f"Tiempo de procesamiento: {result.processing_time:.3f}s")
    print(f"Calidad del análisis: {result.analysis_quality}")
    
    print("\nPuntuaciones por sentimiento:")
    for sentiment, score in result.sentiments.items():
        print(f"  {sentiment}: {score:.3f}")
    
    if verbose:
        print(f"\nPalabras clave encontradas:")
        for sentiment, words in result.matched_keywords.items():
            if words:
                print(f"  {sentiment}: {', '.join(words)}")
        
        print(f"\nRuta en el árbol: {' -> '.join(result.tree_path)}")
        
        if result.modifiers_applied:
            print(f"\nModificadores aplicados:")
            for modifier_type, modifiers in result.modifiers_applied.items():
                if modifiers:
                    print(f"  {modifier_type}: {modifiers}")
        
        if result.secondary_sentiments:
            print(f"\nSentimientos secundarios: {', '.join(result.secondary_sentiments)}")


def save_results(results: list, output_file: str):
    """Guarda los resultados en un archivo JSON"""
    try:
        # Convertir resultados a formato serializable
        serializable_results = []
        for result in results:
            result_dict = result.to_dict()
            serializable_results.append(result_dict)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error al guardar resultados: {str(e)}")


if __name__ == "__main__":
    main() 