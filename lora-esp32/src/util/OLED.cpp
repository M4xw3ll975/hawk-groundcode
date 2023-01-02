/*
    OLED-Screen logic and output format
*/

#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "util/Serial.h"
#include "OLED.h"

// display
Adafruit_SSD1306 display(128, 64, &Wire);

// write to display
void writeToDisplay(String type, String msg) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("AAE");
    display.setCursor(0, 28);
    display.println(type);
    display.setCursor(0, 44);
    display.println(msg);
    display.display();
}

// initialize display
void initOLED() {
    Wire.begin(OLED_SDA, OLED_SCL);
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3c, false, false)) {
        srlError("OLED", "Unable to initialize");
        while (1);
    }
    display.setTextColor(SSD1306_WHITE);
    display.setTextSize(1);
    srlInfo("OLED", "Initialized");
    writeToDisplay("OLED:", "Initialized");
}
