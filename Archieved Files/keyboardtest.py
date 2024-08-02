from pynput import keyboard
    
def on_press(key):
        if str(key) == "'f'":
            print(str(key))
        if str(key) == 'g':
            listener.stop()
    
    
with keyboard.Listener(on_press=on_press) as listener:
        listener.join()