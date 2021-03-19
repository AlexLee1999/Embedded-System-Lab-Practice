/*
 * Copyright (c) 2014-2020 Arm Limited and affiliates.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "PinNames.h"
#include "mbed.h"

// Adjust pin name to your board specification.
// You can use LED1/LED2/LED3/LED4 if any is connected to PWM capable pin,
// or use any PWM capable pin, and see generated signal on logical analyzer.
PwmOut led(PWM_OUT);

int main()
{
    // specify period first
    //led.period(0.05f);      // 4 second period
    //led.write(0.50f);      // 50% duty cycle, relative to period
    //led = 0.5f;          // shorthand for led.write()
    //led.pulsewidth(2);   // alternative to led.write, set duty cycle time in seconds
    led.period(0.05f);  // 4 second period
    int count = 0;
    while(1){
        if (count % 3 == 0){
            led.pulsewidth(0.01f);
        }
        else if(count % 3 == 1) {
            led.pulsewidth(0.02f);
        }
        else{
            led.pulsewidth(0.03f);
        }
        count ++;
    };          // led flashing
}
