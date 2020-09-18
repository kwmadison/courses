#include "msp430.h"
#include "consts.h"

volatile unsigned int signal = 11;

int main(void) {
    /* PIN CONFIGURATIONS */
    P1DIR = P_CAN | P_LEDR | P_LEDG | P_PWM;  // set leds and pwm pin as output
    P1OUT = 0;
//    P1SEL |= P_PWM;  // set pwm pin special function to TA0.1

    /* CLOCK CONFIGURATIONS */
    WDTCTL = WDTPW + WDTHOLD;  // Disable watchdog timer
    BCSCTL1 = CALBC1_16MHZ;  // Configure clock for 16MHz frequency
    DCOCTL = CALDCO_16MHZ;
    BCSCTL2 = 0;  // Select SMCLK source as DCO with divider 1

    /* TIMER CONFIGURATIONS */
    TACTL = TASSEL_2 | MC_1;  // Source Timer A from SMCLK in up mode
    TACCTL1 = CCIE | OUTMOD_7;  // reset/set mode
    TACCR0 = 32;  // set pwm period on CCR1
    TACCR1 = 16;  // set pwm duty cycle on CCR1
    TACCR2 =
//
//    TBCTL = TBSSEL_1 | MC_1;  // Source Timer B from ACLK in up mode
//    TBCCTL1 = CCIE + OUTMOD_3;  // TACCTL1 Capture Compare
//    TBCCR0 = F_TBCLK / 8 - 1;  // period
//    TBCCR1 = 0


//    _BIS_SR(LPM0_bits);  // enter low-power mode

//    __enable_interrupt();

//    __bis_SR_register(LPM3_bits + GIE);   // LPM3 with interrupts enabled

    return 0;
}


#if defined(__TI_COMPILER_VERSION__)
#pragma vector=TIMER0_A1_VECTOR
__interrupt void ta1_isr (void)
#else
void __attribute__ ((interrupt(TIMER0_A1_VECTOR))) ta1_isr(void)
#endif
{
    if (signal % 2) {
        P1OUT |= P_CAN;
    }
    else {

    }
    signal >>= 1;

}