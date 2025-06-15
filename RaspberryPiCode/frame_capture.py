import time
import cv2

class FrameCapture:
    """
    A class used to capture frames from a specific camera.
    Attributes
    ----------
    camera_id : int
        The camera index (used with OpenCV)

    camera_resolution : tuple[int, int]
        The desired resolution for the camera to capture

    target_fps : int
        The desired FPS of the camera

    Methods
    -------
    capture_frame() -> tuple[cv2.Mat, float]
        Captures a frame from the camera and returns it along with the timestamp
    """

    def __init__(self, camera_id : int, camera_resolution : tuple[int, int], target_fps : int):
        """
        A class used to capture frames from a specific camera

        Attributes
        ----------
        camera_id : int
            The camera index (used with open cv)
        
        camera_resolution: tuple[int, int]
            The desired resolution for the camera to capture
        
        target_fps : int
            The desired fps of the camera

        Methods
        -------
        capture_frame(queue)
            Starts frame capture on the camera
        """
        self.camera_id = camera_id
        print("Initializing camera with ID:", camera_id)
        self.cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_resolution[1])
        self.cap.set(cv2.CAP_PROP_FPS, target_fps)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
    
    def capture_frame(self) -> tuple[cv2.Mat, float]:
        """
        Captures a frame from the camera and returns it along with the timestamp
        Returns
        -------
        tuple[cv2.Mat, float]
            The captured frame and the timestamp of when it was captured
        """
        while True:
            start_time = time.time()
            ret, frame = self.cap.read()
            if ret:
                print("FPS:", 1 / (time.time() - start_time))
                return (frame, start_time)
