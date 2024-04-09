#include <Arduino.h>
// const byte ledPin = 13;
// const byte power = 4;
const byte interruptPin = 2;
const byte output_pin = 6; 
const float EncoderResolution = 360.0; //2048;
volatile byte state = LOW;
volatile byte endcoder_state = LOW;
volatile unsigned long EncoderCount =0;
float Revolutions = 0.000000; 
float lastTick; 
float currentTick;
float RPM;
const double reference_rpm = 300;//800;
float error = 0;
float error_old = 0;
const float kp = 0.8;
const float kd = 0.001;



void Encoder() {
  EncoderCount++; 
}

void setup() {
  Serial.begin(9600);
  // pinMode(ledPin, OUTPUT);
  // pinMode(power, OUTPUT); 
  pinMode(interruptPin, INPUT_PULLUP);
  pinMode(output_pin, OUTPUT);
  // digitalWrite(power, LOW); 
  attachInterrupt(digitalPinToInterrupt(interruptPin), Encoder, RISING);
}

void loop() {
  long T_start = millis();
  unsigned long Count_Start = EncoderCount;
  //Serial.print("Count Start: "); Serial.println(Count_Start);
  delay(95);
  //Serial.print("Encoder Count: "); Serial.println(EncoderCount);
  long T_End = millis();
  float Diff = ((float)EncoderCount-Count_Start)/EncoderResolution; //convert to revolutions
  //Serial.print("diff: "); Serial.println(Diff);
  
  float Time = (T_End-T_start)/1000.0; //convert to seconds
  //Serial.print("Time: " ); Serial.println(Time);
  float RPM = ((float)Diff/Time)*60.0; //convert rps to rpm
  //Serial.print("RPM: " ); Serial.println(RPM);
  error = RPM - reference_rpm;
  float P = kp * error;
  float D = kd * (error - error_old/Time);
  error_old = error;
  int Vwm =  int(P + D);
  //Vwm = constrain(Vwm, 0, 255);
  if (Vwm > 0){
    if (Vwm > 255){
      Vwm = 255;
    }
  }
  else if (Vwm < 0){
    Vwm = 0; 
  }
  Serial.print("RPM: ");Serial.print(RPM,4);Serial.print("  Vwm: ");Serial.println(Vwm,4);
  analogWrite(output_pin, Vwm);
}
