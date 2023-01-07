/*
    lTRX
    Protocol for intercommunication and packet parsing
*/

#include <Arduino.h>
#include "lTRX.h"
#include "proc/Controller.h"
#include "util/LoRa.h"
#include "util/Serial.h"
#include "settings/ltrxset.h"

// timeouts for main loop
unsigned long pastMillTRX = 0;
unsigned long pastMillRespThresh = 0;
// keep track of packet count
unsigned int pktCnt = 0;
// packet related data for last
int lastPacketRSSI = 0;
float lastPacketSNR = 0.0;
// remote pkt counter for LQ
int remoteRSSI = 0;
float remoteSNR = 0.0;
// true if we have to wait for telemetry
bool waitForACK = false;

// link quality management
void handleStream(int t, String d) {
    if ( t == 200 ) {
        // recieved telemetry ACK, clear wait
        waitForACK = false;
        // handle data
        remoteRSSI = d.substring(2, d.indexOf("Q")).toInt();
        srlInfo("lTRX", String(remoteRSSI) );
    } else return;
}

// craft control packets to be handled by receiver
void lTRXTransmit() {
    if ( pktCnt < LTRX_TELEMETRY_RATE ) {
        /*
            Data Packet ( 
                A[val] - Stick Aileron
                E[val] - Stick Elevator
                R[val] - Stick Rudder
                SL[val] - Button Shoulder Left
                SR[val] - Button Shoulder Right
                Q - EOF
            )
        */
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
        pktCnt++;
    } else {
        // telemetry request packet
        sendLoRa(100,"REQ");
        // update REQ timestamp
        pastMillRespThresh = millis();
        // requested ACK, set wait bool
        waitForACK = true;
        // reset packet count
        pktCnt = 0;
    }
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
    if (millis() - pastMillTRX > LTRX_DELAY) {
        if ( 
            !waitForACK || 
            millis() - pastMillRespThresh > LTRX_RESPONSE_THRESHOLD 
        ) {
            // clear wait
            waitForACK = false;
            // transmitting
            LoRaTXM();
            lTRXTransmit();
        } else {
            // set recieve
            LoRaRXM();
        }
        pastMillTRX = millis();
    } else return;
}
