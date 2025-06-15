# Use color or ML to detect game pieces on a Raspberry Pi
# In this example, I will use color detection to find game pieces
import cv2
import numpy as np

class ColorDetection:
    """
    A class used to detect game pieces in the image using color detection
    Attributes
    ----------
    lower_bound : numpy array
        The lower hsv color bound for the game piece
    upper_bound: numpy array
        The upper hsv color bound for the game piece
    Methods
    -------
    findMask(img: cv2.Mat) -> cv2.Mat
        Finds the mask of the image based on the lower and upper bounds
    find_rectangle(contour: np.ndarray) -> tuple[int, int, int, int]
        Finds the bounding rectangle of a contour
    detect_color(frame: cv2.Mat) -> np.ndarray
        Detects game pieces in the given frame using color detection
    """

    def __init__(self, lower_bound : np.ndarray, upper_bound : np.ndarray):
        """
        A class used to detect game objects in the image

        Attributes
        ----------
        lower_bound : numpy array
            The lower hsv color bound
        
        upper_bound: numpy array
            The upper hsv color bound

        Methods
        -------
        detect_color(frame, queue)
            Detects object in the given frame using mainly color
        """
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
    
    def findMask(self, img : cv2.Mat) -> cv2.Mat:
        """
        Finds the mask of the image based on the lower and upper bounds
        Parameters
        ----------
        img : cv2.Mat
            The image to find the mask of
        Returns
        -------
        cv2.Mat
            The mask of the image
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)

        # Define the kernel for the morphological operation
        # It is a 7*7 2d array of ones
        # Try changing the size of the kernel to see how it affects the image
        kernel = np.ones((7, 7), np.uint8)

        # Perform morphological opening to remove noise
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Perform morphological closing to close small holes
        processed_mask = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        return processed_mask
    
    def find_rectangle(self, contour : np.ndarray) -> tuple[int, int, int, int]:
        """
        Finds the bounding rectangle of a contour

        Parameters
        ----------
        contour : np.ndarray
            The contour to find the bounding rectangle of

        Returns
        -------
        tuple[int, int, int, int]
            The x, y, width, and height of the bounding rectangle
        """
        x, y, w, h = cv2.boundingRect(contour)
        return (x, y, w, h)

    def detect_color(self, frame : cv2.Mat) -> np.ndarray:
        """
        Detects game pieces in the given frame using color detection

        Parameters
        ----------
        frame : cv2.Mat
            The frame to detect game pieces in
        """
        mask = self.findMask(frame)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If no contours are found, return a rectangle with all zeros
        if not contours:
            return None

        contour = max(contours, key=cv2.contourArea)
        rect = self.find_rectangle(contour)
        x, y, w, h = rect

        return np.array([x, y, w, h], dtype=np.int32)