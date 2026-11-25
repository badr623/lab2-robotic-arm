# Robotic Arm: URDF, Simulation and Hardware Control (ROS 2 Jazzy)

A 4-joint robotic arm modelled in URDF, simulated in Gazebo (gz sim) and RViz2,
controlled through `/arm_controller/joint_trajectory`, and bridged to real servos
through an Arduino Uno.

## Packages (`src/`)
| Package | Purpose |
|---|---|
| `arm_description` | URDF/xacro model (4 revolute joints, visual/collision/inertial on all links) |
| `arm_gazebo` | Gazebo world, ros2_control config (`controllers.yaml`), Gazebo launch |
| `arm_control` | `trajectory_publisher`, `slider_gui`, `hardware_bridge` nodes |
| `arm_bringup` | `sim.launch.py` (Gazebo + RViz2) |

Firmware: `firmware/arm_servo/arm_servo.ino`

## Dependencies
Ubuntu 24.04, ROS 2 Jazzy.
```bash
sudo apt install ros-jazzy-xacro ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-ros-gz ros-jazzy-gz-ros2-control ros-jazzy-ros2-controllers \
  ros-jazzy-rviz2 python3-tk python3-serial
sudo usermod -aG dialout $USER   # then log out and in (serial access)
```

## Build
```bash
git clone <this-repo> lab2_ws && cd lab2_ws
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
```

## Run
Each command in its own terminal (run `source install/setup.bash` in each):
```bash
ros2 launch arm_bringup sim.launch.py      # Gazebo + RViz2
ros2 run arm_control slider_gui            # slider GUI -> /arm_controller/joint_trajectory
ros2 run arm_control hardware_bridge       # sends angles to the Arduino
# optional: automatic demo motion instead of the GUI
ros2 run arm_control trajectory_publisher
```
In RViz2 the fixed frame is `base_link` with a RobotModel display (`/robot_description`).
If the Arduino is not on `/dev/ttyACM0`:
`ros2 run arm_control hardware_bridge --ros-args -p port:=/dev/ttyACM1`.
Without a board connected, the bridge runs in dry-run mode and only prints what it would send.

## Hardware communication
- **Transport:** USB serial, 115200 baud (pyserial on the PC).
- **Message format:** one text line per command, 4 comma-separated integers
  (degrees, 0-180, one per joint in order joint1..joint4), ending with `\n`.
  Example: `90,120,45,90\n`
- **Conversion:** `servo_deg = 90 + degrees(joint_rad)`, clamped to 0-180
  (0 rad = 90 deg, the URDF limits of +-1.5708 rad map to 0 and 180 deg).
- **Firmware:** parses the line, ignores malformed lines, clamps again, drives the servos with the Servo library.

## Wiring (Arduino Uno)
| Board pin | Connects to |
|---|---|
| D3 | Servo 1 signal (joint1, base rotation) |
| D5 | Servo 2 signal (joint2) |
| D6 | Servo 3 signal (joint3) |
| D9 | Servo 4 signal (joint4) |
| GND | GND of the external 5 V servo supply (common ground) |

Servo red wires go to the external 5 V supply, not the Uno 5 V pin.
