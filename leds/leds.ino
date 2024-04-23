/* Prueba de tiras LED inteligentes WS2812B / WS2812
by: www.elprofegarcia.com
Debe instalar la libreria "Adafruit_NeoPixel.h" para que funcione el programa
Conexiones:
ARDUINO   TIRA LED
  5V        +5V ROJO
  GND       GND BLANCO
  3         Din Verde
*/
#include <Adafruit_NeoPixel.h>  // importa libreria, debe indtalarla previamente

const int nleds = 30;   // Numero de LEDs a Probar
int retardo = 5;  // más alto mas lenta la secuencia
int brillo = 30;  // Brillo del LED
Adafruit_NeoPixel tira = Adafruit_NeoPixel(nleds, 3, NEO_GRB + NEO_KHZ800);  // Pin 3 del Arduino es salida de datos
int nextLed = -1;
int prevLed;
bool leds[nleds];

void setup() {
  Serial.begin(9600);
  tira.begin();  // inicializacion de la tira
  tira.setBrightness(brillo);  // Brillo de los LEDs
  tira.show();
}

void loop() {
  if (Serial.available() > 0){
    nextLed = Serial.parseInt();
    if (0 <= nextLed && nextLed < nleds){
      leds[nextLed] = !leds[nextLed];
    } else if (nextLed == 1000){
      for (int i = 0; i < nleds; i++){
        leds[i] = false;
      }
    } else if (nextLed == 999){
      for (int i = 0; i < nleds; i++){
        leds[i] = true;
      }
    }
  }

  for (int i = 0; i < nleds; i++) {
    if (leds[i]){
      tira.setPixelColor(i, 255, 255, 255);  // Blanco
    } else {
      tira.setPixelColor(i, 0, 0, 0);  // Apagado
    }
    tira.show();
  }
}
