#include <SPI.h>
#include <WiFi.h>
#include <WiFiNINA.h>
#include <Adafruit_NeoPixel.h>

const int nleds = 30;
int brightness = 30;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(nleds, 15, NEO_GRB + NEO_KHZ800);  // Arduino Pin 3 Data Output
int nextLed;
bool leds[nleds];
char colors[nleds];

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = "PGI_Acceso";        // your network SSID (name)
char pass[] = "usuario123";    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;   // your network key index number (needed only for WEP)

int status = WL_IDLE_STATUS;
WiFiServer server(8080);

void setup() {
  Serial.begin(9600);
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
  
  IPAddress ip(192, 168, 0, 125);
  WiFi.config(ip);
  
  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  server.begin();                           // start the web server on port 80
  digitalWrite(LEDG, HIGH);
  digitalWrite(LEDB, LOW);
  for (int i = 0; i < nleds; i++){
    colors[i] = 'n';
  }
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
    Serial.println(currentLine);
    if (currentLine.startsWith("r") || currentLine.startsWith("g") || currentLine.startsWith("c") || currentLine.startsWith("y") || currentLine.startsWith("m") || currentLine.startsWith("w")|| currentLine.startsWith("o")){
      nextLed = currentLine.substring(1).toInt();
      leds[nextLed] = true;
      if (0 <= nextLed && nextLed <= nleds){
        colors[nextLed] = currentLine[0];
      } else if (nextLed == 99){
        for (int i = 0; i < nleds; i++){
          colors[i] = currentLine[0];
        }
      } else if (nextLed == -1){
        for (int i = 0; i < nleds; i++){
          colors[i] = 'n';
        }
      } 
    } else {
      nextLed = currentLine.substring(2,4).toInt();
      leds[nextLed] = false;
    }
    
    if (nextLed == -1){
      for (int i = 0; i < nleds; i++){
        leds[i] = false;
      }
    } else if (nextLed == 99){
      for (int i = 0; i < nleds; i++){
        leds[i] = true;
      }
    }

    for (int i = 0; i < nleds; i++) {
      if (leds[i] && colors[i] == 'r'){
        strip.setPixelColor(i, 255,   0,   0);  // Red
      } else if (leds[i] && colors[i] == 'g'){
        strip.setPixelColor(i,   0, 255,   0);  // Green
      } else if (leds[i] && colors[i] == 'c'){
        strip.setPixelColor(i,   0, 255, 255);  // Cyan
      } else if (leds[i] && colors[i] == 'y'){
        strip.setPixelColor(i, 255, 255,   0);  // Yellow
      } else if (leds[i] && colors[i] == 'm'){
        strip.setPixelColor(i, 255,   0, 255);  // Magenta
      } else if (leds[i] && colors[i] == 'o'){
        strip.setPixelColor(i, 252,  98,   0);  // Orange
      } else if (leds[i] && colors[i] == 'w'){
        strip.setPixelColor(i, 255, 255, 255);  // White
      } else {
        strip.setPixelColor(i,  0,    0,   0);  // Off
      }
      strip.show();
    }
  }
}
