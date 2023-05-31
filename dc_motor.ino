#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Adafruit_DCMotor *myMotor_LEFT = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor_RIGHT = AFMS.getMotor(3);

void setup() {
  AFMS.begin();
  Serial.begin(9600);
}
void loop() {
  myMotor_LEFT->setSpeed(255);//255 max
  myMotor_RIGHT->setSpeed(255);
  int incomingData;
  
  if(Serial.available()>0){
    incomingData = Serial.read();
    Serial.println(incomingData);
    if(incomingData == 115){ 
      Serial.println("w");
      myMotor_LEFT->run(FORWARD);
      myMotor_RIGHT->run(BACKWARD);
    }
    if(incomingData ==100){
      Serial.println("a");
      myMotor_LEFT->run(FORWARD);
      myMotor_RIGHT->run(FORWARD);
    }
    if(incomingData == 97){
      Serial.println("s");
      myMotor_LEFT->run(BACKWARD);
      myMotor_RIGHT->run(BACKWARD);
    }
    if(incomingData == 119){ 
      Serial.println("d");
      myMotor_LEFT->run(BACKWARD);
      myMotor_RIGHT->run(FORWARD);
    }
    if(incomingData == 104){
      myMotor_LEFT->run(RELEASE);
      myMotor_RIGHT->run(RELEASE);
    }
  }

}
