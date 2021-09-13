import os

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from src.kubectl import get_pods, get_pods_params, get_contexts, get_contexts_params, set_context_params, set_context, describe_pod_params

# from src.globals import _func_waiting_key

import src.globals as globals

layout = Layout()


def clear() -> None:
    """
    Limpa o terminal
    """
    os.system('clear') 


def main_layout(contexto: str, namespace: str, pod: str) -> Layout:
    """
    Cria layout inicial
    """
    console = Console()

    #clear()

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
            name="info_context"
        ),
        Layout(
            Panel(f"[cyan]{namespace}", title="Namespace [F2]"),
            name="info_namespace"
        ),
    )

    return layout


def show_contexts() -> None:
    global _func_waiting_key 

    layout["info_context"].update(
        Panel(
            Spinner("aesthetic", text=Text.assemble(("buscando contextos...", "green")), style="green"),
            title="Contexto [F1]"
        )
    )

    params = get_contexts_params()

    layout["cmd"].update(
        Panel(
            Text.assemble((' '.join(params), "green")),
            title="CMD"
        )
    )

    contexts = get_contexts()

    panel_info = panel_context = None
    if "erro" in contexts.lower():
        panel_info = Panel(Text.assemble(("ERRO! ", "red")), title="Contexto [F1]")
        panel_context = Panel(Text.assemble((contexts, "orange3")))
    else:
        panel_info = Panel(Text.assemble(("Selecione um contexto", "orange3")), title="Contexto [F1]")

        table = Table(title="Selecione um contexto")
        table.add_column("Id", justify="right", style="cyan", no_wrap=True)
        table.add_column("Contexto", style="green")

        cont = 0
        options = {}
        for linha in contexts.split('\n'):
            if cont is not 0:
                _ctx = linha[10:22]
                if len(_ctx.strip()):
                    table.add_row(str(cont), _ctx)
                    options[cont] = _ctx
            cont += 1
            
        panel_context = Panel(table)
        globals._func_waiting_key = "update_context(\"_p_\")"
        globals._dict = str(options)


    layout["info_context"].update(panel_info)

    layout["contents"].update(
        Align.center(
            panel_context,
            vertical="middle"
        )
    )


def update_context(context) -> None:
    params = set_context_params(context)

    layout["cmd"].update(
        Panel(
            Text.assemble((' '.join(params), "green")),
            title="CMD"
        )
    )

    layout["info_context"].update(
        Panel(
            Spinner("aesthetic", text=Text.assemble(("Setando contexto...", "green")), style="green"),
            title="Contexto [F1]"
        )
    )

    result = set_context(context)


    info_ctx = ""
    if "erro" in result.lower():
        info_ctx = Text.assemble(("ERRO! ", "red"))
    else:
        info_ctx = Text.assemble((context, "cyan"))

    layout["contents"].update(
        Align.center(
            Text(result),
            vertical="middle"
        )
    )

    layout["info_context"].update(
        Panel(
            info_ctx,
            title="Contexto [F1]"
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


    table = Table(title="Pods do namespace %s" % namespace, show_lines=True)

    cont = 0
    options = {}
    for linha in pods.split('\n'):
        if len(linha.strip()) > 0:
            if cont == 0:
                table.add_column("Id", justify="left", style="green", no_wrap=True)
                table.add_column(linha[:55], justify="left", no_wrap=True, style="orange3")
                table.add_column(linha[56:62], justify="left", no_wrap=True, style="orange3")
                table.add_column(linha[64:71], justify="left", no_wrap=True, style="orange3")
                table.add_column(linha[74:82], justify="left", no_wrap=True, style="orange3")
                table.add_column(linha[85:88], justify="left", no_wrap=True, style="orange3")
            else:
                table.add_row(
                    str(cont),
                    linha[:55],
                    linha[56:62],
                    linha[64:71],
                    linha[74:82],
                    linha[85:88]
                )
                options[cont] = linha[:55]

        cont += 1


    layout["info_pod"].update(
        Panel(
            Text.assemble(text),
            title="Pod [F3]"
        )
    )

    layout["contents"].update(
        Panel(
            Align.center(
                table,
                vertical="middle"
            )
        )
    )

    globals._func_waiting_key = "select_pod('%s', '_p_')" % namespace
    globals._dict = str(options)


def message(msg) -> None:
    layout["info_context"].update(
        Panel(
            Text(msg),
            title="Contexto [F1]"
        )
    )

def select_pod(namespace: str, pod_name: str) -> None:
    """
    Atualiza pods e mostra na tela
    """

    params = describe_pod_params(namespace, pod_name)

    layout["cmd"].update(
        Panel(
            Text.assemble((' '.join(params), "green")),
            title="CMD"
        )
    )

    layout["info_pod"].update(
        Panel(
            Text.assemble((pod_name, "cyan")),
            title="Pod [F3]"
        )
    )