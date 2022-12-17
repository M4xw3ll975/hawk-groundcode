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
    int incomingRSSI = LoRa.packetRssi();
    float incomingSNR = LoRa.packetSnr();

    while (LoRa.available()) {
        LoRaData += (char)LoRa.read();
    }
    if (incomingLength != LoRaData.length()) {
        return;
    }
    if (recipient != LORA_LOCAL) {
        return;
    }

    #ifdef LORA_RX_LOGGING
    srlInfo("LoRa", "received '" 
            + String(recipient) + "/"
            + String(sender) + "/"
            + String(incomingLength) + "/"
            + String(incomingID) + "/"
            + String(LoRaData)
            + "'");
    #endif

    declTRX(incomingID, LoRaData, incomingRSSI, incomingSNR);
}

void LoRaTXM(){
    LoRa.idle();
}

void LoRaRXM(){
    LoRa.receive();
}

void sendLoRa(int type, String outgoing) {
    LoRa.beginPacket();
    LoRa.write(LORA_DEST);
    LoRa.write(LORA_LOCAL);
    LoRa.write(outgoing.length());
    LoRa.write(type);
    LoRa.print(outgoing);
    LoRa.endPacket();

    #ifdef LORA_TX_LOGGING
    srlInfo("LoRa", "sent '" 
            + String(LORA_DEST) + "/"
            + String(LORA_LOCAL) + "/"
            + String(outgoing.length()) + "/"
            + String(type) + "/"
            + String(outgoing)
            + "'");
    #endif
}

void initLoRa() {
    SPI.begin(SCK, MISO, MOSI, SS);
    LoRa.setPins(SS, RST, DIO0);
    if (!LoRa.begin(BAND)) {
        srlError("LoRa", "Failed");
        writeToDisplay("LoRa:", "Failed");
        while (1);
    }
    LoRa.onReceive(onReceive);
    srlInfo("LoRa", "Initialized");
    writeToDisplay("LoRa:", "Initialized");
}
