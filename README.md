# AirhockeyAI

AirHockey Branch contains main code

Edward Zhang Eric Feng
Senior Research Project - Yilmaz Period 6
https://www.youtube.com/watch?v=zZiMVUovUpY&feature=youtu.be

## File Directory 

/.ipynb_checkpoints -> Gym Envrioment Version 1 on Jupyter Notebook

/HOCKEY2 -> Mainm repository for the genetic algorihim code and adapter physics siimulation

/Training -> Saved model folders

/detection -> Preliminary CV detection algorihtim with hough transform, updated dual detection CV algirhtim is under /HOCKEY2

/gym_Game -> First version of OpenAI Gym game. Updated version is adapted found under /HOCKEY2

/motor_driver -> Serial command translations from python code to Arduino Leonardo Motor Sheild
To run the motors according to your computer's WASD keys, connect your machine to the arduino and compile and upload the arduino code /dc_motor.ino file. Identify the PORT that the arduino is connected to via USB. This can be found by going to tools on the arduino ide. Update the port address in the motor driver file. On a ubuntu machine, the port used is in the form '/dev/ttyACM0'. After uploading the code, run python3 motor_drive.py. On Linux machines, this requires sudo permissions so run sudo python3 motor_drive.py and follow the prompt.

/neatalgo -> NEAT algorithim class declarations

## How To Run Code

Main directory is under /HOCKEY2. Run main.py to see the simulation and play of the AI NEAT agent


