from pynput import keyboard
    
def on_press(key):
        if key == keyboard.Key.up:
            print('PRESSED')
        if key == keyboard.Key.esc:
            listener.stop()
    
    
with keyboard.Listener(on_press=on_press) as listener:
        listener.join()