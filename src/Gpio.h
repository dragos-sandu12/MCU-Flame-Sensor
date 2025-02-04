#include "MKL25Z4.h"
void RGBLed_Init(void);
void ChangeColorFromFlame(float);
void ChangePlacaColor(void);
void black(void);
void SetRGB(int, int, int);

volatile extern uint8_t ledDirection;
