from rich.live import Live
from time import sleep

from getkey import getkey, keys

from src.kubectl import get_current_context, get_first_fav_namespace

from src.layout import main_layout, update_pods

if __name__ == "__main__":
    context =  get_current_context()
    namespace = get_first_fav_namespace() 
    pod = None 
    
    layout = main_layout(context, namespace, pod)

    with Live(layout, refresh_per_second=10, screen=True):
        while True:
            key = getkey()
            if key == keys.F1:
                print("F1")
            if key == keys.F2:
                print("F2")
            if key == keys.F3:
                # update_pods(get_pods(namespace))
                update_pods(namespace)
            if key == keys.ESC:
                break
            else:  
                pass # Handle text characters

            # update_contents(key)
            
            sleep(0.1)


"""

        cmd = console.input("Digite uma opção: ")

        if cmd == 'q':
            break
        elif cmd == '1':
            get_all_ctx()
        elif cmd == '2':
            ns_select()
        elif cmd == '3':
            namespace = input("Digite o nome do namespace: ")
            print(get_pods(namespace))
        else:
            os.system('clear')
            print("# Opção não encontrada. Tente novamente.")
            """