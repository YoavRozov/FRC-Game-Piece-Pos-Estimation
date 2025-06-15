import ntcore
from cscore import CameraServer
from cv2 import Mat
import time

class NetworkManager:
    """
    A class used to manage the network connection and camera setup for a robot.
    Attributes
    ----------
    team_number : int
        The team number of the robot, used to determine the robot's IP address.

    robot_ip : str
        The IP address of the robot, formatted as "team_number.local".

    nt : ntcore.NetworkTableInstance
        The NetworkTable instance used for communication.

    data_table : ntcore.NetworkTable
        The NetworkTable used to store and retrieve data.
        
    camera_publisher : cscore.VideoSink
        The publisher for the camera stream.

    topics : dict
        A dictionary of topics for publishing data to the NetworkTable.

    publishers : dict
        A dictionary of publishers for the topics defined in `topics`.

    Methods
    -------
    setup_camera(camera_name: str)
        Sets up the camera with the specified name and resolution.
    publish_image(image: Mat)
        Publishes an image to the camera stream.
    setup_topics()
        Sets up the topics for publishing data to the NetworkTable.
    game_piece_position(x: float, y: float, a: float, certainty: float = 0.0)
        Publishes the robot's position and certainty to the NetworkTable.
    """

    def __init__(self, team_number : int):
        self.robot_ip = str(team_number) + ".local"  # Assuming the robot's IP is in the format "team_number.local"
        
        print("Setting up NetworkManager...")
        print("Robot IP:", self.robot_ip)
        self.nt = ntcore.NetworkTableInstance.getDefault()

        print('Setting up NetworkTable named: "datatable"...')
        self.data_table = self.nt.getTable("datatable")
        print("NetworkTable setup complete.")

        self.setup_camera("Camera")
        print("Camera setup complete.")

        print("Setting up topics...")
        self.setup_topics()
        print("Topics setup complete.")

        self.nt.startClient4("raspberrypi_" + str(team_number))
        self.nt.setServerTeam(team_number, 0) # where TEAM=5554, 294, 1690, etc
        print("Starting NetworkTable client...")
        time.sleep(3) # Wait for the client to start Recommended by the library
        print("NetworkTable client started.")

    def setup_camera(self, camera_name):
        """ Sets up the camera on the robot. """
        print("Setting up camera stream...")
        self.camera_publisher = CameraServer.putVideo(camera_name, 640, 480) # Set the resolution to 640x480 to reduce CPU usage and bandwidth
        self.camera_publisher.setFPS(15) # Limit the FPS to 15 to limit CPU usage and bandwidth
    
    def publish_image(self, image : Mat):
        """ Publishes an image to the camera stream. """
        self.camera_publisher.putFrame(image)

    def setup_topics(self):
        self.topics = {
            "game_piece_position_x" : self.data_table.getDoubleTopic("game_piece_position_x"),
            "game_piece_position_y" : self.data_table.getDoubleTopic("game_piece_position_y"),
            "game_piece_yaw" : self.data_table.getDoubleTopic("game_piece_yaw"),
            "certainty" : self.data_table.getDoubleTopic("certainty")
        }

        self.publishers = {
            "game_piece_position_x" : self.topics["game_piece_position_x"].publish(),
            "game_piece_position_y" : self.topics["game_piece_position_y"].publish(),
            "game_piece_yaw" : self.topics["game_piece_yaw"].publish(),
            "certainty" : self.topics["certainty"].publish()
        }        

    def publish_game_piece_position(self, x, y, a, certainty=0.0):
        """ Publishes the game piece's position to the NetworkTable. """
        timestamp = ntcore._now()
        self.publishers["game_piece_position_x"].set(x, timestamp)
        self.publishers["game_piece_position_y"].set(y, timestamp)
        self.publishers["game_piece_yaw"].set(a, timestamp)
        self.publishers["certainty"].set(certainty, timestamp)