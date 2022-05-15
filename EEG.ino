const int holdButtonPin = 3;
const int inputButtonPin = 4;

bool pressed = False;
void setup()
{
  Serial.begin(9600);
  pinMode(holdButtonPin, INPUT);
  pinMode(inputButtonPin, INPUT);
}


void loop()
{
  int buttonState;
  int buttonHold;
  buttonState = digitalRead(holdButtonPin);
  
  if (buttonState==HIGH) {
    buttonHold = digitalRead(inputButtonPin);
    if (buttonHold == HIGH && pressed == False) {
      pressed = True;
      Serial.println("LOW");
    }
    if (buttonHold == LOW && pressed == True) {
      pressed = False;
      Serial.println("HIGH");
    }
  }
}
