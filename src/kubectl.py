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
        return ('kubectl', 'get', 'pods', '-n', namespace)


def get_pods(namespace: str) -> str:
    """
    Devolve os pods daquele namespace
    """
    try:
        params = get_pods_params(namespace)
        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except Exception as err:
        return "Erro ao executar get_pods:\n%s" % err


def get_all_ctx() -> str:
    os.system('clear')
    try:
        params = ('kubectl', 'config', 'get-contexts')

        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        linhas = result.stdout.split('\n')
        dicio = {}
        for idx, linha in enumerate(linhas[1:]):
            l = linha.replace('*', '').strip().split(' ')[0]
            if len(l):
                print("%d. %s" % (idx+1, l))
                dicio[idx+1] = l

        while True:
            idx = input("\nSelecione um contexto: ")

            try:
                sel = dicio[int(idx)]
                switch_ctx(sel)
                break
            except KeyError:
                print("Tente novamente...")

        
        os.system('clear')

    except:
        print("Erro ao executar subprocess.run com os seguintes parâmetros: %s" % params)


def switch_ctx(ctx) -> str:
    try:
        params = ('kubectl', 'config', 'use-context', ctx)

        result = subprocess.run(params, stdout=subprocess.PIPE, universal_newlines=True)
        return result.stdout.replace('\n', '')
    except:
        return "Erro ao executar switch_ctx com os seguintes parâmetros: %s" % params