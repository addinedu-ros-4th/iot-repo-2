#include <OneWire.h>

#include <Servo.h>

const int WLEVELECHO = 4;
const int WLEVELTRIG = 3;
const int WQUALITY = 15;
const int WTEMP = 16;

const int pumpPin = 12;
const int LIGHT = 6;

const int height = 30; 


Servo servo;

bool servo_is_activated = false;
bool pump_is_activated = false;
bool light_is_on = false;

int count = 0;
int servo_angle = 150;
int water_count = 0;

OneWire ds(2); 

String meal_count = ",0";
String meal = "0";

String properLevel = "24";
String properTemp = "25";
String properQuality = "5";

String start_time = "0";
String plan_list = ",0";

String order = "";
String response = "";

String sub_string = "";
void setup() {
  
  Serial.begin(9600);
  servo.attach(9);
  servo.write(0);

  pinMode(WQUALITY, INPUT);
  pinMode(WLEVELTRIG, OUTPUT);
  pinMode(WLEVELECHO, INPUT);
  pinMode(WTEMP, INPUT);
  pinMode(LIGHT, OUTPUT);
  digitalWrite(LIGHT, LOW);

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
  
  properLevel = orders.substring(0, orders.indexOf(","));
  sub_string = orders.substring(orders.indexOf(",") + 1);

  
  

  properTemp = sub_string.substring(0, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(",") + 1);
  
  
  properQuality = sub_string.substring(0, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(","));

  
  meal_count = sub_string.substring(3, sub_string.indexOf("',"));
  sub_string = sub_string.substring(sub_string.indexOf("',") + 2);


  meal = sub_string.substring(1, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(",") + 1);

 

  start_time = sub_string.substring(1, sub_string.indexOf(","));
  sub_string = sub_string.substring(sub_string.indexOf(",") + 1);

 

  plan_list = sub_string.substring(2);
  plan_list = plan_list.substring(0, plan_list.indexOf("'"));
  
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

  sub_string = plan_list;
  String plan = sub_string;

  String sub_string2 = meal_count;
  String plan_count = sub_string2;
  
  while (1) {
    plan = (sub_string.substring(0, sub_string.indexOf(",")));
    sub_string = sub_string.substring(sub_string.indexOf(",") + 1);
    
    plan_count = (sub_string2.substring(0, sub_string2.indexOf(",")));
    sub_string2 = sub_string2.substring(sub_string2.indexOf(",") + 1);


    if (3000 >=  abs(plan.toInt() - ((start_time.toInt() + pretime) % 86400000))) {
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
  water_count++;

  

  float duration, distance;
  digitalWrite(WLEVELTRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(WLEVELTRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(WLEVELTRIG, LOW);
  duration = pulseIn(WLEVELECHO, HIGH);
  distance = ((float)(340 * duration) / 10000) / 2; //distance : sensor~surface distance -> water level = bowl height - distance 
  float level = height - distance; 

  float temperature = getTemp();
   

  if (Serial.available()) {
    order = Serial.readStringUntil('\n');
    decode_input(order);
    
  }
  //decode_input("0, 0, 0, '4,4', 0, 0, 11430000, '11460000,54660000'"); // test_data


//water level pumping 
  if (level < properLevel.toFloat()) {
    analogWrite(pumpPin, 150);
    pump_is_activated = true;

    
    //Serial.println("water on");
  }
  else {
    analogWrite(pumpPin, 0);
    //Serial.println("water off");
    pump_is_activated = false;
  } 

  if (temperature > properTemp.toFloat()){
    digitalWrite(LIGHT, HIGH);
    light_is_on = true;
  }
  else if (temperature <= properTemp.toFloat()){
    digitalWrite(LIGHT, LOW);
    light_is_on = false;
  }


  if (meal == "1") {
    servo.write(servo_angle);
    servo_is_activated = true;
    count = 0;
    meal = "0";
    
  }
  else if (servo_is_activated == true && count >= 2){
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
  if (water_count >= 500) {
    water_count = 0;
  }

  response =  "{\"waterLevel\" : " + (String)level + ", " + 
  "\"waterTemperature\" : " + (String)temperature + ", " + 
  "\"waterQuality\" : "+ (String)analogRead(WQUALITY) + ", " +
  "\"light\" : "+ (String)light_is_on + ", " +
  "\"properTemp\" : "+ properTemp + ", " +
  "\"properQuality\" : "+ properQuality + ", " +
  "\"servo\" : "+ (String)servo_is_activated + ", " +
  "\"pump\" : "+ (String)pump_is_activated + "}"; //", " +
  // "\"meal_count\" : "+ (String)meal_count + ", " +
  // "\"meal\" : "+ (String)meal + ", " +
  // "\"start_time\" : "+ (String)start_time + ", " +
  // "\"plan_list\" : "+ (String)plan_list + "}";

  Serial.println(response);
    
  
  delay(500);
}
