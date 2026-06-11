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
    
    // 1. Read the raw 0-1023 values
    int rawAperture = analogRead(POT_APERTURE);
    int rawShutterSpeed = analogRead(POT_SHUTTERSPEED);

    // 2. The Math Magic: Convert 0-1023 into an Array Index (0 to 6, or 0 to 5)
    // This chops the pot's rotation into perfectly equal slices.
    int indexAperture = getZoneIndex(rawAperture, ApertureBounds, numAperturePositions);
    int indexShutterSpeed = getZoneIndex(rawShutterSpeed, ShutterSpeedBounds, numShutterSpeedPositions);

    // 3. Pull the specific number out of our arrays based on the zone
    float selectedAperture = ApertureDialValues[indexAperture];
    int selectedShutterSpeed = ShutterSpeedDialValues[indexShutterSpeed];

    // 4. Print the snapped values!
    Serial.print("Left Dial (Aperture): f/");
    Serial.print(selectedAperture, 1); // The '1' tells it to print one decimal place
    
    Serial.print("  |  Right Dial (Shutter): 1/");
    Serial.println(selectedShutterSpeed); 

    // Debounce delay
    delay(300); 
  }
}
int getZoneIndex(int rawReading, int boundsArray[], int numZones) {
  for (int i = 0; i < numZones; i++) {
    if (rawReading <= boundsArray[i]) {
      return i; // Found the zone!
    }
  }
  return numZones - 1; // Fallback to the last zone just in case
}