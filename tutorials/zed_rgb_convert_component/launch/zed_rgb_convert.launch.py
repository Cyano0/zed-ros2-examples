import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Define LaunchDescription variable
    ld = LaunchDescription()

    # use:
    #  - 'zed' for "ZED" camera
    #  - 'zedm' for "ZED mini" camera
    #  - 'zed2' for "ZED2" camera
    camera_model = 'zed2'

    # Camera name
    camera_name = 'zed2'

    # URDF file to be loaded by Robot State Publisher
    urdf = os.path.join(
        get_package_share_directory('zed_wrapper'),
        'urdf', camera_model + '.urdf'
    )

    # ZED Configurations to be loaded by ZED Node
    config_common = os.path.join(
        get_package_share_directory('zed_wrapper'),
        'config',
        'common.yaml'
    )

    config_camera = os.path.join(
        get_package_share_directory('zed_wrapper'),
        'config',
        camera_model + '.yaml'
    )

    # Set LOG format
    os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = '{time} [{name}] [{severity}] {message}'

    # Robot State Publisher node
    rsp_node = Node(
        package='robot_state_publisher',
        node_namespace="/"+camera_name,
        node_executable='robot_state_publisher',
        node_name=camera_name+'_state_publisher',
        output='screen',
        arguments=[urdf],
    )

    # ZED node using manual composition
    zed_node = Node(
        package='zed_rgb_convert',
        node_namespace="/"+camera_name,
        node_executable='zed_rgb_convert',
        output='screen',
        parameters=[
            config_common,  # Common parameters
            config_camera,  # Camera related parameters
        ],
        remappings=[
            ("zed_image_4ch", "zed_node/rgb/image_rect_color"),
            ("camera_info", "zed_node/rgb/camera_info")
        ]
    )

    # Add nodes to LaunchDescription
    ld.add_action(rsp_node)
    ld.add_action(zed_node)

    return ld
