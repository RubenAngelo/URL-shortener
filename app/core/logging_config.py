"""
Configuração de logging para módulos da aplicação.

Este módulo fornece uma função para configurar o sistema de logging,
definindo o nível de log, o formato das mensagens e os handlers utilizados.
"""

import logging

def setup_logging(module_name: str) -> logging.Logger:
    """
    Configura o sistema de logging para o módulo especificado.
    Este método inicializa a configuração básica de logging, definindo o nível de log como INFO,
    o formato da mensagem e o handler para saída no console. Retorna um logger associado ao nome
    do módulo fornecido.
    """

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     %(name)s module: %(message)s",
        handlers=[
            logging.StreamHandler(),
        ]
    )

    return logging.getLogger(module_name)
