#include <Arduino.h>
// const byte ledPin = 13;
// const byte power = 4;
const byte interruptPin = 2;
const byte output_pin = 6; 
const int EncoderResolution = 2048;
volatile byte state = LOW;
volatile byte endcoder_state = LOW;
volatile unsigned long EncoderCount =0;
float Revolutions = 0.000000; 
float lastTick; 
float currentTick;
float RPM;
const double reference_rpm = 800;
float error = 0;
float error_old = 0;
const double kp = 0.8;
const double kd = 0.001;


void Encoder() {
  EncoderCount++; 
}

void setup() {
  Serial.begin(9600);
  // pinMode(ledPin, OUTPUT);
  // pinMode(power, OUTPUT); 
  pinMode(interruptPin, INPUT_PULLUP);
  // digitalWrite(power, LOW); 
  attachInterrupt(digitalPinToInterrupt(interruptPin), Encoder, RISING);
}

void loop() {
  long T_start = millis();
  unsigned long Count_Start = EncoderCount;
  delay(4000);
  long T_End = millis();
  int Diff = (EncoderCount-Count_Start);
  long Time = T_End-T_start;
  float RPM = (float)Diff/Time;
  Serial.print("RPM: ");Serial.print(RPM,4);Serial.print("  Diff: ");Serial.println(Diff);

  error = RPM - reference_rpm;
  float P = kp * error;
  float D = kd * (error - error_old/Time);
  error_old = error;
  float Vwm =  P + D;
  Vwm = constrain(Vwm, 0, 255);
  pinMode(output_pin, Vwm); 
}
