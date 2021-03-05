// Testing code for 4 channel driver
// Author: Bill Cai, Robert Herlihy
// Date:   2021/02/12


// not on for now, after the encoder is enable, we will use it
volatile int rotaryCount = 0;
//#define INTERRUPT 0  // that is, pin 2
//#define INTERRUPT 1  // that is, pin 3
#define PINA 2
#define PINB 3 

#define DIRECTION1 5  // Channel 1 motor DIR pin
#define MOTOR1 9      // Channel 1 motor PWM pin

#define DIRECTION2 4  // Channel 2 motor DIR pin
#define MOTOR2 6      // Channel 2 motor PWM pin

#define DIRECTION3 8  // Channel 3 motor DIR pin
#define MOTOR3 11      // Channel 3 motor PWM pin

#define DIRECTION4 7  // Channel 4 motor DIR pin
#define MOTOR4 10      // Channel 4 motor PWM pin

#define TIME_FORWARDS 10000
#define TIME_BACKWARDS 10000

byte phase;
unsigned long start;
int time_to_go;
byte motorInstruction[5] = {0,0,0,0,0};
int serialInput;

int counter;

// Interrupt Service Routine for a change to encoder pin A (not in use now)
void isr ()
{
 boolean up;

 if (digitalRead (PINA))
   up = digitalRead (PINB);
 else
   up = !digitalRead (PINB);

 if (up)
   rotaryCount++;
 else
   rotaryCount--;
}  // end of isr

void setup ()
{
  // attachInterrupt (INTERRUPT, isr, CHANGE);   // interrupt 0 is pin 2, interrupt 1 is pin 3
    pinMode (MOTOR1, OUTPUT);
    pinMode (DIRECTION1, OUTPUT);
    pinMode (MOTOR2, OUTPUT);
    pinMode (DIRECTION2, OUTPUT);
    pinMode (MOTOR3, OUTPUT);
    pinMode (DIRECTION3, OUTPUT);
    pinMode (MOTOR4, OUTPUT);
    pinMode (DIRECTION4, OUTPUT);
    Serial.begin(9600);

    counter=0;
}  // end of setup

void loop ()
{
    if (counter == 0){
        //Set the direction of each motor as determined by the 4 least significant bits of the first byte of motorInstruction
       motorInstruction[0] & 0b00000001 ? digitalWrite(DIRECTION1, HIGH) : digitalWrite(DIRECTION1,LOW);
       motorInstruction[0] & 0b00000010 ? digitalWrite(DIRECTION2, HIGH) : digitalWrite(DIRECTION2,LOW);
       motorInstruction[0] & 0b00000100 ? digitalWrite(DIRECTION3, HIGH) : digitalWrite(DIRECTION3,LOW);
       motorInstruction[0] & 0b00001000 ? digitalWrite(DIRECTION4, HIGH) : digitalWrite(DIRECTION4,LOW);
       
       //Set the speed of the motors per the last 4 bytes of motorInstruction
       analogWrite(MOTOR1, motorInstruction[1]);
       analogWrite(MOTOR2, motorInstruction[2]);
       analogWrite(MOTOR3, motorInstruction[3]);
       analogWrite(MOTOR4, motorInstruction[4]);
       
    }
     if (Serial.available() > 0)
    {   
        //Execute the motor instruction next cycle
        //if (executeInstructionNextCycle){
       serialInput =Serial.read();
        if (serialInput != -1)
        {
            motorInstruction[counter] = (byte) serialInput;

            counter++;
            counter %=5;
        }
        Serial.print(rotaryCount);
    }
}  
