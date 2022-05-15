const int holdButtonPin = 3;
const int inputButtonPin = 4;

bool pressed = False;
bool held = False;
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
    if (held==False) {
      held = True
      Serial.println("START");
    }
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
  if (buttonState==LOW && held==True) {
    Serial.println("END");
  }
}
