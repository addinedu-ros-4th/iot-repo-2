#include <OneWire.h>

#include <Servo.h>

const int WHEIGHT = 14;

Servo servo;

bool servo_is_activated = false;

int count = 0;
int servo_angle = 150;

OneWire ds(2); 

String angle = "0";
String meal_count = "";
String water_level = "0";

String meal = "0";
String light = "0";
String water = "0";

String start_time = "0";
String plan_list = "0";

String order = "";
String response = "";



String sub_string = "";
void setup() {
  
  Serial.begin(9600);
  servo.attach(9);
  servo.write(0);

  pinMode(WHEIGHT, INPUT);


}

float getTemp(){                                   //온도 측정 후 반환하는 함수
  byte data[12];
  byte addr[8];
  if ( !ds.search(addr)) {
    ds.reset_search();
    return -1000;
  }
  if ( OneWire::crc8( addr, 7) != addr[7]) {
    //Serial.println("CRC is not valid!");
    return -1000;
  }
  if ( addr[0] != 0x10 && addr[0] != 0x28) {
    //Serial.print("Device is not recognized");
    return -1000;
  }
  ds.reset();
  ds.select(addr);
  ds.write(0x44,1);                                   
  byte present = ds.reset();
  ds.select(addr);  
  ds.write(0xBE); 
  
  for (int i = 0; i < 9; i++) { 
    data[i] = ds.read();                                                          
  }
  
  ds.reset_search(); 
  byte MSB = data[1];
  byte LSB = data[0];
  float tempRead = ((MSB << 8) | LSB); 
  float TemperatureSum = tempRead / 16; 
  return TemperatureSum;                                                                    
}

void decode_input(String orders) {
  
  meal = orders.substring(0, orders.indexOf(","));
  sub_string = orders.substring(orders.indexOf(",") + meal.length());

  water = sub_string.substring(1, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(",") + water.length());
  
  light = sub_string.substring(1, sub_string.indexOf(", "));
  sub_string = sub_string.substring(sub_string.indexOf(", ") + light.length());

  
  meal_count = sub_string.substring(2, sub_string.indexOf("',"));
  sub_string = sub_string.substring(sub_string.indexOf(",") + meal_count.length() + 1);
  
  
  water_level = sub_string.substring(1, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(",") + water_level.length());
  
  angle = sub_string.substring(1, sub_string.indexOf(", "));
  sub_string = sub_string.substring(sub_string.indexOf(", ") + angle.length());

  start_time = sub_string.substring(1, sub_string.indexOf(","));
  sub_string = sub_string.substring(start_time.length() + 3);

  plan_list = sub_string;
  
  
}

void activate_servo() {
  servo.write(servo_angle);
  delay(2000);
  servo.write(0);
  delay(500);
}


void plan_is_now() {
  unsigned long pretime = millis();
  bool is_now = false;

  sub_string = plan_list.substring(1);
  sub_string = (sub_string.substring(0, sub_string.indexOf("'")));
  String plan = sub_string;

  String sub_string2 = meal_count.substring(0);
  sub_string2 = (sub_string2.substring(0, sub_string2.indexOf("'")));
  String plan_count = sub_string2;

  while (1) {
    plan = (sub_string.substring(0, sub_string.indexOf(",")));
    sub_string = sub_string.substring(sub_string.indexOf(",") + 1);
    
    plan_count = (sub_string2.substring(0, sub_string2.indexOf(",")));
    sub_string2 = sub_string2.substring(sub_string2.indexOf(",") + 1);


    if (2500 >=  abs(plan.toInt() - ((start_time.toInt() + pretime) % 86400000))) {
      is_now = true;
      break;
    }
    else if (plan == sub_string) {
      break;
    }
    
    //Serial.println("{\"plan\" : "+ (String)plan.toInt() + "}" + (String)(start_time.toInt() + pretime));
  }

  if (is_now == true) {
    for (int i = 0; i < plan_count.toInt(); i++){
      activate_servo();
    }
  }

}









void loop() {
  

  count ++;
  response = "{\"waterLevel\" : "+ (String)analogRead(A0) + ", " + "\"temperature\" : "+ (String)getTemp() + ", " + "\"waterQulity\" : "+ (String)analogRead(A2) + "}";
  Serial.println(response);
  
  
   

  if (Serial.available()) {
    order = Serial.readStringUntil('\n');
    decode_input(order);
    
  }
  //decode_input("0, 0, 0, '4,4', 0, 0, 11430000, '11460000,54660000'"); // test_data
    

  if (meal == "1") {
    servo.write(servo_angle);
    servo_is_activated = true;
    count = 0;
    
  }
  else if (servo_is_activated == true && count >= 20){
    servo.write(0);
    servo_is_activated = false;
    meal = "0";
  }
  else {
    plan_is_now();
  }




  if (count >= 1000) {
    count = 0;
  }
    
    
  
  delay(500);
}