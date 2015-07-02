#include <Servo.h>

int servo_count = 3;
Servo servo[3];

typedef struct ServoWeight {
  float right; // バネの右側に位置するサーボの重み
  float left; // バネの左側に位置するサーボの重み
} ServoWeight;

// 使うサーボが1個の時の重み
ServoWeight weight[3];
// 使うサーボが2個の時の重み
ServoWeight weight2[3];

//now skip the definition of the value of servo_Weight
//servo_weight should be multiplied by pos as below
//servo[i].write(left * (pos - deg_weighted_pos));
//servo[(i + 1) % servo_count].write(right * (deg_weighted_pos));

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo[0].attach(2);
  servo[0].write(0);
  servo[1].attach(4);
  servo[1].write(0);
  servo[2].attach(3);
  servo[2].write(0);
  delay(2000);
}

int i = 0;
int pos = 0;
int deg = 0;
int delay_duration = 70;
bool stop_servo = 0;
double deg_weight = 0.0;//weight of degree [0,1)
int stan = 0;//servo number whose pos is not adjusted
int change = 1;//servo number whose pos is adjusted
double change_weight = 0.0;//weight to adjust pos of change servo

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    deg = 2 * Serial.read();//get the direction for anago to go to
    stop_servo = !stop_servo;
    i = deg / 120;//get the number of left servo to move
  }
  if (stop_servo) return;
  deg_weight = double((deg - 120 * i)) / 120.0;
  if (deg_weight < 0.5){
    stan = i; 
    change = (i + 1) % servo_count;
    change_weight = deg_weight / (1 - deg_weight);
  }
  else{
    stan = (i + 1) % servo_count;
    change = i;
    change_weight = (1 - deg_weight) / deg_weight;
  }
  for(pos = 0; pos <= 180; pos += 1){
    //adjust pos by degree
    servo[change].write(int(pos * change_weight));
    servo[stan].write(pos);
    delay(delay_duration);
  }
  for(pos = 180; pos >= 0; pos -= 1){
    //adjust pos by degree
    servo[change].write(int(pos * change_weight));
    servo[stan].write(pos);
    delay(delay_duration);
  }
  delay(delay_duration);
}
