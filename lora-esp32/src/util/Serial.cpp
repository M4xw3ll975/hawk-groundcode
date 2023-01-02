/*
    Communicate with WCP and other serial interfaces
*/

#include <Arduino.h>
#include "Serial.h"
#include <ArduinoJson.h>
#include "settings/serialSet.h"

// create json onbjects for streams
jsonObject infoStream, errorStream, telemStream;

void initSerial() {
  // Initialize serial communication
  Serial.begin(BAUD_RATE);
}

String toJson(jsonObject &inJson) {
    // Create a JSON object
    StaticJsonDocument<200> doc;
    
    // what to include
    doc["id"] = inJson.ID;

    // serialize it and return
    String jsonString;
    serializeJson(doc, jsonString);
    return jsonString;
}

// @TODO: reciever loop
void srlRX() {
    if (Serial.available()) {
        // Read the input
        String jsonString = Serial.readStringUntil('\n');
        // dont do anything if the message isn't from WCP
        if (jsonString.startsWith("WCP")) {
            // Deserialize the JSON string into a dynamic JSON object
            DynamicJsonDocument doc(200);
            DeserializationError error = deserializeJson(doc, jsonString);
            // Check if the JSON string was successfully deserialized
            if (error) {
                return;
            } else {
                // @TODO: do necessary stuff
                return;
            }
        }
    }
}

// serial general info message
void srlInfo(String type, String infoMsg) {
    // zero for normal
    infoStream.ID = 0;
    infoStream.msg = type + infoMsg;
    Serial.println("ESP" + toJson(infoStream));
}

// serial error message
void srlError(String type, String errorMsg) {
    // one for error
    errorStream.ID = 1;
    errorStream.msg = type + errorMsg;
    Serial.println("ESP" + toJson(errorStream));
}

// serial telemetry from lTRX and other
void srlTLM() {
    // ten for telemetry
    telemStream.ID = 10;
    errorStream.msg = "Telemetry";
    Serial.println("ESP" + toJson(telemStream));
}
