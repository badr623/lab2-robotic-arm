from setuptools import find_packages, setup

package_name = 'arm_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='badr',
    maintainer_email='ايميلك@example.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'hardware_bridge = arm_control.hardware_bridge:main',
            'hardware_bridge = arm_control.hardware_bridge:main',
            'slider_gui = arm_control.slider_gui:main',
            'hardware_bridge = arm_control.hardware_bridge:main',
            'trajectory_publisher = arm_control.trajectory_publisher:main',
        ],
    },
)
