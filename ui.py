from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.rule import Rule
from rich.prompt import Prompt
from time import sleep

console = Console()


def loading_fake(texto="Carregando..."):
    with Progress(
        SpinnerColumn(style="#89CFF0"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None, complete_style="#CDA4DE"),
        transient=True,
    ) as progress:
        task = progress.add_task(f"[#F9C6D3]{texto}", total=100)
        while not progress.finished:
            progress.update(task, advance=20)
            sleep(0.2)

def linha(texto=""):
    console.print(Rule(f"[#CDA4DE]{texto}"))

def sucesso(msg):
    console.print(f":white_check_mark: [bold #AEEEEE]{msg}[/]")

def erro(msg):
    console.print(f":x: [bold white on red] {msg} [/]")

def alerta(msg):
    console.print(f":warning: [bold #F9C6D3]{msg}[/]")

def info(msg):
    console.print(f":information_source: [italic #89CFF0]{msg}[/]")

def painel(texto, titulo="Info"):
    painel = Panel(
        f"[#FFFDD0]{texto}",
        title=f"[bold #89CFF0]{titulo}",
        border_style="#CDA4DE"
    )
    console.print(painel)

def menu(titulo, opcoes: list):
    linha(titulo)
    for i, opcao in enumerate(opcoes, 1):
        console.print(f"[#F9C6D3][{i}] [#FFFDD0]{opcao}")
    console.print(f"[#F9C6D3][0] [#FFFDD0]Sair")
    escolha = Prompt.ask(f"[#89CFF0]Escolha uma opção", default="0")
    return escolha

def input_pastel(texto):
    return Prompt.ask(f"[#CDA4DE]{texto}")


def pause():
    console.print("\n[#FFFDD0]Pressione Enter para continuar...[/]")
    input()