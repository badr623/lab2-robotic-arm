import tkinter as tk

import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

JOINTS = ['joint1', 'joint2', 'joint3', 'joint4']
LIMIT = 1.5708  # +-90 degrees, same as the URDF limits


class SliderPublisher(Node):
    def __init__(self):
        super().__init__('slider_gui')
        self.pub = self.create_publisher(
            JointTrajectory, '/arm_controller/joint_trajectory', 10)

    def send(self, positions):
        msg = JointTrajectory()
        msg.joint_names = JOINTS
        point = JointTrajectoryPoint()
        point.positions = [float(p) for p in positions]
        point.time_from_start = Duration(sec=0, nanosec=300_000_000)
        msg.points.append(point)
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = SliderPublisher()

    root = tk.Tk()
    root.title('Arm Sliders')
    variables = []

    def publish(_=None):
        node.send([v.get() for v in variables])

    def home():
        for v in variables:
            v.set(0.0)
        publish()

    for name in JOINTS:
        v = tk.DoubleVar(value=0.0)
        tk.Scale(root, label=f'{name} (rad)', from_=-LIMIT, to=LIMIT,
                 resolution=0.01, orient=tk.HORIZONTAL, length=320,
                 variable=v, command=publish).pack(padx=10, pady=4)
        variables.append(v)

    tk.Button(root, text='Home (all 0)', command=home).pack(pady=8)

    root.mainloop()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
