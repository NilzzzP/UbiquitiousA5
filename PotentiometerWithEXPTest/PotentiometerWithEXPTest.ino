// Define the pins
#define POT_SHUTTERSPEED 9
#define POT_APERTURE 10
#define BUTTON_PIN 0


float ApertureDialValues[] = {2.0, 2.8, 4.0, 5.6, 8.0, 11.0, 16.0 };
int numAperturePositions = 7; 


int ShutterSpeedDialValues[] = {1000, 500, 250, 125, 60, 30, 15};
int numShutterSpeedPositions = 7; 
//Potentiometer Bounds for each dial
int ShutterSpeedBounds[] = {55, 209, 321, 576, 718, 970, 1024}; 
int ApertureBounds[] = {68, 242, 410, 615, 802, 1000, 1024};


void setup() {
  Serial.begin(9600);
  while (!Serial) { delay(10); }
  
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  Serial.println("Camera Dials Ready! Press the button to read.");
}


void loop() {
  int buttonState = digitalRead(BUTTON_PIN);

  if (buttonState == LOW) {
    
    int rawAperture = analogRead(POT_APERTURE);
    int rawShutterSpeed = analogRead(POT_SHUTTERSPEED);

    int indexAperture = getZoneIndex(rawAperture, ApertureBounds, numAperturePositions);
    int indexShutterSpeed = getZoneIndex(rawShutterSpeed, ShutterSpeedBounds, numShutterSpeedPositions);

    float selectedAperture = ApertureDialValues[indexAperture];
    int selectedShutterSpeed = ShutterSpeedDialValues[indexShutterSpeed];

    Serial.print("(Aperture): f/");
    Serial.print(selectedAperture, 1); // The '1' tells it to print one decimal place
    
    Serial.print("  |(Shutter): 1/");
    Serial.println(selectedShutterSpeed); 

    // Debounce delay
    delay(300); 
  }
}
int getZoneIndex(int rawReading, int boundsArray[], int numZones) {
  for (int i = 0; i < numZones; i++) {
    if (rawReading <= boundsArray[i]) {
      return i;
    }
  }
  return numZones - 1;
}
