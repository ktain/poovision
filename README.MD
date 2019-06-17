# Welcome to the Poo Vision Github!

This github repository was made to document our embedded systems design project for CSE 145 at UC San Diego. The repository will contain our class presentations, assignments, code files, mechanical design files, and other relevant documentation.

The team members of this project are:

Richard Chum (Computer Engineering)

Derek Lam (Electrical Engineering)

Kevin Tain (Computer Engineering)


## Project Overview

The Brilliant Pad is a device that has the purpose of being an automated potty for dogs. Our class project is to improve the Brilliant Pad device by adding a vision system through extra components such as a camera to increase its ability to detect a dog on the pad and to allow the pad to determine how soiled it is ie. 10%, 20% soiled. With this vision system, the Brilliant Pad will be able to automatically advance a soiled pad given a threshold of soiledness.

## Project Approach
We are using a Raspberry Pi Zero and a Pi Zero Camera to detect waste on the BrilliantPad. Using a widely available computer vision library, OpenCV, we aim to use the image output of our Camera module to distinguish between a clean pad and a dirty pad, and to detect when a dog is present on the pad. The overall goal is to integrate our system with the Brilliant Pad’s current control module and design.

## Key Milestones

Below are the key milestones and objectives that our team has established for the Brilliant Pad Poo Vision. Each milestone has its own deliverable that must be delivered.

### Key Milestone 1 - Create and design mechanical prototypes to mount the Camera on the Brilliant Pad
_Definition:_ Mock-ups of the mount

_Deliverable:_ Pictures of the mount setup on the Brilliant Pad  

### Key Milestone 2 - Web Presence and Documentation
_Definition:_ Create a “web presence” and document all required information about our project. Goal is to also document information well for the Brilliant Pad company.

_Deliverable:_ Accessible webpage

### Key Milestone 3 - Gathering and Analyzing Information of the Pad
_Definition:_ Image processing

_Deliverable:_ A video demonstration of the camera capturing a picture and processing it into relevant information needed for the pad.

### Key Milestone 4 - Communicate with Brilliant Pad
_Definition:_ Using UART to tell the Brilliant Pad to advance the pad

_Deliverable:_ A full working product that can detect the dog and how soiled the pad is, and advance the pad


