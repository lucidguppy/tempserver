int tempPin = 0;


void setup()
{
  Serial.begin(9600);
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
  return (analogRead(pin) * .004882814);
}

