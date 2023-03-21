//MOVEMENT STATEMACHINE
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <ezButton.h>

ezButton button(52); //CHANGE BUTTON PIN

LiquidCrystal_I2C lcd(0x27, 16, 2);
// defines pins
#define stepPin 2
#define dirPin 5 
#define stepPin2 4
#define dirPin2 7
#define relay_pin A8

//global variables
volatile uint8_t x,y,x2,y2;
volatile char type;

volatile int flag1,flag2;

const uint8_t numOffset = 0x61;
int pressed = 0;

String data;

void changeLCD(int t){

  if(t == 0){
    lcd.clear();
    lcd.print("White's Move");
  }
  else if(t == 1){
    lcd.clear();
    lcd.print("Black's Move");
  }
  else if(t == 2){
    lcd.clear();
    lcd.print("Game over!");
  }

  return;
}

//XY MOVEMENT FUNCTION
void xyMovement(int x, int y){ //moves end effector from home position to give x,y coordinates

  if(x > 0){
    digitalWrite(dirPin,HIGH);
    for(int i = 0; i < (x * 200); ++i){
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(800); 
    }
    delay(1000);
    digitalWrite(dirPin,LOW);
  }

  if(y > 0){
    digitalWrite(dirPin2,LOW);
    for(int j = 0; j < (y * 200); ++j){
      digitalWrite(stepPin2,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin2,LOW);
      delayMicroseconds(800); 
    }
    delay(1000);
    digitalWrite(dirPin2,HIGH);
  }
  return;  
}

//PIECEMOVEMENT
void pieceMovement(uint8_t x2,uint8_t y2){//called after a EM reaches a piece to move, doesn't account for if a piece already occupies destination
  //move the piece to the inbetween grid
  digitalWrite(relay_pin,HIGH);
  
  if(x < 7){
    digitalWrite(dirPin, HIGH);
  }
  else{
    digitalWrite(dirPin, LOW);
  }
    for(int i = 0; i < 120; ++i){
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(800); 
    }
    delay(1000);
  

  uint8_t yOffset;
  if(y2 >= y && y2 != 0){//move the end effector along the y direction between gridspaces
    yOffset = y2 - y;
    digitalWrite(dirPin2,LOW);
    for(int j = 0; j < (yOffset * 200); ++j){
      digitalWrite(stepPin2,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin2,LOW);
      delayMicroseconds(800); 
    }
    delay(1000);
    digitalWrite(dirPin2,HIGH);
    for(int j1 = 0; j1 < 100; ++j1){
      digitalWrite(stepPin2,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin2,LOW);
      delayMicroseconds(800);
    }
    delay(1000);
  }//end of if
  else if(y2 <= y && y2 != 7){
    yOffset = y - y2;
    digitalWrite(dirPin2,HIGH);
    for(int k = 0; k < (yOffset * 200); ++k){
      digitalWrite(stepPin2,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin2,LOW);
      delayMicroseconds(800); 
    }
    delay(1000);
    digitalWrite(dirPin2,LOW);
    for(int k1 = 0; k1 < 100; ++k1){
      digitalWrite(stepPin2,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin2,LOW);
      delayMicroseconds(800);
    }
    delay(1000);
  }//end of else if
  uint8_t xOffset;
  if(x2 >= x && x != 7){
    xOffset = x2 - x;
    digitalWrite(dirPin,HIGH);
    for(int l = 0; l < (xOffset * 200); ++l){
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(800); 
    }
    delay(1000);
    if(x < 7){
      digitalWrite(dirPin, LOW);
      for(int l1 = 0; l1 < 100; ++l1){
        digitalWrite(stepPin,HIGH);
        delayMicroseconds(800);
        digitalWrite(stepPin,LOW);
        delayMicroseconds(800);
      }
      delay(1000); 
    }
    else{
      digitalWrite(dirPin, HIGH);
      for(int l2 = 0; l2 < 100; ++l2){
        digitalWrite(stepPin,HIGH);
        delayMicroseconds(800);
        digitalWrite(stepPin,LOW);
        delayMicroseconds(800);
      }
      delay(1000); 
    }
  }
  else if(x2 <= x && x != 0){
    xOffset = x - x2;
    digitalWrite(dirPin, LOW);
    for(int i1 = 0; i1 < (xOffset * 200); ++i1){//PROBLEM AREA
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(800); 
    }
    delay(1000);
    if(x < 7){
      digitalWrite(dirPin, LOW);
      for(int m = 0; m < 100; ++m){
        digitalWrite(stepPin,HIGH);
        delayMicroseconds(800);
        digitalWrite(stepPin,LOW);
        delayMicroseconds(800); 
      }
      delay(1000);
    }
    else{
      digitalWrite(dirPin, HIGH);
      for(int m1 = 0; m1 < 100; ++m1){
        digitalWrite(stepPin,HIGH);
        delayMicroseconds(800);
        digitalWrite(stepPin,LOW);
        delayMicroseconds(800); 
      }
      delay(1000);
    }
  }
  if(y2 >= y && y2 != 0){
    digitalWrite(dirPin2,LOW);
    for(int m1 = 0; m1 < 100; ++m1){
      digitalWrite(stepPin2,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin2,LOW);
      delayMicroseconds(800); 
    }
    delay(1000);
  }
  else if(y2 <= y && y2 != 7){
    digitalWrite(dirPin2,HIGH);
    for(int m1 = 0; m1 < 100; ++m1){
      digitalWrite(stepPin2,HIGH);
      delayMicroseconds(800);
      digitalWrite(stepPin2,LOW);
      delayMicroseconds(800); 
    }
    delay(1000);
  }
  delay(50);
  digitalWrite(relay_pin,LOW);
  return;
}//END OF PIECEMOVEMENT

