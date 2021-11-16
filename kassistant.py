# -*- coding: utf-8 -*-
import os
import time
import sys

from PyInquirer import prompt, Separator

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text
from rich.syntax import Syntax


from src.kubectl import (get_current_context, get_first_fav_namespace, 
    get_contexts as get_k_contexts, get_contexts_params,
    get_pods_params, get_pods,
    describe_pod_params, describe_pod,
    get_pod_containers_params, get_pod_containers,
    check_pod_logs_by_container, check_pod_logs_by_container_params,
    set_context, set_context_params)

from typing import List

console = Console()

def clear() -> None:
    """
    Limpa o terminal
    """
    os.system('clear') 

def header(context: str, namespace: str, pod: str, container: str) -> None:
    """
    Cria layout inicial
    """
    clear()
    console.print( Panel("ASSISTENTE KUBECTL") )

    renderables = [
        Panel(Text.assemble((context, "khaki1")), title="Contexto"),
        Panel(Text.assemble((namespace or "Nenhum selecionado", "cyan")), title="Namespace"),
        Panel(Text.assemble((pod or "Nenhum selecionado", "turquoise4")), title="Pod"),
        Panel(Text.assemble((container or "Nenhum selecionado", "medium_orchid")), title="Container")
    ]

    console.print(Columns(renderables))


def get_contexts(answers) -> List[str]:
    """
    Get contexts from kubectl environment
    """
    raw_contexts = get_k_contexts()

    return [line[10:22].strip() for line in raw_contexts.split('\n')[1:-1]]


def get_favorite_namespaces(answers) -> List[str]:
    """
    Get favorite namespaces from ns_favs.txt file
    """
    filename = "ns_favs.txt"
    options = []

    if os.path.exists(filename):
        with open(filename) as file:
            lines = file.readlines()
            options = [line.rstrip() for line in lines]

    if len(options):
        options.sort()
        return options
    else:
        clear()
        print()
        console.print( Text.assemble(("\tERRO: Nenhum namespace cadastrado no arquivo ", "dark_red"), ("ns_favs.txt", "red bold"))) 
        print()
        console.print( Text.assemble( ("\tVeja: ", "grey50"), ("https://github.com/alduxx/kubectl_assistant#add-namespaces", "grey42 underline"))) 
        print("\n\n")
        sys.exit(1)


def get_pods_from_namespace(answers, namespace: str) -> List[str]:
    """
    Get pods from namespace
    """
    if namespace is None:
        return []
    else:
        raw_pods = None
        with Progress() as progress:
            task = progress.add_task("[cyan]Buscando pods...", total=5, start=False)
            raw_pods = get_pods(namespace)
            progress.start_task(task)
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(0.06)

        return [line.split(' ', 1)[0] for line in raw_pods.split('\n')[1:]]


def get_containers_from_pod(answers, namespace: str, pod: str) -> List[str]:
    """
    Get pods from namespace
    """
    if namespace is None or pod is None:
        return []
    else:
        raw_containers = None
        with Progress() as progress:
            task = progress.add_task("[cyan]Buscando containers...", total=5, start=False)
            raw_containers = get_pod_containers(namespace, pod)
            progress.start_task(task)
            while not progress.finished:
                progress.update(task, advance=1)
                time.sleep(0.06)

        return [line for line in raw_containers.replace('"', '').split(' ')]


def print_on_last_line(message: str) -> None:
    columns, lines = os.get_terminal_size()

    print("\n", end="")  # Ensure the last line is available.
    print("\0337", end="")  # Save cursor position
    print(f"\033[0;{lines-1}r", end="")  # Reserve the bottom line
    print("\0338", end="")  # Restore the cursor position
    print("\033[1A", end="")  # Move up one line
    print("\0337", end="")  # Save cursor position
    print(f"\033[{lines};0f", end="")  # Move cursor to the bottom margin
    console.print( Text.assemble(("> " + message, "green"), end=""), end="" )
    print("\0338", end="")  # Restore cursor position


MENU_CHOICES = [ {
                    "value": "switch_context",
                    "name": "Mudar de contexto"
                }, {
                    "value": "select_namespace", 
                    "name": "Selecionar namespace"
                }, {
                    "value": "select_pod",
                    "name": "Selecionar pod",
                    "disabled": "Selecione um namespace"
                }, {
                    "name": "Detalhar Pod",
                    "value": "pod_details",
                    "disabled": "Selecione um pod"
                }, {
                    "value": "select_container",
                    "name": "Selecionar container",
                    "disabled": "Selecione um pod"
                }, {
                    "name": "Ver log",
                    "value": "pod_logs",
                    "disabled": "Selecione um container"
                }, {
                    "name": "Ver último comando kubectl",
                    "value": "last_command"
                }, {
                    "name": "Sair",
                    "value": "quit"
                }
            ]

