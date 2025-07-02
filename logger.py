import logging
from logging import Logger, FileHandler, Formatter
from rich.console import Console
from rich.panel import Panel
console = Console()

logger: Logger = logging.getLogger("elo_logger")
logger.setLevel(logging.DEBUG)  # Captura todos os níveis (INFO, WARNING, ERROR, CRITICAL)


LOG_FILE = "elo.log"


file_handler = FileHandler(LOG_FILE, mode="a", encoding="utf-8", delay=False)
file_handler.setLevel(logging.DEBUG)

# Formato para o arquivo: [DD/MM/YYYY HH:MM:SS] [NÍVEL] Mensagem
file_formatter = Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s",
                           datefmt="%d/%m/%Y %H:%M:%S")
file_handler.setFormatter(file_formatter)


if not logger.handlers:
    logger.addHandler(file_handler)


# Funções de log estilizadas no terminal
def log_info(msg: str):
    logger.info(msg)
    console.print(f"[bold #89CFF0][INFO][/]: {msg}")


def log_sucesso(msg: str):
    logger.info(f"[SUCESSO] {msg}")
    console.print(f":white_check_mark: [bold #AEEEEE][SUCESSO][/]: {msg}")


def log_erro(msg: str):
    logger.error(msg)
    console.print(f":x: [bold white on red][ERRO][/]: {msg}")


def log_alerta(msg: str):
    logger.warning(msg)
    console.print(f":warning: [bold #F9C6D3][ALERTA][/]: {msg}")


def log_critico(msg: str):
    logger.critical(msg)
    painel = Panel(
        f"[bold white on red]{msg}",
        title="[bold red]CRÍTICO",
        border_style="red"
    )
    console.print(painel)