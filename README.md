# OpenGL_learning
  
Here will be found an explanation of the content of this repository as well as which packages will be needed to run this project.  

# Content
This project is composed of two git branches:  
  - The Master branch contains a working version on the project. In its actual state, you will found a 3D cube in an empty environment and a camera that can move in the 3D space with keyboard and mouse.  
  ***for this version to work, you will need pyOpenGL, pygame and numpy to be installed in your python environment***
  - The develop branch contains the same project but pygame has been entirely replaced by GLFW to that its no longer needed.
  ***for this version to work, you will need pyOpenGL, GLFW, GLM and numpy to be installed in your python environment***
  > ***please NOTE that the content of the develop branch is a susceptible to change and may not work until it's been pushed to the master branch***
****

# Master Branch update history:
### V0.1:
A 3D empty space with **a cube** in the center.
By modifying the code, the following can be drawn:
  - a full cube
  - only its edges
  - only its vertices
  - the X, Y and Z axis
  - a grey 2D plane   
By modifying the code, two cameras can be chosen:
  - a fixed one where mouse click + motion will rotate the 3D object and mouse wheel will zoom in and out
  - a *Free camera* which will rotate with the mouse motion and move with keyboard inputs.  
  
Needed packages: ***pyOpenGL***, ***pygames***, ***numpy***

### V0.1.2
This version is an improvement of the previous one. 
The fixed camera have been removed and only a full cube and a triangle are displayed (both together)  
Backface Culling has been enabled to avoid displaying triangles that aren't facing the camera.
Pygame is no longer used and has been replaced by GLFW.  
Introducing GLM and matrices are now computed manually.  
