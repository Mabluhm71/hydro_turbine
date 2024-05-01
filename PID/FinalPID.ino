#include <Arduino.h>
// const byte ledPin = 13;
// const byte power = 4;
const byte interruptPin = 2;
const byte output_pin = 6; 
const float EncoderResolution = 2048.0; //2048;
volatile byte state = LOW;
volatile byte endcoder_state = LOW;
volatile unsigned long EncoderCount =0;
float Revolutions = 0.000000; 
float lastTick; 
float currentTick;
float instant_RPM;
float running_average_RPM = 0;
const double reference_RPM = 100;
float error = 0;
float error_old = 0;
float kp = 0.8;
float kd = 0.001;
float old_count = 0;
const double Encoder_Resolution = 2048; 
const double gearbox_ratio = 5;
float diff;
int Vwm = 0; 



void Encoder() {
  EncoderCount++; 
}

void setup() {
  Serial.begin(9600);
  // pinMode(ledPin, OUTPUT);
  // pinMode(power, OUTPUT); 
  pinMode(interruptPin, INPUT);
  pinMode(output_pin, OUTPUT);
  // digitalWrite(power, LOW); 
  attachInterrupt(digitalPinToInterrupt(interruptPin), Encoder, RISING);
}

void loop() {
  if (Serial.available() > 0) {
    int inByte = Serial.read();

    switch (inByte)
    {
    case '1':
      kp = kp + 0.05;
      Serial.print('kp = ');Serial.println(kp);
      break;

    case '2':
      
      if (kp > 0.05) {
        kp = kp - 0.05;
        Serial.print('kp = ');Serial.println(kp);
      } else {
        Serial.print("kp is below 0.05 can't go any lower");
      }
      break;

    case '3':
      kd = kd + 0.001;
      Serial.print('kd = ');Serial.println(kd);
      break;

    case '4':
      if (kd > 0.001) {
        kd = kd - 0.001;
        Serial.print('kd = ');Serial.println(kd);
      } else {
        Serial.print("kd is below 0.001 can't go any lower");
      }
      break;

    case '5':
      Serial.print('The current Kp and Kd values are ') ;
      Serial.print('kp = ');Serial.print(kp);
      Serial.print(', kd = ');Serial.println(kd);

      break;
    default:
      break;
    }
  } 


  float T_Start = millis();
  old_count = EncoderCount;
  delay(2000);
  float T_End = millis();
  diff = EncoderCount - old_count;
  float Time = (T_End-T_Start)/1000.0; //convert to seconds
  float Gen_RPM = ((diff/((T_End - T_Start)/1000))/Encoder_Resolution) *60 * gearbox_ratio;
  if (Gen_RPM < 1){
    Gen_RPM = 0;  
  } 

  error = Gen_RPM - reference_RPM;
  float P = kp * error;
  float D = kd * (error - error_old/Time);
  error_old = error;
  int temp =  int(P + D);
  if (temp > 255){
    Vwm = 255;
  } else if (temp < 0){
    Vwm = 0;
  } else {
    Vwm = temp; 
  }
  Serial.print("RPM: ");Serial.print(Gen_RPM,4);Serial.print("  Vwm: ");Serial.println(Vwm);
  analogWrite(output_pin, Vwm);
}