#include <Servo.h> 

Servo servo;
int count = 0;


String angle = "";
String meal_count = "";
String water_level = "";

String meal = "";
String light = "";
String water = "";

String meal_time = "";

String meal_list[10];
int meal_counting = 0; 
unsigned long millisTime = millis();

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
  sub_string = sub_string.substring(sub_string.indexOf(",") + angle.length());

  meal_time = sub_string.substring(sub_string.lastIndexOf(",") + 1);
  Serial.println(orders);
}


void feed() {
  for (Angle = 0; Angle <= 120; Angle++) {
    servo.write(Angle);
    delay(3);
  }
  for (Angle = 120; Angle <=120; Angle--) {
    servo.write(Angle);
    delay(3);

    if (Angle == 0) {
    return;
    }
  }       
}


void feedAction() {

  String new_data = meal + "," + meal_count + "," + meal_time;
  
  meal_list[meal_counting] = new_data;
  meal_counting++;

  for (int i = 0; i < meal_counting; i++) {
    String current_meal = meal_list[i].substring(0, meal_list[i].indexOf(","));
    String current_meal_count = meal_list[i].substring(meal_list[i].indexOf(",") + 1, meal_list[i].lastIndexOf(","));
    String current_meal_time = meal_list[i].substring(meal_list[i].lastIndexOf(",") + 1);
    
    if (current_meal == "1") {
      feed();

      for (int j = i; j < meal_counting - 1; j++) {
        meal_list[j] = meal_list[j + 1];
      }
      meal_counting--;
      i--; 
    }

    if (current_meal_time == millisTime) {
      if (current_meal == "1") {
        if (current_meal_count.toInt() > 0){
          for (int x = 0; x < current_meal_count.toInt(); x++){
            feed(); 
          }

          for (int j = i; j < meal_counting - 1; j++) {
            meal_list[j] = meal_list[j + 1];
          }
          meal_counting--;
          i--; 

        }
      }
    }
  }
}


void loop() {
  
  count++;
  response = "{\"waterLevel\" : "+ (String)analogRead(A0) + "}";
  // Serial.println(response);
  
  while (Serial.available() > 0) {
    order = Serial.readStringUntil('\n');
    decode_input(order);
    count++;

    feedAction();
    
    count = 0;
  } 

  delay(100);

}