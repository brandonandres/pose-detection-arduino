char estado;

void setup() {
  Serial.begin(9600); //Inicia la comunicación serial.
  pinMode(8, OUTPUT);  // DONDE ESTA EL LED ROJO
  pinMode(9, OUTPUT);  // DONDE ESTA EL LED VERDE
}

void loop() {
  if (Serial.available() > 0) { //¿Llegó algún dato desde el computador?
    estado = Serial.read(); //Lee la letra que envió Python. Y la guarda

    if (estado == 'R') {
      digitalWrite(8, HIGH);
      digitalWrite(9, LOW);
    }

    if (estado == 'G') {
      digitalWrite(9, HIGH);
      digitalWrite(8, LOW);
    }
  }
}