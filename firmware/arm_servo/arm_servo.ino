#include <Servo.h>

const uint8_t NUM_SERVOS = 4;
const uint8_t SERVO_PINS[NUM_SERVOS] = {3, 5, 6, 9};
Servo servos[NUM_SERVOS];

char buf[32];
uint8_t len = 0;

void setup() {
  Serial.begin(115200);
  for (uint8_t i = 0; i < NUM_SERVOS; i++) {
    servos[i].attach(SERVO_PINS[i]);
    servos[i].write(90);
  }
}

// Parses "a1,a2,a3,a4" (degrees) and moves the servos
void applyLine(char *line) {
  int vals[NUM_SERVOS];
  uint8_t n = 0;
  char *tok = strtok(line, ",");
  while (tok != NULL && n < NUM_SERVOS) {
    vals[n++] = atoi(tok);
    tok = strtok(NULL, ",");
  }
  if (n != NUM_SERVOS) return;  // ignore malformed lines
  for (uint8_t i = 0; i < NUM_SERVOS; i++) {
    servos[i].write(constrain(vals[i], 0, 180));
  }
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      buf[len] = 0;
      applyLine(buf);
      len = 0;
    } else if (c != '\r' && len < sizeof(buf) - 1) {
      buf[len++] = c;
    }
  }
}
