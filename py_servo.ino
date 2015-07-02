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

/*
union u_tag {
    byte b[1];
    struct {
        unsigned long pitch_val;
        //unsigned long dur_val;
    };
} u;
*/
    
int i = 0;
int pos = 0;
int deg = 0;
int deg_weighted_pos = 0;
int delay_duration = 70;
bool stop_servo = 0;
void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    deg = 2 *Serial.read();//get the direction for anago to go to
    stop_servo = !stop_servo;
    i = deg / 120;
  }
  if (stop_servo) return;
  for(pos = 0; pos <= 180; pos += 1){
    deg_weighted_pos = int(double(pos) * double(deg) / double((120 * (i + 1))));//resume pos by degree
    servo[i].write(pos - deg_weighted_pos);
    servo[(i + 1) % servo_count].write(deg_weighted_pos);
    delay(delay_duration);
  }
  for(pos = 180; pos >= 0; pos -= 1){
    deg_weighted_pos = int(double(pos) * double(deg) / double((120 * (i + 1))));//resume pos by degree
    servo[i].write(pos - deg_weighted_pos);
    servo[(i + 1) % servo_count].write(deg_weighted_pos);
    delay(delay_duration);
  }
  delay(delay_duration);
}
