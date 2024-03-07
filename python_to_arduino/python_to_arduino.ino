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

int Angle = 0;



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
    
    
    if (meal == 1) {
      
      for (Angle = 0; Angle <= 100; Angle++) {
        servo.write(Angle);
      

        // for (; Angle <= 100; Angle--) {
        //   servo.write(Angle);
        //   delay(5);

        //   if (Angle == 0) {
        //     break;
        //   }
        // }
      }

      count = 0;
    }

    
    
  }
  delay(10);
}