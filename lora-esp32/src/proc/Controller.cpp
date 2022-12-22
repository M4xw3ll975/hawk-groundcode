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

// main stick val array
int stickOut[4];
// button array
int btnOut[6];

void onConnect() {
    srlInfo("ps3ctl", "Connected");
}

// expose controls
int fetchCtrl(int id) {
    return stickOut[id];
}

// expose buttons
int fetchBtn(int id) {
    return btnOut[id];
}

void initPs3() {
    Ps3.attachOnConnect(onConnect);
    Ps3.begin(MASTER_ADDRESS);
    srlInfo("ps3ctl", "Initialized");
    writeToDisplay("ps3ctl:", "Initialized");
}

// main controller process
void procps3() {
    if (Ps3.isConnected()) {
        // fetch all values
        stickOut[0] = Ps3.data.analog.stick.ry;
        stickOut[1] = Ps3.data.analog.stick.rx;
        stickOut[2] = Ps3.data.analog.stick.lx;
        stickOut[3] = Ps3.data.analog.stick.ly;
        btnOut[0] = Ps3.data.analog.button.r2;
        btnOut[1] = Ps3.data.analog.button.l2;
        btnOut[2] = Ps3.data.button.cross;
        btnOut[3] = Ps3.data.button.square;
        btnOut[4] = Ps3.data.button.triangle;
        btnOut[5] = Ps3.data.button.circle;
        // apply deadzone
        for (int i = 0; i < 4; i = i + 1) {
            if (stickOut[i] < DEADZONE && stickOut[i] > (DEADZONE*(-1)) ) {
                stickOut[i] = 0;
            }
        }
    } else return;
}
