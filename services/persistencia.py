import json
import os


class Persistencia:
    @staticmethod
    def carregar_dados(caminho_arquivo):
        if not os.path.exists(caminho_arquivo):
            return []

        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []
        except Exception as e:
            print(f"Erro ao carregar dados de {caminho_arquivo}: {e}")
            return []

    @staticmethod
    def salvar_dados(caminho_arquivo, dados):
        try:
            os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar dados em {caminho_arquivo}: {e}")