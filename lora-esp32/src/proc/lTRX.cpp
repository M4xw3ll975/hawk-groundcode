/*
    lTRX
    Protocol for intercommunication and packet parsing
*/

#include <Arduino.h>
#include "lTRX.h"
#include "util/LoRa.h"
#include "util/Controller.h"
#include "util/Serial.h"
#include "settings/ltrxset.h"

unsigned long prCL = 0;
unsigned long crCL = 0;

void craftCTL(int t) {
    switch (t) {
        case 31:
            sendLoRa(t,
                "A" +
                String(fetchControllerVals(0)) +
                "E" +
                String(fetchControllerVals(1)) +
                "R" +
                String(fetchControllerVals(2)) +
                "Q"
            );
            break;
        /*
        case 32:
            // Custom Button 1, @TODO, do nothing for now
            break;
        case 33:
            // Custom Button 2, @TODO, do nothing for now
            break;
        case 34:
            // Custom Button 3, @TODO, do nothing for now
            break;
        */
    }
}

void declTRX(int msgType, String data) {
    switch (msgType) {
        /*
        case 10 ... 19:
            // ACK, @TODO, do nothing for now
            break;
        case 20 ... 29:
            // ACK, @TODO, do nothing for now
            break;
        case 30 ... 39:
            // CTL, @TODO, do nothing for now
            break;
        case 40 ... 49:
            // ERR, @TODO, do nothing for now
            break;
        case 50 ... 59:
            // GPS, @TODO, do nothing for now
            break;
        */
    }
}

void lTRXctl() {
    crCL = millis();
    if (crCL - prCL > LTRX_DELAY) {
        prCL = crCL;
        craftCTL(31);
    } else return;
}
