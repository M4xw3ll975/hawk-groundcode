/*
    Hardware Button Handling
*/

#include <Arduino.h>
#include "hwbts.h"
#include "pins/buttonPins.h"

void inithwbts() {
    pinMode(BUTTON1, INPUT);
}

void hwbtListener() {
    int buttonState = digitalRead(BUTTON1);
    if(buttonState == HIGH) { delay(250); }
}
