/*
    Stuff in here is mostly for prettier
    serial console logging output
*/

#include <Arduino.h>
#include "Serial.h"
#include "settings/serialSet.h"

void srlError(String type, String errorMsg) {
    Serial.println("> Error:");
    Serial.println("> " + type + ": " + errorMsg);
    Serial.println(END_SEPERATOR);
}

void srlInfo(String type, String infoMsg) {
    Serial.println("> Info:");
    Serial.println("> " + type + ": " + infoMsg);
    Serial.println(END_SEPERATOR);
}
