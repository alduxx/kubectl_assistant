import os

from time import sleep

from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.spinner import Spinner, SPINNERS
from rich.layout import Layout
from rich.markdown import Markdown

from src.kubectl import get_pods, get_pods_params

layout = Layout()


def clear() -> None:
    os.system('clear') # clears terminal


def main_layout(contexto: str, namespace: str, pod: str) -> Layout:
    console = Console()

    clear()

    layout.split_column(
        Layout( 
            Panel("ASSISTENTE KUBECTL", style="on blue"), 
            name="title",
            size=3
        ),
        Layout(name="info", size=3),
        Layout(
            Panel(Text.assemble(("Aperte F3 para listar os pods.", "green")), title="Pod [F3]"),
            name="info_pod",
            size=3
        ),
        Layout(
            Panel(""),
            name="contents"
        ),
        Layout(
            Panel("", title="CMD"),
            name="cmd",
            size=3
        ),
    )

    layout["info"].split_row(
        Layout(
            Panel(f"[cyan]{contexto}", title="Contexto [F1]"),
            name="left"
        ),
        Layout(
            Panel(f"[cyan]{namespace}", title="Namespace [F2]"),
            name="middle"
        ),
    )

    return layout


def update_contents(text:str) -> None:
    layout["contents"].update(
        Align.center(
            Text(
                "texto: %s" % text,
                justify="center",
            ),
            vertical="middle",
        )
    )


def update_pods(namespace:str) -> None:
    """
    Atualiza pods e mostra na tela
    """

    layout["info_pod"].update(
        Panel(
            Spinner("aesthetic", text=Text.assemble(("buscando pods...", "green")), style="green"),
            title="Pod [F3]"
        )
    )

    params = get_pods_params(namespace)

    layout["cmd"].update(
        Panel(
            Text.assemble((' '.join(params), "green")),
            title="CMD"
        )
    )

    pods = get_pods(namespace)

    if "erro" in pods.lower():
        text = Text.assemble(("ERRO! ", "red")),
    else:
        text = Text.assemble(("Selecione um pod abaixo para ver mais detalhes", "orange3")),

    layout["info_pod"].update(
        Panel(
            Text.assemble(text),
            title="Pod [F3]"
        )
    )

    layout["contents"].update(
        Panel(
            Text.assemble((pods, "orange3"))
        )
    )