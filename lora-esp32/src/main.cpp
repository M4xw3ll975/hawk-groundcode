/*
  main file
  folder structure explained below

  src/
  ├─ main.cpp
  ├─ settings/
  │  ├─ header files with settings for other code modules
  ├─ pin/
  │  ├─ contains header files with pin definitions
  ├─ util/
  │  ├─ general use modules and code
*/

#include <Arduino.h>
#include "util/LoRa.h"
#include "util/hwbts.h"
#include "util/Controller.h"
#include "util/Serial.h"
#include "util/OLED.h"
#include "proc/lTRX.h"

void setup() {
  // Serial init
  Serial.begin(115200);
  // init OLED screen and output
  initOLED();
  // init LoRa Link and Comms
  initLoRa();
  // init HW Buttons
  inithwbts();
  // init ps3 Controller interface
  initPs3();
}

void loop() {
  procps3();
  lTRXctl();
  ps3Stat();
}
