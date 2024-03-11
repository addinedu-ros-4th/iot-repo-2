#include <Servo.h>
#define TRIG 3 //sy
#define ECHO 4 //sy 

const int WHEIGHT = 14;

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

  pinMode(WHEIGHT, INPUT);
  
  pinMode(TRIG, OUTPUT); //trig sy 
  pinMode(ECHO, INPUT); //echo sy 


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
  response = "{\"waterLevel\" : "+ (String)analogRead(WHEIGHT) + "}";
  //Serial.println(response);  

  //sy-waterlevel 
  float duration, distance;
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  duration = pulseIn(ECHO, HIGH); //
  distance = ((float)(340 * duration) / 10000) / 2;  // turn into cm 
  Serial.println(distance);
  delay(1000); //-- sy 
  

  // while (Serial.available() > 0) {
  //   order = Serial.readStringUntil('\n');
  //   decode_input(order);
  //   count++;
    
    
  //   if (count % 10 == 0) {
  //     angle = angle.toInt();

  //     for (angle = 0; angle <= 100; angle++) {
  //       servo.write(angle);
  //       delay(5);
  //     }

  //     for (angle = 100; angle = tmp; angle--) {
  //       servo.write(angle);
  //       delay(5);

  //       if (angle == 0) {
  //         break;
  //       }
  //     }

  //     count = 0;
  //   }

    
    
  // }
  delay(500);
}
