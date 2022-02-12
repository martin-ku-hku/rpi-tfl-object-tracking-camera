# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)


class Servo():
    def __init__(self, pin, freq=50):
        self.pin = pin
        self.freq = freq
        self.started = False

    def start(self):
        GPIO.setup(self.pin, GPIO.OUT)
        self.output = GPIO.PWM(self.pin, self.freq)
        self.output.start(0)
        self.started = True
        print("Start sending signal to the servo.")

    def set_angle(self, angle):
        if not self.started:
            print('The servo has not started sending signal.')
            return
        if angle < 0 or angle > 180:
            raise ValueError('The angle must be between 0 and 180')
        self.output.ChangeDutyCycle(2+(angle/18))
        time.sleep(0.5)
        self.output.ChangeDutyCycle(0)

    def end(self):
        if self.started:
            self.started = False
            self.output.stop()
            GPIO.cleanup()
            print("Stop sending signal to the servo.")

    def __del__(self):
        self.end()


def main():
    try:
        # Set pin 11 as an output, and pulse 50Hz
        servo = Servo(11, 50)
        # Let the Raspberry Pi send signal to the servo motor
        servo.start()
        while True:
            try:
                # Ask user for angle and turn servo to it
                angle = float(input('Enter angle between 0 & 180: '))
                # Set the angle
                servo.set_angle(angle)
            except ValueError as e:
                print(e)
                continue
    except KeyboardInterrupt:
        # Press Ctrl+C to end the program
        print("End of program.")
    finally:
        # Cleanup at the end of the program
        if servo.started:
            servo.end()


if __name__ == "__main__":
    main()
