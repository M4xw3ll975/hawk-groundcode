/*
    OLED-Screen logic and output format
*/

#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "util/Serial.h"
#include "pins/oledPins.h"
#include "settings/oledSet.h"
#include "OLED.h"

// display
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire);

// write to display
void writeToDisplay(String type, String msg) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("AAE Hawk");
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
    display.setTextSize(OLED_FONT_SIZE);
    srlInfo("OLED", "Initialized");
    writeToDisplay("OLED:", "Initialized");
}
