#include <Servo.h>

const int WHEIGHT = 14;

Servo servo;
int count = 0;
int servo_angle = 0;

String angle = "0";
String meal_count = "0";
String water_level = "0";

String meal = "0";
String light = "0";
String water = "0";

String order = "";
String response = "";



String sub_string = "";
void setup() {
  
  Serial.begin(9600);
  servo.attach(9);
  servo.write(0);

  pinMode(WHEIGHT, INPUT);


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
  

  
  response = "{\"waterLevel\" : "+ (String)analogRead(A0) + ", " + "\"test_val\" " + ": " + (String)meal + "}";
  Serial.println(response);
  
  
  

  while (Serial.available() > 0) {
    order = Serial.readStringUntil('\n');
    decode_input(order);

    
    servo_angle = 150;
    

    if (meal == "1") {
      servo.write(servo_angle);
      
    }

    
    
  }
  delay(500);
}