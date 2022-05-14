const int holdButtonPin = 3;
const int inputButtonPin = 4;

int counter = 0;
void setup()
{
  pinMode(buttonPin, INPUT);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}


void loop()
{
  int buttonState;
  buttonState = digitalRead(buttonPin);
  
  if (buttonState==HIGH) {
  
  }
}
