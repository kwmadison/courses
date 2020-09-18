#include "msp430.h"

// Pin assignments
#define P_PWM       BIT2
#define P_LEDR     BIT0
#define P_LEDG     BIT6
#define P_CAN   BIT3

// Timing constants
#define F_TACLK     16E6l  // Timer A clock frequency
#define F_TBCLK      300  // Timer B clock frequency


#define F_PWM       50  // PWM frequency
#define F_BLINK     2  // LED

// Modes