import cv2 # -------- Manejo de cámara e imágenes --------
import mediapipe as mp # -------- Modelo de IA para postura --------
import serial # -------- Comunicación con Arduino --------
import time # -------- Esperas y temporización --------
import math # -------- Cálculos trigonométricos --------

# -------- CONFIGURAR PUERTO ARDUINO --------
arduino = serial.Serial('COM5', 9600)
time.sleep(2)

# -------- FUNCION PARA CALCULAR ANGULO --------
def calcular_angulo(a, b, c):
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    cx, cy = c.x, c.y

    angulo = math.degrees( # -------- transforma en angulo --------
        math.atan2(cy - by, cx - bx) -
        math.atan2(ay - by, ax - bx)
    )

    if angulo < 0: # -------- Normalización "Convierte de negativo a positivo en algulos"--------
        angulo += 360

    return angulo

# -------- INICIALIZAR MEDIAPIPE --------
mp_pose = mp.solutions.pose # -------- Entramos al módulo de detección de postura (Detectar el cuerpo)--------
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils # -------- dibujar en pantalla los puntos del cuerpo -------- 

# -------- ABRIR CAMARA --------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# -------- No Abrio la camara Msj --------
if not cap.isOpened():
    print("No se pudo abrir la cámara")
    arduino.write(b'R')  # Estado seguro
    arduino.close()
    exit()

estado_anterior = "" # Crea una variable vacía

try:
    while True: # Bucle infinito principal
        ret, frame = cap.read() #Capturar imagen
        if not ret:
            break
            #Valida si la camara falla
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Convierte la imagen al formato que MediaPipe necesita
        results = pose.process(image) #analiza el cuerpo la IA

        if results.pose_landmarks: #¿Detectó puntos del cuerpo?
            landmarks = results.pose_landmarks.landmark

            # Pierna izquierda
            cadera = landmarks[23]
            rodilla = landmarks[25]
            tobillo = landmarks[27]

            angulo_rodilla = calcular_angulo(cadera, rodilla, tobillo) #Calcula el ángulo de la rodilla

            # -------- LOGICA SENTADO / PARADO --------
            if angulo_rodilla < 160:
                estado = "SENTADO"
            else:
                estado = "PARADO"

            # -------- ENVIAR SOLO SI CAMBIA --------
            if estado != estado_anterior:
                if estado == "SENTADO":
                    arduino.write(b'G')  # Verde
                    print("Enviado: G (SENTADO)") 
                else:
                    arduino.write(b'R')  # Rojo
                    print("Enviado: R (PARADO)")

                estado_anterior = estado #Guarda el estado

            # -------- MOSTRAR EN PANTALLA --------
            cv2.putText(frame,
                        f"{estado} - Angulo: {int(angulo_rodilla)}",
                        (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,255),
                        2)

            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        cv2.imshow("Pose Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'): #cierra ejecucion py
            break

except KeyboardInterrupt:
    print("Interrupción manual detectada") #Detecta si lo detienes manualmente.

finally:
    print("Cerrando sistema - Enviando estado seguro (ROJO)")
    arduino.write(b'R')  # Estado seguro final destruye procesos
    time.sleep(0.5)

    cap.release()
    arduino.close()
    cv2.destroyAllWindows()