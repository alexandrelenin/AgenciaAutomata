import argparse
import sys
import os

# Adiciona o diretório src ao path para que possamos importar nossos módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.processing.analyzer import process_media_file

def main():
    """
    Ponto de entrada do script para processar um novo arquivo de mídia.
    Este script será chamado pelo N8N.
    """
    parser = argparse.ArgumentParser(description="Processa um arquivo de mídia para análise e catalogação.")
    parser.add_argument("file_path", type=str, help="O caminho absoluto para o arquivo a ser processado.")
    args = parser.parse_args()

    print(f"Iniciando processamento para o arquivo: {args.file_path}")

    try:
        result = process_media_file(args.file_path)
        print("Processamento concluído com sucesso.")
        print(f"Resultado: {result}")
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()