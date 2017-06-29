#include <Servo.h>
#include "HX711.h" 
#include <SPI.h>
#include <SD.h>

#define DOUT  3
#define CLK  2


/*
 * First send full throttle
 * Turn on ESC and motor (3 beeps means all electronics are connected properly)
 * After 4 long beeps, move it to the lowest position
 * After 1 second, there should be 2 beeps emitted
 * Then the ESC is calibrated
 * */

//This is the file that will record all the data produced by the program
File recordedData;
String fileName;

//Servo and ESC variables (pins)
Servo esc;
int escPin = 9;
int throttle = 40;

//Controls the loops inside - not important
boolean printed = false;
boolean completed = false;

//The HX711. DOUT and CLK is saved above
HX711 scale(DOUT, CLK);

void setup() {

  /*
   * This part of the code is setting up the ESC and the serial communications
   */
  //Start serial communication at 9600 bits per second
  Serial.begin(9600);

  //Attach the pin to the esc
  esc.attach(escPin);
  esc.write(0);
  
  /*
   * This part of the code is setting up the SD Cards read and write features
   */
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  Serial.print("Initializing SD card...");

  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");

  fileName = "thr_data.txt";

  recordedData = SD.open(fileName, FILE_WRITE);

  if (!recordedData) {
    // if the file didn't open, print an error:
    Serial.println("ERROR: COULD NOT WRITE TO TXT FILE");
  }

  recordedData.close();
}

void loop() {
  if(!completed){
    if(!printed){
      Serial.println("Awaiting calibration, type HIGH to begin process.");
      printed = true;
    }
    String input = Serial.readString();
    if(input == "HIGH"){
      esc.write(149);
      Serial.println("Your ESC is at full throttle, type LOW to begin next process."); 
    } else if (input == "LOW"){
      esc.write(0);
      Serial.println("Your ESC is at lowest throttle, type FINISH to complete the calibration.");
    } else if (input == "FINISH"){
      Serial.println("Your ESC is now running normally, type EXIT to end calibration");
      input = Serial.readString();
    } else if (input == "EXIT" || input == "SKIP"){
      completed = true;
    } else if (input == "STOP"){
       esc.write(0);
    }
  } 
  else {

    recordedData = SD.open(fileName, FILE_WRITE);
    
    int throttle;
    Serial.println("\nWhat is your throttle? (1-150, negative for 0)");
    //read throttle as int from serial
    //keep reading if parseInt times out or invalid value is inputted
    while (!throttle) {
      throttle = Serial.parseInt();
    }

    if (throttle < 0) {
      throttle = 0;
    }
    
    if (throttle > 149) {
      throttle = 149;
    }

    //write throttle to the ESC
    esc.write(throttle);
    //read load cell
    //write data
    Serial.println("1  |Time: " + (String)(millis() / 1000.0) + "|HX711: " + (String)scale.get_units() + "|Throttle: " + (String)((throttle/150.0) * 100));
    recordedData.println("1  |Time: " + (String)(millis() / 1000.0) + "|HX711: " + (String)scale.get_units() + "|Throttle: " + (String)((throttle/150.0) * 100));

    delay(1000);
    //read load cell
    //write data
    Serial.println("2  |Time: " + (String)(millis() / 1000.0) + "|HX711: " + (String)scale.get_units() + "|Throttle: " + (String)((throttle/150.0) * 100));
    recordedData.println("2  |Time: " + (String)(millis() / 1000.0) + "|HX711: " + (String)scale.get_units() + "|Throttle: " + (String)((throttle/150.0) * 100));
    
    delay(2000);
    //read load cell
    //write data
    Serial.println("3  |Time: " + (String)(millis() / 1000.0) + "|HX711: " + (String)scale.get_units() + "|Throttle: " + (String)((throttle/150.0) * 100));
    recordedData.println("3  |Time: " + (String)(millis() / 1000.0) + "|HX711: " + (String)scale.get_units() + "|Throttle: " + (String)((throttle/150.0) * 100));
    
    Serial.println("ESC currently running at " + (String)((throttle/150.0) * 100) + "% max throttle");

    recordedData.close();
  }

  delay(1);
}
