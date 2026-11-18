#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 for a 16 chars and 2 line display
// (If 0x27 shows blank boxes later, change it to 0x3F)
LiquidCrystal_I2C lcd(0x3F, 16, 2); 

void setup() {
  // Start the serial connection at 9600 baud (matches Python)
  Serial.begin(9600);
  
  lcd.init();        // Initialize the LCD
  lcd.backlight();   // Turn on the backlight
  
  lcd.setCursor(0, 0);
  lcd.print("SYSTEM ONLINE");
  delay(2000);
  lcd.clear();
  lcd.print("AWAITING GESTURE");
}

void loop() {
  // Check if Python sent data over the USB cable
  if (Serial.available() > 0) {
    // Read the incoming text until the newline character '\n'
    String incomingText = Serial.readStringUntil('\n');
    
    lcd.clear(); // Clear the old text
    
    // Logic to wrap text cleanly across the two lines of the LCD
    if (incomingText.length() <= 16) {
      lcd.setCursor(0, 0);
      lcd.print(incomingText);
    } else {
      lcd.setCursor(0, 0);
      lcd.print(incomingText.substring(0, 16));
      lcd.setCursor(0, 1);
      lcd.print(incomingText.substring(16, 32));
    }
  }
}