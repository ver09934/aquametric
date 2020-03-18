#include <JsonParserGeneratorRK.h>
#include <math.h>
#include <VL53L0X.h>

const int    SAMPLE_NUMBER      = 5;            // Constants for thermistor readings
const double BALANCE_RESISTOR   = 97200.0;
const double MAX_ADC            = 4095.0;
const double BETA               = 3974.0;
const double ROOM_TEMP          = 298.15;
const double RESISTOR_ROOM_TEMP = 100000.0;


int thermistorPin = A0;

SYSTEM_THREAD(ENABLED);                         // Allows the device to take sample measurements while attempting to make a cloud connection

ApplicationWatchdog wd(600000, timedShutdown);       // Turns off the device if measurement is not taken successfully after 10 minutes

VL53L0X sensor;                                 // Creates instances of the ToF distance sensor and battery voltage measurement
FuelGauge fuel;

void setup(){
    pinMode(D2, OUTPUT);                        // Digital pin 2 used to signal Arduino when the device is done uploading its data and can be safely put into sleep
    digitalWrite(D2, LOW);
    Serial.begin(9600);
    RGB.control(true); 
    RGB.brightness(2);
    RGB.control(false);

    begining:
    
    delay(500);
    JsonWriterStatic<256> doc;                  // Assembles sensor data into JSON string to be uploaded
	{
		JsonWriterAutoObject obj(&doc);

		doc.insertKeyValue("id", "001");
		doc.insertKeyValue("battery", fuel.getVCell());
		doc.insertKeyValue("stage", getRange());
		doc.insertKeyValue("temp", getTemp());
		doc.insertKeyValue("conductivity", getCond());
		doc.insertKeyValue("turbidity", getTurb());
	}
    
    while(!Particle.connected()){               // Waits here until device establishes a cloud connection
        delay(500);
    }
    
    Particle.publish("Measurement", doc.getBuffer());   // Publishes sensor measurement and sends sleep signal
    delay(15000);
    RGB.control(true); 
    RGB.color(0, 0, 255);
    delay(1000);
    digitalWrite(D2, HIGH);
    delay(1000);
    Particle.publish("Measurement", "{\"IMPROPER SHUTDOWN\"}");
    //Serial.println(doc.getBuffer());
    //Serial.println(getTemp());
    //delay(1000);
    //goto begining;
    
}

void loop() {                                   // The boron is shut down completely in between sends, so nothing runs in a loop

}

bool timedShutdown(){                           // Runs if device stays awake for more than 10 minutes
    RGB.control(true); 
    RGB.color(255, 0, 0);
    delay(1000);
    digitalWrite(D2, HIGH);
    delay(1000);
    Particle.publish("Measurement", "{\"IMPROPER SHUTDOWN\"}");
}

int getRange(){
    
    Wire.begin();
    
    if(!sensor.init()){                         // Initilizes ToF distance sensor
        return -2;
    }
    
    delay(200);
    
    sensor.setTimeout(500);                     // Puts ToF sensor into long range mode
    sensor.setSignalRateLimit(0.1);
    sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 18);
    sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 14);
    sensor.setMeasurementTimingBudget(200000);
    
    int sum = 0;
    
    delay(200);
    
    for (int i = 0; i < 5; i++){
        delay(200);
        sum += sensor.readRangeSingleMillimeters();     // Take 5 range measurements and return average
    }
    
    /*f(sensor.timeoutOccurred()){
        return -1;
    }*/
    
    return sum/5;
    
}

double getCond(){
    int sum = 0;
    
    for (int i = 0; i < 5; i++){
        sum += map(analogRead(A1),0.0,4095.0,0.0,1.0);     // Take 5 conductivity measurements and return average as value from 0 to 1
    }
    return sum/5;
}

double getTemp() 
{
  double rThermistor = 0;
  double tKelvin     = 0;
  double tCelsius    = 0;
  double adcAverage  = 0;
  int    adcSamples[SAMPLE_NUMBER];
  
  for (int i = 0; i < SAMPLE_NUMBER; i++) 
  {
    adcSamples[i] = analogRead(thermistorPin);
    delay(10);
  }

  for (int i = 0; i < SAMPLE_NUMBER; i++) 
  {
    adcAverage += adcSamples[i];                // Take the average of 5 temperature readings
  }
  adcAverage /= SAMPLE_NUMBER;

  rThermistor = BALANCE_RESISTOR * ( (MAX_ADC / adcAverage) - 1);
  tKelvin = (BETA * ROOM_TEMP) / 
            (BETA + (ROOM_TEMP * log(rThermistor / RESISTOR_ROOM_TEMP)));
  tCelsius = tKelvin - 273.15;
  return tCelsius;                              // Return the temperature in Celsius
}

double getTurb() 
{
    int sum = 0;
    
    for (int i = 0; i < 5; i++){
        sum += map(analogRead(A2),0.0,4095.0,0.0,1.0);     // Take 5 conductivity measurements and return average as value from 0 to 1
    }
    return sum/5;
}
