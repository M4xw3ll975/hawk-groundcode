/*
    Interfacing with the PS3 Controller
    and other stuff related to it
*/

#include <Arduino.h>
#include <Ps3Controller.h>
#include "Controller.h"
#include "util/Serial.h"
#include "util/OLED.h"
#include "settings/ps3Set.h"

unsigned long prevMillis = 0;
int stickOut[4];

void onConnect() {
    srlInfo("ps3ctl", "Connected");
}

void initPs3() {
    Ps3.attachOnConnect(onConnect);
    Ps3.begin(MASTER_ADDRESS);
    srlInfo("ps3ctl", "Initialized");
    writeToDisplay("ps3ctl:", "Initialized");
}

void procps3() {
    if (Ps3.isConnected()) {
        // fetch all values
        stickOut[0] = Ps3.data.analog.stick.ry;
        stickOut[1] = Ps3.data.analog.stick.rx;
        stickOut[2] = Ps3.data.analog.stick.lx;
        stickOut[3] = Ps3.data.analog.stick.ly;
        // apply deadzone
        for (int i = 0; i < 4; i = i + 1) {
            if (stickOut[i] < DEADZONE && stickOut[i] > (DEADZONE*(-1)) ) {
                stickOut[i] = 0;
            }
        }
    } else return;
}

void ps3Stat() {
    if (Ps3.isConnected()) {
        unsigned long currMillis = millis();
        if (currMillis - prevMillis > PS3_LOG_INTERVAL) {
            prevMillis = currMillis;
            String LOG_STRING = "("
                + String(stickOut[0]) 
                + "/" + String(stickOut[1])
                + ") ("
                + String(stickOut[2])
                + "/" + String(stickOut[3])
                + ")";
            srlInfo("ps3ctl:", LOG_STRING);
            writeToDisplay("ps3ctl", LOG_STRING);
        } else return;
    } else return;
}

int fetchControllerVals(int id) {
    return stickOut[id];
}
