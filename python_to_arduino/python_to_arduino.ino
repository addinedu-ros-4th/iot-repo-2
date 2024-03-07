#include <Servo.h>
Servo servo;
int angle = 0;
int count = 0;
String response = "";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo.attach(9);
  servo.write(0);


}

void loop() {
  // put your main code here, to run repeatedly:
  count++;
  response = "{\"waterLevel\" : "+ (String)analogRead(A0) + "}";
  Serial.println(response);
  while (Serial.available() > 0) {
    count++;
    
    String input_str = Serial.readStringUntil('\n');
    float tmp = input_str.toFloat();
    if (count % 1000 == 0) {
      servo.write(tmp);
    }
    
  }
  delay(100);
}