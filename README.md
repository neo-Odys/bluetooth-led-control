# bluetooth-led-control

sudo apt update
sudo apt install bluez
sudo systemctl stop bluetooth
sudo /usr/sbin/bluetoothd -C &
sudo sdptool add SP
sudo sdptool browse local
sudo rfcomm watch hci0 1

python3 -m venv venv
source venv/bin/activate
pip3 install RPi.GPIO pyserial
