#include "MKL25Z4.h"

void ADC0_Init(void);
int ADC0_Calibrate(void);
uint16_t ADC0_Read(void);
void ADC0_IRQHandler(void);

volatile extern uint8_t readyToTransmit;
volatile extern uint16_t analog_input;
