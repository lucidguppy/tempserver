#define aref_voltage 3.3

int tempPin = 0;
int tempReading;

void setup()
{
  Serial.begin(9600);
  analogReference(EXTERNAL);
}

void loop()
{

  if (Serial.available() > 0) 
  {
    int inByte = Serial.read();
    float tempc = getVoltage(tempPin);
    float tempf = 0.0;
    tempc = (tempc - 0.5) * 100;
    tempf = (tempc*9.0/5.0) + 32;
    if (inByte == 'c') 
    {
      Serial.print(tempc);
      Serial.println(" c ");
    } 
    else if (inByte == 'f') 
    {
      Serial.print(tempf);
      Serial.println(" f");
    } 
    else
    {
      Serial.println("Error: Bad Command (use 'c' or 'f')");
    }
  } 
  //sleep a little for energy 
}

float getVoltage(int pin)
{
  tempReading = analogRead(pin);
  float voltage = tempReading * aref_voltage;
  
  return voltage / 1024.0;
}

