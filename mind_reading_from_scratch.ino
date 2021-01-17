int sensorValue;
int sensorValue_o;
int sensorValue_t;
int voltage_filter;
int prev_z;
int prev_o;
int prev_t;

bool gorl(int first, int prev) {
  if (first > prev) {
    return true;
  } else {
    return false;
  }
}

int find_frequency(int sVz, int z) {
  bool freq = gorl(sVz, z);
  return 1;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  prev_z = analogRead(A0);
  prev_o = analogRead(A2);
  prev_t = analogRead(A4);
}

void loop() {
  // put your main code here, to run repeatedly:
  sensorValue = analogRead(A0);
  sensorValue_o = analogRead(A2);
  sensorValue_t = analogRead(A4);
  voltage_filter = 5;
  if (sensorValue > voltage_filter) {
    sensorValue -= voltage_filter;
  }
  else {
    sensorValue = 0;
  }
  if (sensorValue_o > voltage_filter) {
    sensorValue_o -= voltage_filter;
  }
  else {
    sensorValue_o = 0;
  }
  if (sensorValue_t > voltage_filter) {
    sensorValue_t -= voltage_filter;
  }
  else {
    sensorValue_t = 0;
  }
  Serial.print(sensorValue);
  Serial.print(",");
  Serial.print(sensorValue_o);
  Serial.print(",");
  Serial.print(sensorValue_t);
  Serial.println(";");
  int freq_z = find_frequency(sensorValue, prev_z);
  int freq_o = find_frequency(sensorValue_o, prev_o);
  int freq_t = find_frequency(sensorValue_t, prev_t);
}
