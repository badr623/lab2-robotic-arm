import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

JOINTS = ['joint1', 'joint2', 'joint3', 'joint4']


class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')
        self.pub = self.create_publisher(
            JointTrajectory, '/arm_controller/joint_trajectory', 10)
        self.poses = [
            [0.0, 0.0, 0.0, 0.0],
            [1.0, 0.5, 0.5, 0.0],
            [-1.0, -0.5, 0.8, 0.5],
            [0.0, 0.0, 0.0, 0.0],
        ]
        self.i = 0
        self.timer = self.create_timer(4.0, self.step)
        self.get_logger().info('Publishing poses every 4 s')

    def step(self):
        msg = JointTrajectory()
        msg.joint_names = JOINTS
        point = JointTrajectoryPoint()
        point.positions = self.poses[self.i]
        point.time_from_start = Duration(sec=2, nanosec=0)
        msg.points.append(point)
        self.pub.publish(msg)
        self.get_logger().info(f'Pose {self.i}: {point.positions}')
        self.i = (self.i + 1) % len(self.poses)


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