questions = [
    {
        "type": "list",
        "name": "menu",
        "message": "Selecione uma opção:",
        "choices": MENU_CHOICES 
    },
    {
        "type": "list",
        "name": "kcontext",
        "message": "Selecione um contexto:",
        "choices": get_contexts,
        "when": lambda answers: answers.get("menu", "") == "switch_context"
    },
    {
        "type": "list",
        "name": "namespace",
        "message": "Selecione um namespace:",
        "choices": get_favorite_namespaces,
        "when": lambda answers: answers.get("menu", "") == "select_namespace"
    },
    {
        "type": "list",
        "name": "pod",
        "message": "Selecione um pod:",
        "choices": lambda answers: get_pods_from_namespace(answers, None),
        "when": lambda answers: answers.get("menu", "") == "select_pod"
    },
    {
        "type": "list",
        "name": "container",
        "message": "Selecione um container:",
        "choices": lambda answers: get_containers_from_pod(answers, None, None),
        "when": lambda answers: answers.get("menu", "") == "select_container"
    }
]


if __name__ == "__main__":
    current_context = get_current_context()
    current_namespace = None
    current_pod = None
    current_container = None
    last_cmd_params = get_contexts_params()

    while True:
        header(current_context, current_namespace, current_pod, current_container)
        print("")

        if last_cmd_params: # Prints kubeclt command on last line
            print_on_last_line(' '.join(last_cmd_params))

        answers = prompt(questions)

        if answers["menu"] == "switch_context":
            print("")
            kcontext = answers['kcontext']
            last_cmd_params = set_context_params(kcontext)
            ret = set_context(kcontext)
            current_context = get_current_context()
            print("")
        elif answers["menu"] == "select_namespace":
            current_namespace = answers['namespace']
            questions[3]["choices"] = lambda answers: get_pods_from_namespace(answers, current_namespace)
            MENU_CHOICES[2].pop('disabled', None) # enables pod selection
        elif answers["menu"] == "select_pod":
            if current_namespace is not None:
                current_pod = answers['pod']
                last_cmd_params = get_pods_params(current_namespace)
                questions[4]["choices"] = lambda answers: get_containers_from_pod(answers, current_namespace, current_pod)
                MENU_CHOICES[3].pop('disabled', None) # enables pod detail
                MENU_CHOICES[4].pop('disabled', None) # enables container select
        elif answers["menu"] == "last_command":
            console.print( Panel(Text.assemble((' '.join(last_cmd_params), "green"))) )
            print_on_last_line(' '.join(last_cmd_params))
            console.print(Text.assemble(("ENTER para continuar...", "grey30")) )
            input()
        elif answers["menu"] == "pod_details":
            last_cmd_params = describe_pod_params(current_namespace, current_pod)

            ret = None
            with Progress() as progress:
                task = progress.add_task("[cyan]Buscando pod info...", total=5, start=False)
                ret = describe_pod(current_namespace, current_pod)
                progress.start_task(task)
                while not progress.finished:
                    progress.update(task, advance=1)
                    time.sleep(0.06)

            syntax = Syntax(ret, "yaml", theme="monokai", line_numbers=True)
            console.print(syntax)
            console.print(Text.assemble(("ENTER para continuar...", "grey30")) )
            input()
        elif answers["menu"] == "select_container":
            current_container = answers['container']
            last_cmd_params = get_pod_containers_params(current_namespace, current_pod)
            MENU_CHOICES[5].pop('disabled', None) # enables container log
        elif answers["menu"] == "pod_logs":
            last_cmd_params = check_pod_logs_by_container_params(current_namespace, current_pod, current_container)

            ret = None
            with Progress() as progress:
                task = progress.add_task("[cyan]Buscando pod log...", total=5, start=False)
                ret = check_pod_logs_by_container(current_namespace, current_pod, current_container)
                progress.start_task(task)
                while not progress.finished:
                    progress.update(task, advance=1)
                    time.sleep(0.06)

            syntax = Syntax(ret, "yaml", theme="monokai", line_numbers=True)
            console.print(syntax)
            console.print(Text.assemble(("ENTER para continuar...", "grey30")) )
            input()
        elif answers["menu"] == "quit":
            break
        else:
            pass