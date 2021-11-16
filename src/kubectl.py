import subprocess

from typing import List, Tuple

NS_FAVS = [
    'imc-mercado-capitais-api',
    'imc-mercado-capitais-exporter'
]

def get_current_context() -> str:
    """
    Returns current kubetclt context
    """
    try:
        params = ('kubectl', 'config', 'current-context')

        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout.replace('\n', '')
    except:
        return "Err fetching context"


def get_first_fav_namespace() -> str:
    """
    Returns first item of NS_FAVS. Otherwise, returns None
    """
    try:
        return NS_FAVS[0]
    except:
        return None



def get_pods_params(namespace: str) -> Tuple[str]:
        return ('kubectl', 'get', 'pods', '--namespace', namespace)

def get_pods(namespace: str) -> str:
    """
    Devolve os pods daquele namespace
    """
    try:
        params = get_pods_params(namespace)
        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except Exception as err:
        return "Erro ao executar get_pods:\nnamespace: %s\n%s" % (namespace, err)


def get_contexts_params() -> Tuple[str]:
    return ('kubectl', 'config', 'get-contexts')

def get_contexts() -> str:
    """
    Devolve os contextos disponíveis
    """
    try:
        params = get_contexts_params()

        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except Exception as err:
        return "Erro ao executar get_contexts:\n%s" % err


def set_context_params(context) -> Tuple[str]:
    return ('kubectl', 'config', 'use-context', context)

def set_context(context) -> str:
    """
    Seta o contexto selecionado
    """
    try:
        params = set_context_params(context)

        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except Exception as err:
        return "Erro ao executar set_contexts:\n%s" % err


def get_pod_containers_params(namespace: str, pod: str) -> Tuple[str]:
    return ('kubectl', 'get', 'pod', pod, '--namespace', namespace, '-o', 'jsonpath="{.spec.containers[*].name}"')


def get_pod_containers(namespace: str, pod:str) -> str:
    """
    Get containers from pod
    """
    try:
        params = get_pod_containers_params(namespace, pod)
        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except Exception as err:
        return "Erro ao executar get_pod_containers:\nnamespace: %s\npod: %s\n%s" % (namespace, pod, err)


def describe_pod_params(namespace: str, pod:str) -> Tuple[str]:
    return ('kubectl', 'describe', 'pod', pod, '--namespace', namespace)


def describe_pod(namespace: str, pod:str) -> str:
    """
    Describes pod
    """
    try:
        params = describe_pod_params(namespace, pod)
        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except Exception as err:
        return "Erro ao executar describe_pods:\nnamespace: %s\npod: %s\n%s" % (namespace, pod, err)


def check_pod_logs_by_container_params(namespace: str, pod:str, container:str) -> Tuple[str]:
    return('kubectl', 'logs', '--timestamps', '--namespace', namespace, pod, '--container', container)


def check_pod_logs_by_container(namespace: str, pod:str, container: str) -> str:
    """
    Check logs by container
    """
    try:
        params = check_pod_logs_by_container_params(namespace, pod, container)
        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except Exception as err:
        return "Erro ao executar check_pod_logs_by_container:\nnamespace: %s\npod: %s\ncontainer: %s\n%s" % (namespace, pod, container, err)


def switch_ctx(ctx) -> str:
    try:
        params = ('kubectl', 'config', 'use-context', ctx)

        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout.replace('\n', '')
    except:
        return "Erro ao executar switch_ctx com os seguintes parâmetros: %s" % params