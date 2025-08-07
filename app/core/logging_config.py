"""
Configuração de logging para módulos da aplicação.

Este módulo fornece uma função para configurar o sistema de logging,
definindo o nível de log, o formato das mensagens e os handlers utilizados.
"""

import logging


def setup_logging(module_name: str) -> logging.Logger:
    """
    Configura o sistema de logging para o módulo especificado.
    """

    logger = logging.getLogger(module_name)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()

        formatter = logging.Formatter("%(levelname)s:     %(name)s: %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        logger.setLevel(logging.INFO)

    return logger
