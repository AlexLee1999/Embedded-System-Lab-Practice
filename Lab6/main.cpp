#include "mbed.h"


InterruptIn button(USER_BUTTON);
DigitalOut led(LED1);
Timeout  press_threhold;
EventQueue queue(32 * EVENTS_EVENT_SIZE);
Thread t;

void button_release_detecting()
{
    button.enable_irq();
}



void button_pressed()
{
    button.disable_irq();
    
    press_threhold.attach(&button_release_detecting, 1000ms);
}

void button_released()
{
    led = !led;
    queue.call(printf, "Embedded System Lab is a good course. %p\n", ThisThread::get_id());
}


// main() runs in its own thread in the OS
int main()
{
    t.start(callback(&queue, &EventQueue::dispatch_forever));
    button.fall(&button_pressed);
    button.rise(&button_released);
    while (1);
}
