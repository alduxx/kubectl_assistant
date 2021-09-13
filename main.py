import ast
import src.globals as globals

from getkey import getkey, keys
from rich.live import Live
from time import sleep

from src.kubectl import get_current_context, get_first_fav_namespace
from src.layout import main_layout, update_pods, show_contexts, update_context, message, select_pod


if __name__ == "__main__":
    globals.initialize()

    context =  get_current_context()
    namespace = get_first_fav_namespace() 
    pod = None 
    
    layout = main_layout(context, namespace, pod)

    with Live(layout, refresh_per_second=10, screen=True, redirect_stdout = False) as live:
        while True:
            key = getkey()
            if key == keys.F1:
                show_contexts()
            elif key == keys.F2:
                print("F2")
            elif key == keys.F3:
                update_pods(namespace)
            elif key == keys.ESC:
                live.console.print("breaking")
                print("ip breaking")
                break
            else:  
                if len(globals._func_waiting_key) == 0:
                    pass
                else:
                    #try:
                    _dict_ = ast.literal_eval(globals._dict)
                    _value = _dict_[int(key)].strip()
                    _func = globals._func_waiting_key.replace("_p_", _value)
                    eval(_func)
                    globals._func_waiting_key = "" # resets waiting function
                    #except Exception as err:
                        #return "Erro ao executar get_pods:\n%s" % err
                        #message(err)
                    #    pass
                #break
                #pass # Handle text characters

            
            sleep(0.1)