#include "Pit.h"
#include "Uart.h"
#include "Adc.h"
#include "Gpio.h"

void PIT_Init(void) {
	
	/*  Activarea semnalului de ceas pentru perifericul PIT*/
	SIM->SCGC6 |= SIM_SCGC6_PIT_MASK;
	/*  Utilizarea semnalului de ceas pentru tabloul de timere*/
	PIT->MCR &= ~PIT_MCR_MDIS_MASK;
	/*  Oprirea decrementarii valorilor numaratoarelor in modul debug*/
	PIT->MCR |= PIT_MCR_FRZ_MASK;
	/*  Setarea valoarea numaratorului de pe canalul 0 la o perioada de 1 secunda*/
	PIT->CHANNEL[0].LDVAL = 0x8851EA;  /* in decimal: 8 933 666, pt 852 ms */  
	
  /*  Activarea intreruperilor pe canalul 0*/
	PIT->CHANNEL[0].TCTRL |= PIT_TCTRL_TIE_MASK;
	/* Activarea timerului de pe canalul 0 */
	PIT->CHANNEL[0].TCTRL |= PIT_TCTRL_TEN_MASK;

/* 	Activarea intreruperii mascabile si setarea prioritatiis */

	NVIC_ClearPendingIRQ(PIT_IRQn);
	NVIC_SetPriority(PIT_IRQn,5);
	NVIC_EnableIRQ(PIT_IRQn);
}

void PIT_IRQHandler(void) {
	
	if(PIT->CHANNEL[0].TFLG & PIT_TFLG_TIF_MASK) 
	{
		ChangePlacaColor();
		PIT->CHANNEL[0].TFLG &= PIT_TFLG_TIF_MASK;
	}
}
