/*
  main file
  folder structure explained below

  src/
  ├─ main.cpp
  ├─ settings/
  │  ├─ header files with settings for other code modules
  ├─ pin/
  │  ├─ contains header files with pin definitions
  ├─ proc/
  │  ├─ contains the more code heavy processing stuff and modules
  ├─ util/
  │  ├─ general use modules and code
*/

#include <Arduino.h>
#include "util/LoRa.h"
#include "util/Serial.h"
#include "util/OLED.h"
#include "proc/Controller.h"
#include "proc/lTRX.h"
#include "settings/version.h"

void setup() {
  // Serial init
  Serial.begin(115200);
  // init message
  srlInfo("System", "Starting " + String(GROUNDCODE_VERSION));
  // init OLED screen and output
  initOLED();
  // init LoRa Link and Comms
  initLoRa();
  // init ps3 Controller interface
  initPs3();
}

void loop() {
  // handle controller inputs
  procps3();
  // main lora control loop
  lTRXctl();
}
