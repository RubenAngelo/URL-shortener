import logging

def setup_logging(module_name: str):
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s:     %(name)s module: %(message)s",
        handlers=[
            logging.StreamHandler(),
        ]
    )

    return logging.getLogger(module_name)
