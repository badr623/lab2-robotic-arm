import math
import time

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory

JOINTS = ['joint1', 'joint2', 'joint3', 'joint4']


class HardwareBridge(Node):
    def __init__(self):
        super().__init__('hardware_bridge')
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud', 115200)
        port = self.get_parameter('port').value
        baud = self.get_parameter('baud').value

        self.angles = [90] * len(JOINTS)
        self.ser = None
        try:
            import serial
            self.ser = serial.Serial(port, baud, timeout=0.1)
            time.sleep(2.0)  # Arduino Uno resets when the port opens
            self.get_logger().info(f'Connected to {port} @ {baud}')
        except Exception as e:
            self.get_logger().warn(
                f'Cannot open {port} ({e}). Dry-run mode: printing only.')

        self.create_subscription(
            JointTrajectory, '/arm_controller/joint_trajectory', self.callback, 10)

    def callback(self, msg):
        if not msg.points:
            return
        target = msg.points[-1].positions
        for name, pos in zip(msg.joint_names, target):
            if name in JOINTS:
                deg = 90.0 + math.degrees(pos)
                self.angles[JOINTS.index(name)] = int(round(min(180.0, max(0.0, deg))))
        line = ','.join(str(a) for a in self.angles) + '\n'
        if self.ser is not None:
            self.ser.write(line.encode())
        self.get_logger().info(f'Sent: {line.strip()}')


def main(args=None):
    rclpy.init(args=args)
    node = HardwareBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    if node.ser is not None:
        node.ser.close()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
