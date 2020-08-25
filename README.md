# auto_apply_body_wrench
This package reads the /clock topic to obtain sim_time, and applies the predefined force according to sim_time. You can change some parameters in the script to adjust the force test you want.

## Setup
1. Download the package repo
2. Link the pakage in srv folder of your workspace, such as
   $ ln -s ~/Documents/anymal/auto_apply_body_wrench ~/Documents/alma_ws/src
3. In the workspace, build the package
   $ catkin build auto_apply_body_wrench
4. Source the path
   $ source ~/Documents/alma_ws/devel/setup.bash
Note: If the system cannot find a python file, run the command below to change python script
   $ chmod +x auto_apply_body_wrench.py

## Run the simulaiton
1. Ensure you source the path
   $ source /opt/ros/melodic/setup.bash
   $ source ~/Documents/alma_ws/devel/setup.bash
2. In one terminal, run the simulation
   $ roslaunch alma_sim sim.launch
3. Once the simulaiton is up, click the play button of "/alma_opt_controller" on the panel.
4. Click the play button of "walk"
3. In another terminal, run
   $ rosrun auto_apply_body_wrench auto_apply_body_wrench.py


## The parameter you might want to revise
You can change some parameters in the script to specify your force test.

test_start_time: the sim time in secs that starts applying force
test_period: duration for each predefined force
body_name: the link that force applied on
force: the 2D array that predefines the forces. The number of the force can be changed.
