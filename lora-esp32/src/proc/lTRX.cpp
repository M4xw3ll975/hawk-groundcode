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
// keep track of packet count
unsigned int pktCnt = 0;
// packet related data for last
int lastPacketRSSI = 0;
float lastPacketSNR = 0.0;
// remote pkt counter for LQ
int remoteRSSI = 0;
float remoteSNR = 0.0;

// craft control packets to be handled by receiver
void lTRXStream() {
    sendLoRa(1,
        "A" +
        String(fetchCtrl(0)) +
        "E" +
        String(fetchCtrl(1)) +
        "R" +
        String(fetchCtrl(2)) +
        "SR" + 
        String(fetchBtn(0)) +
        "SL" +
        String(fetchBtn(1)) +
        "Q"
    );
    ++pktCnt;
}

// link quality management
void handleStream(int t, String d) {
    remoteRSSI = d.substring(2, d.indexOf("Q")).toInt();
    srlInfo("lTRX", String(remoteRSSI) );
    return;
}

// decoder function for lTRX packets
void declTRX(int msgType, String data, int pktRS, float pktSNR) {
    lastPacketRSSI = pktRS;
    lastPacketSNR = pktSNR;
    handleStream(msgType, data);
}

// lTRX main control loop
void lTRXctl() {
    // send response after delay
    if (millis() - prCL > LTRX_DELAY) {
        // set transmit
        LoRaTXM();
        // send
        lTRXStream();
        prCL = millis();
    } else return;
    // recieving
    LoRaRXM();
}
