import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    gz = get_package_share_directory('arm_gazebo')
    desc = get_package_share_directory('arm_description')
    rviz_cfg = os.path.join(desc, 'rviz', 'arm.rviz')
    rviz_args = ['-d', rviz_cfg] if os.path.exists(rviz_cfg) else []

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gz, 'launch', 'gazebo.launch.py'))),
        Node(package='rviz2', executable='rviz2', arguments=rviz_args,
             parameters=[{'use_sim_time': True}]),
    ])
