/*
    This file contains most of the 
    Communication logic via the LoRa
*/

#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include "LoRa.h"
#include "proc/lTRX.h"
#include "util/Serial.h"
#include "util/OLED.h"
#include "pins/loraPins.h"
#include "settings/loraSet.h"

void onReceive(int packetSize) {
    if (packetSize == 0) return;

    String LoRaData = "";
    byte recipient = LoRa.read();
    byte sender = LoRa.read();
    int incomingLength = LoRa.read();
    int incomingID = LoRa.read();

    while (LoRa.available()) {
        LoRaData += (char)LoRa.read();
    }

    if (incomingLength != LoRaData.length()) {
        srlInfo("LoRa", "'" + String(incomingLength) +  "' -> corrupt?");
        return;
    }

    if (recipient != LORA_LOCAL) {
        srlInfo("LoRa", "'" + String(recipient) +  "' -> rogue?");
        return;
    }

    srlInfo("LoRa", "received '" 
            + String(recipient) + "/"
            + String(sender) + "/"
            + String(incomingLength) + "/"
            + String(LoRaData)
            + "'");

    declTRX(incomingID, LoRaData);
}

void LoRaTXM(){
  LoRa.idle();
}

void LoRaRXM(){
  LoRa.receive();
}

void sendLoRa(int type, String outgoing) {
  LoRaTXM();
  LoRa.beginPacket();
  LoRa.write(LORA_DEST);
  LoRa.write(LORA_LOCAL);
  LoRa.write(outgoing.length());
  LoRa.write(type);
  LoRa.print(outgoing);
  LoRa.endPacket();
}

void initLoRa() {
    SPI.begin(SCK, MISO, MOSI, SS);
    LoRa.setPins(SS, RST, DIO0);
    if (!LoRa.begin(BAND)) {
        srlError("LoRa", "Unable to start!");
        while (1);
    }
    LoRa.onReceive(onReceive);
    LoRa.onTxDone(LoRaRXM);
    LoRaRXM();
    srlInfo("LoRa", "Initialized");
    writeToDisplay("LoRa:", "Initialized");
}
