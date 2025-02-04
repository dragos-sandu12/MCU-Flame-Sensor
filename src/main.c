#include "Gpio.h"
#include "Uart.h"
#include "Adc.h"
#include "Pit.h"

static uint8_t flag = 0;

float measured_voltage;
uint8_t parte_zecimala;
uint8_t parte_fractionara1;

char changeLedSeqDir(void);

void ComponentsInit()
{
	UART0_Init(14400);
  RGBLed_Init();
	ADC0_Init();
  PIT_Init();
}

char changeLedSeqDir(void)
{
	if(UART0->S1 & UART0_S1_RDRF_MASK) 
	{
		char c;
		c = UART0->D;
		if(flag == 0)
			flag = 1;
		else
			flag = 0;
		ledDirection = flag;
		return c;
	}
	else
		return 'c';
}

int main(void)
{
	ComponentsInit();
	for(;;)
	{	
		for(int i=0;i<1000000;i++){}
			
		changeLedSeqDir();		
		if(readyToTransmit == 1)
		{
				measured_voltage = (analog_input * 6.0f) / 65535;
				
				parte_zecimala = (uint8_t) measured_voltage;
				parte_fractionara1 = ((uint8_t)(measured_voltage * 10)) % 10;
		
				ChangeColorFromFlame(parte_zecimala+(parte_fractionara1)/10);
				UART0_TransmitString("Value = ", parte_zecimala, parte_fractionara1);
				
				readyToTransmit = 0;
			}
		}
}

