## Install All the Modules
sudo apt update
sudo apt upgrade

# Python3 related packages must be installed if you are installing the Lite version OS.
sudo apt install -y git python3-pip python3-setuptools python3-smbus

# Install robot-hat.
cd /home/pi/
git clone https://github.com/sunfounder/robot-hat.git
cd robot-hat
sudo python3 setup.py install

# Then download and install the vilib module.
cd /home/pi/
git clone https://github.com/sunfounder/vilib.git
cd vilib
sudo python3 install.py

# Download and install the picar-x module.
cd /home/pi/
git clone -b v2.0 https://github.com/sunfounder/picar-x.git
cd picar-x
sudo python3 setup.py install

# Run the script i2samp.sh to install the components required by the i2s amplifier
cd /home/pi/picar-x
sudo bash i2samp.sh
