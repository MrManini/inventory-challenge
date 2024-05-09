#include <SPI.h>
#include <WiFi.h>
#include <WiFiNINA.h>
#include <Adafruit_NeoPixel.h>

const int nleds = 30;
int brightness = 30;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(nleds, 3, NEO_GRB + NEO_KHZ800);  // Arduino Pin 3 Data Output
int nextLed = -1;
int prevLed;
bool leds[nleds];

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = "";        // your network SSID (name)
char pass[] = "";    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;                 // your network key index number (needed only for WEP)

int status = WL_IDLE_STATUS;
WiFiServer server(80);

void setup() {
  strip.begin();
  strip.setBrightness(brightness);
  strip.show();
  
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);

  digitalWrite(LEDR, LOW);
  digitalWrite(LEDG, LOW);
  digitalWrite(LEDB, HIGH);

  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    digitalWrite(LEDR, HIGH);
    while (true);
  }

  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  server.begin();                           // start the web server on port 80
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, LOW);
}


void loop() {
  WiFiClient client = server.available();   // listen for incoming clients
  digitalWrite(LEDB, LOW);
  if (client) {                             // if you get a client,
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        digitalWrite(LEDB, HIGH);
        if (c != '\r'){
          currentLine += c;
        }
      }
    }
    // close the connection:
    client.stop();
    nextLed = currentLine.toInt();
    if (0 <= nextLed && nextLed < nleds){
      leds[nextLed] = !leds[nextLed];
    } else if (nextLed == -1){
      for (int i = 0; i < nleds; i++){
        leds[i] = false;
      }
    } else if (nextLed == 99){
      for (int i = 0; i < nleds; i++){
        leds[i] = true;
      }
    }
    for (int i = 0; i < nleds; i++) {
      if (leds[i]){
        strip.setPixelColor(i, 255, 255, 255);  // White
      } else {
        strip.setPixelColor(i, 0, 0, 0);  // Off
      }
      strip.show();
    }
  }
}