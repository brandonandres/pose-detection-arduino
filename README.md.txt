# Sistema de Detección de Postura con MediaPipe y Arduino

## Descripción del Proyecto

Este proyecto implementa un sistema de visión artificial que detecta si una persona está SENTADA o PARADA utilizando inteligencia artificial con MediaPipe.  

El sistema calcula el ángulo de la rodilla en tiempo real usando la cámara del computador y, dependiendo del resultado, envía una señal al Arduino para encender un LED rojo o verde.

---

## Funcionamiento General

El sistema está compuesto por dos partes:

1. Procesamiento en Python (Inteligencia Artificial)
2. Control físico con Arduino (Actuador)

Flujo del sistema:

Cámara → MediaPipe → Cálculo de ángulo → Determinación de postura → Comunicación Serial → Arduino → LED

---

## Parte 1: Python + MediaPipe

### Librerías utilizadas

- OpenCV
- MediaPipe
- PySerial
- Math
- Time

### ¿Qué hace el programa?

1. Abre la cámara.
2. Detecta los puntos del cuerpo usando MediaPipe.
3. Extrae los puntos de:
   - Cadera
   - Rodilla
   - Tobillo
4. Calcula el ángulo de la rodilla.
5. Determina:
   - Ángulo < 160° → SENTADO
   - Ángulo ≥ 160° → PARADO
6. Envía por puerto serial:
   - 'G' → Sentado
   - 'R' → Parado

---

## Parte 2: Arduino

El Arduino recibe los datos por comunicación serial a 9600 baudios.

### Funcionamiento:

- Si recibe 'R' → Enciende LED rojo
- Si recibe 'G' → Enciende LED verde

El Arduino actúa como sistema de salida física del análisis realizado en Python.

---

## Requisitos

### Software

- Python 3.x
- Arduino IDE
- Librerías:
  pip install opencv-python
  pip install mediapipe
  pip install pyserial

### Hardware

- Arduino Uno
- 2 LEDs (Rojo y Verde)
- Resistencias 220Ω
- Protoboard
- Cable USB

---

## Comunicación Serial

Velocidad utilizada: 9600 baudios  
Puerto configurado en Python: COM5 (puede variar según el equipo)

---

## Seguridad del Sistema

El sistema envía un estado seguro (Rojo) cuando:

- No se detecta la cámara.
- Se cierra el programa.
- Ocurre una interrupción manual.

---

## Conclusión

Este proyecto integra visión artificial e interacción hardware, demostrando la aplicación práctica de inteligencia artificial en sistemas físicos en tiempo real.

Python actúa como sistema de procesamiento inteligente y Arduino como sistema actuador.

---

## Autor

Brandon Andrés León Caro - Samuel Rojas