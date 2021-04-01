/*
	Name:       test_ino_py.ino
	Created:	27/08/2018 19:10:36
	Author:     EMSE2000\joseph.brunet
*/


#include <Wire.h>
#include <Adafruit_ADS1015.h>

Adafruit_ADS1115 ads;  /* Use this for the 16-bit version */

//----------------------------
// VARIABLE TO STORE RECEIVED DATA
const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
int index = 1;
char incomingByte;
//----------------------------
// PIN DEFINITION

const int tarePin = 12;     // the number of the pushbutton pin
const int oriPin = 10;     // the number of the pushbutton pin
const int secuPin = 11;     // the number of the pushbutton pin


char buf [40]; // must be large enough for the whole stringint sensorPin = 0;
int ori = 0;
int secu = 0;
float F;
float F_recal;
float F_tot = 0;
float F_fin = 0;
float F_fin2 = 0;
float P;
float P_recal;
float P_tot = 0;
float P_fin = 0;
float F_offset = 0;
float P_offset = 0;
int c = 0;


float test;

//-----------------------------------------------------------

void setup() {
  Serial.begin(115200); //max
  
  pinMode(tarePin, OUTPUT);     
  pinMode(oriPin, INPUT);     
  pinMode(secuPin, INPUT);     
  
  //Serial.println("Getting differential reading from AIN0 (P) and AIN1 (N)");
  //Serial.println("ADC Range: +/- 6.144V (1 bit = 3mV/ADS1015, 0.1875mV/ADS1115)");

  // The ADC input range (or gain) can be changed via the following
  // functions, but be careful never to exceed VDD +0.3V max, or to
  // exceed the upper and lower limits if you adjust the input range!
  // Setting these values incorrectly may destroy your ADC!
  //                                                                ADS1115
  //                                                                -------
  // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 0.1875mV (default)
   ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.0078125mV

  ads.begin();

}

//-----------------------------------------------------------

void loop() {

  int16_t val_F;
  int16_t val_P;
  secu = 0;
  ori = 0;



  // Sécurity
  if (digitalRead(secuPin) == 0) {
    //Serial.println("Secu");
    secu = 1;
  }

  if (digitalRead(oriPin) == 1) {
    //Serial.println("Origin");
    ori = 1;
  }


  /* Be sure to update this value based on the IC and the gain settings! */
  float multiplier = 0.125F; /* ADS1115  @ +/- 6.144V gain (16-bit results) */
  
  val_F = ads.readADC_Differential_0_1();  
  val_P = ads.readADC_Differential_2_3(); 
  
  
  P = val_P* multiplier;
  P = (P * 0.00069893138)*750.062;   //*750.062 pour mettre en mmHg
  P_recal = P - P_offset; 

  F = val_F* multiplier;
  //F = (F * 7.69637 * 9.81 / 1000);//-(P_recal*0.000133322*3.1415*0.2*0.2);
  F = (F * 8.67086272335938 * 9.81 / 1000)  -(P_recal*0.000133322*3.1415*0.2*0.2);  
  F_recal = F -  F_offset;


   //Add 5 value
  c = c+1;
  F_tot = F_tot + F_recal;
  P_tot = P_tot + P_recal;
  
  if (c == 5) {
   
  P_fin = P_tot / c;
  F_fin = F_tot / c;
  F_fin2 = F_fin ;//- (P_fin/(750.062*10))*3.14*4*4;   //Remove the force induce by the pressure
  
  char str_temp_F[10];
  char str_temp_P[10];

  /* 4 is mininum width, 2 is precision; float value is copied onto str_temp*/
  dtostrf(F_fin2, 4, 3, str_temp_F);
  dtostrf(P_fin, 4, 3, str_temp_P);

  sprintf (buf, "%s\r\n", str_temp_F); 
  sprintf (buf, "(%1d,%1d,%s,%s)\r\n", secu,ori,str_temp_F,str_temp_P); 

  Serial.print (buf);
  
  
  c = 0;
  F_tot = 0;
  P_tot = 0;
  
  }

  //Serial.println (P);

  
  //--------------------------------------------------------------        
  //--------------------------------------------------------------
  //// Read incomming order  
        
  if (Serial.available() > 0) {
        index = 0;
        for (int i = 0; i < sizeof(receivedChars); i++) {  //Erase memory at each iteration
          receivedChars[i] = '\0';
        }
        while (Serial.available() > 0) {
          incomingByte = Serial.read();  // Read the incomming bit 
                                        //(one at a time / need to empty the buffer)
          //Serial.print(incomingByte);
          receivedChars[index] = incomingByte;       //Put the bit in the memory array
          index++;               //incrementation
        }

        //receivedChars[strlen(receivedChars)-1]='\0'; //remove the linebreak at the end
        //Serial.println(receivedChars);
        
    
        //// Define orders !
        if (strcmp(receivedChars, "tare_F") == 0) {
        // Function to tare the load cell
          Serial.println("Tare baby");
          //digitalWrite(tarePin, HIGH);
          //delay(500);
          //digitalWrite(tarePin, LOW);
          //delay(500);
          F_offset = F_fin + F_offset;
         
        }
        if (strcmp(receivedChars, "tare_P") == 0) {
        // Function to tare the load cell
          Serial.println("Tare baby");
          P_offset = P_fin + P_offset;
        }

  }
  //--------------------------------------------------------------
  //--------------------------------------------------------------
  
  
  delay(10); //IMPORTANT this delay play an important role in the total speed

}


//void ini() {
//// Function to initialise the machine
//  
//  Serial.println("Initialisation 1st step: ");
//  while  capteur bas == 0 {
//    delay(10);
//  }
//  
//  Serial.println("on");
//  Serial.println("on");
//  Serial.println("on");
//  
//  Serial.println("Initialisation 2nd step: ");
//  while  capteur haut == 0 {
//    delay(10);
//  }
//
//  Serial.println("on");
//  Serial.println("on");
//  Serial.println("on");
//
//}
