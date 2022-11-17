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

// timeouts for main loop
unsigned long prCL = 0;
unsigned long crCL = 0;
// keep track of packet count
unsigned int pktCnt = 0;
// packet related data for last
int lastPacketRSSI = 0;
float lastPacketSNR = 0.0;
// remote pkt counter for LQ
int remotePktDiff = 0;

// craft control packets to be handled by receiver
void craftCTL(int t) {
    switch (t) {
        case 11:
            // Link REQ packet
            // (PC[val]Q)
            sendLoRa(t,
                "PC" +
                String(pktCnt) +
                "Q"
            );
            ++pktCnt;
            break;
        case 31:
            // most important packet
            // crafts controlle stick vals
            // ( A[val]E[val]R[val]Q )
            sendLoRa(t,
                "A" +
                String(fetchCtrl(0)) +
                "E" +
                String(fetchCtrl(1)) +
                "R" +
                String(fetchCtrl(2)) +
                "Q"
            );
            ++pktCnt;
            break;
        case 32:
            // L/R Shoulder Buttons
            // ( SR[val]SL[val]Q )
            sendLoRa(t,
                "SR" + 
                String(fetchBtn(0)) +
                "SL" +
                String(fetchBtn(1)) +
                "Q"
            );
            ++pktCnt;
            break;
        case 33:
            // Symbol Buttons
            // ( PX[val]PS[val]PT[val]PC[val]Q )
            sendLoRa(t,
                "PX" + 
                String(fetchBtn(2)) +
                "PS" + 
                String(fetchBtn(3)) +
                "PT" + 
                String(fetchBtn(4)) +
                "PC" + 
                String(fetchBtn(5)) +
                "Q"
            );
            ++pktCnt;
            break;
    }
}

// link quality management
void handleLNK(int t, String d) {
    switch (t) {
        case 12:
            remotePktDiff = d.substring(2, d.indexOf("Q")).toInt();
            break;
    }
}

// decoder function for lTRX packets
void declTRX(int msgType, String data, int pktRS, float pktSNR) {
    lastPacketRSSI = pktRS;
    lastPacketSNR = pktSNR;
    switch (msgType) {
        case 10 ... 19:
            handleLNK(msgType, data);
            break;
        /*
        case 20 ... 29:
            // GPS, @TODO, do nothing for now
            break;
        */
    }
}

// lTRX main control loop
void lTRXctl() {
    crCL = millis();
    if (crCL - prCL > LTRX_DELAY) {
        prCL = crCL;
        // main control is always sent
        craftCTL(31);
        // every 4 packets
        if (pktCnt % 4 == 0) {
            craftCTL(32);
            craftCTL(33);
            craftCTL(11);
        }
    } else return;
}
