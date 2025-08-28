import RPi.GPIO as GPIO
import time
import serial

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.LOW)

try:
    ser = serial.Serial('/dev/rfcomm0', 9600, timeout=0.1)
except serial.SerialException:
    print("Failed to open /dev/rfcomm0")
    exit(1)

led_manual = False

try:
    while True:
        if GPIO.input(21) == GPIO.LOW:
            GPIO.output(20, GPIO.HIGH)
            led_manual = False
        else:
            if led_manual:
                GPIO.output(20, GPIO.HIGH)
            else:
                GPIO.output(20, GPIO.LOW)

        data = ser.readline().decode('utf-8').strip().upper()
        if data:
            print(f"Received: {data}")
            if data == "ON":
                led_manual = True
                GPIO.output(20, GPIO.HIGH)
                ser.write(b"LED ON\r\n")
            elif data == "OFF":
                led_manual = False
                GPIO.output(20, GPIO.LOW)
                ser.write(b"LED OFF\r\n")
            elif data == "EXIT":
                ser.write(b"BYE\r\n")
                break
            else:
                ser.write(b"UNKNOWN COMMAND\r\n")

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    GPIO.output(20, GPIO.LOW)
    GPIO.cleanup()
    ser.close()

