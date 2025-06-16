from flask import Flask, request, jsonify
import pywhatkit
import pyautogui
import time

app = Flask(__name__)

@app.route('/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    numeros = data["numeros"]
    mensaje = data["mensaje"]
    wait_time = data.get("wait_time", 20)

    for numero in numeros:
        try:
            pywhatkit.sendwhatmsg_instantly(f"+51{numero}", mensaje, wait_time=wait_time)
            time.sleep(5)
            pyautogui.hotkey('ctrl','w')  # Cierra la pestaña
            pyautogui.press('enter')      # Confirma si aparece alerta
            pyautogui.hotkey('ctrl','r')  # Refresca
        except Exception as e:
            print(f"Error con {numero}: {e}")
    
    return jsonify({"status": "ok", "mensaje": "Mensajes enviados desde la PC"})

if __name__ == '__main__':
    app.run(port=5000)