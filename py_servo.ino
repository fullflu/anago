#include <Servo.h>
#include <math.h>

int servo_count = 3;
Servo servo[3];

typedef struct ServoWeight {
  float forward; // 動かすサーボのうち前サーボの重み
  float back; // 動かすサーボのうち，後ろサーボの重み
} ServoWeight;

// 使うサーボが1個の時の重み
ServoWeight weight[3];
// 使うサーボが2個の時の重み
ServoWeight weight2[3];

//now skip the definition of the value of servo_Weight
//servo_weight should be multiplied by pos as below
//servo[stan].write(pos);
//servo[change].write(pos * change_servo_weight * change_deg_weight);

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
double deg_rad = 0.0;//degree transformed to radian
int stan = 0;//servo number whose pos is not adjusted
int change = 1;//servo number whose pos is adjusted
double change_deg_weight = 0.0;//weight to adjust pos of change servo
double change_servo_weight = 0.0;

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    deg = 2 * Serial.read();//get the direction for anago to go to
    stop_servo = !stop_servo;
    i = deg / 120;//get the number of left servo to move
  }
  if (stop_servo) return;
  deg_rad = double((deg - 120 * i) * PI / 180.0);//;
  if (deg_rad < PI / 3.0){
    stan = i; 
    change = (i + 1) % servo_count;
    change_deg_weight = sin(deg_rad) / sin(2 * PI / 3.0 - deg_rad);
    //change_servo_weight = ,,,;
  }
  else{
    stan = (i + 1) % servo_count;
    change = i;
    change_deg_weight = sin(2 * PI / 3.0 - deg_rad) / sin(deg_rad);
    //change_servo_weight = ,,,;
  }
  for(pos = 0; pos <= 180; pos += 1){
    //adjust pos by degree
    servo[change].write(int(pos * change_deg_weight));
    servo[stan].write(pos);
    delay(delay_duration);
  }
  for(pos = 180; pos >= 0; pos -= 1){
    //adjust pos by degree
    servo[change].write(int(pos * change_deg_weight));
    servo[stan].write(pos);
    delay(delay_duration);
  }
  delay(delay_duration);
}