//PIECE TAKEN FUNCTION
void pieceTaken(){
  //engage magnet or maybe seperate helper function in state machine 
  digitalWrite(relay_pin,HIGH);
   //proceed to move piece onto edges
  if(y < 7){
    digitalWrite(dirPin2,LOW); //may need to switch
  }
  else{
    digitalWrite(dirPin2,HIGH);
  }
  for(int i = 0; i < 100; ++i){
    digitalWrite(stepPin2,HIGH);
    delayMicroseconds(800);
    digitalWrite(stepPin2,LOW);
    delayMicroseconds(800); 
  }
  delay(1000);
  //move piece along x axis until is off the board

  int xOffset = 7 - x;
  digitalWrite(dirPin,HIGH);
  for(int j = 0; j < ((xOffset * 200) + 180); ++j){
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(800);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(800); 
  }
  delay(1000);
  //disengage magnet and call recalibration helper function
  digitalWrite(relay_pin,LOW);
  return;
}

//recalibration system interrupts
void reachHomeX(){  
  flag1 = 1;
  return;
}

void reachHomeY(){
  flag2 = 1;
  return;
}

void recal(){
  digitalWrite(dirPin,LOW); // Enables the motor to move backwards
  digitalWrite(dirPin2,HIGH);

  flag1 = 0;
  flag2 = 0;
  
  while(flag1 == 0){
    digitalWrite(stepPin,HIGH);  
    delayMicroseconds(800);    
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(800); 
  }

  digitalWrite(dirPin,HIGH);
  for(uint8_t r = 0; r < 30; ++r){
    digitalWrite(stepPin,HIGH);  
    delayMicroseconds(800);    
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(800); 
  }

  while(flag2 == 0){
    digitalWrite(stepPin2,HIGH); 
    delayMicroseconds(800);    
    digitalWrite(stepPin2,LOW);
    delayMicroseconds(800); 
  }

  digitalWrite(dirPin2,LOW);
  for(uint8_t r1 = 0; r1 < 30; ++r1){
    digitalWrite(stepPin2,HIGH);  
    delayMicroseconds(800);    
    digitalWrite(stepPin2,LOW); 
    delayMicroseconds(800); 
  }
  
  return;
}

//task struct
typedef struct task {
  int state;
  unsigned long period;
  unsigned long elapsedTime;
  int (*TickFct)(int);
} task;

//creation of task object
const unsigned short tasksNum = 1; //FIXME
task tasks[tasksNum];


//Enumeration of Movement task's state
enum MV_states{MV_start, MV_wait, MV_button, MV_taken, MV_movePiece}MV_state;

void setup() {

  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(stepPin2,OUTPUT); 
  pinMode(dirPin2,OUTPUT);
  pinMode(relay_pin,OUTPUT);
  
  Serial.begin(9600);

  button.setDebounceTime(50);
  
  lcd.begin();
  lcd.backlight();
  lcd.print("Start Game?");

  attachInterrupt(digitalPinToInterrupt(18), reachHomeX, FALLING);
  attachInterrupt(digitalPinToInterrupt(19), reachHomeY, FALLING);

  type = ' ';

  flag1 = 0;
  flag2 = 0;
  digitalWrite(18,HIGH); 
  digitalWrite(19,HIGH);

  //set up MV tick function
  tasks[0].state = MV_start;
  tasks[0].period = 50;
  tasks[0].elapsedTime = 0;
  tasks[0].TickFct = &MV_TickFct;
}

int MV_TickFct(int state){
  button.loop();
  int pressed = button.isReleased();
  //Parsing string data
  if(Serial.available() > 0){
     data = Serial.readStringUntil('\n');
     type = data[0];
     if(type == 'm'){
      x2 = data[3] - numOffset;
      y2 = data[4] - '1';
     }
      x = data[1] - numOffset;
      y = data[2] - '1';
  }
  
  switch(state){//transitions for movement state machine
    case MV_start:
      if(pressed){
        state = MV_wait;
        changeLCD(0);
        delay(500);
        recal();
        delay(500);
      }
      else{
        state = MV_start;
      }
    break;

    case MV_wait:
      if(type == 't'){//FIXME
        state = MV_taken;  
      }
      else if(type == 'm'){//FIXME
        state = MV_movePiece;
      }
      else if(pressed){
        state = MV_button;
      }
      else{
        state = MV_wait;
      }
      break;

      case MV_button:
        state = MV_wait;
      break;

      case MV_taken:
        state = MV_wait;
      break;

      case MV_movePiece:
        state = MV_wait;
      break;

    default:
      state = MV_wait;
    break;
  }

  switch(state){//state actions for movement state machine
    case MV_start:
    break;

    case MV_wait:
    break;

    case MV_button:
      changeLCD(0);
      Serial.write("Black Turn Over");
    break;

    case MV_taken:
      xyMovement(x,y);//FIXME
      delay(500);
      pieceTaken();
      delay(500); 
      recal();
      type = ' ';
    break;

    case MV_movePiece:
      xyMovement(x,y);
      delay(500);
      pieceMovement(x2,y2);
      delay(500);
      recal();
      type = ' ';
      changeLCD(1);
    break;
    
  }

  return state;
}

void loop() {
  //input read

  

  for (int i = 0; i < tasksNum; ++i) {
    if ( (millis() - tasks[i].elapsedTime) >= tasks[i].period) {
      tasks[i].state = tasks[i].TickFct(tasks[i].state);
      tasks[i].elapsedTime = millis(); // Last time this task was ran
    }
  }//end of for loop
}
