#include <Servo.h>

Servo servo;
int count = 0;


String angle = "";
String meal_count = "";
String water_level = "";

String meal = "";
String light = "";
String water = "";

String order = "";
String response = "";



String sub_string = "";
void setup() {
  
  Serial.begin(9600);
  servo.attach(9);
  servo.write(0);


}


void decode_input(String orders) {
  
  meal = orders.substring(0, orders.indexOf(","));
  sub_string = orders.substring(orders.indexOf(",") + meal.length());

  water = sub_string.substring(0, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(",") + water.length());
  
  light = sub_string.substring(0, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(",") + light.length());

  
  meal_count = sub_string.substring(0, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(",") + meal_count.length());
  
  water_level = sub_string.substring(0, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(",") + water_level.length());
  
  angle = sub_string.substring(0, sub_string.indexOf(","));
  
}



void loop() {
  
  count++;
  response = "{\"waterLevel\" : "+ (String)analogRead(A0) + "}";
  Serial.println(response);
  
  
  

  while (Serial.available() > 0) {
    order = Serial.readStringUntil('\n');
    decode_input(order);
    count++;
    
    
    if (count % 10 == 0) {
      angle = angle.toInt();

      for (angle = 0; angle <= 100; angle++) {
        servo.write(angle);
        delay(5);
      }

      for (angle = 100; angle = tmp; angle--) {
        servo.write(angle);
        delay(5);

        if (angle == 0) {
          break;
        }
      }

      count = 0;
    }

    
    
  }
  delay(100);
}