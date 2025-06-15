import multiprocessing as mp
import cv2
import numpy as np
import pandas as pd
from frame_capture import FrameCapture
from game_piece_detection import ColorDetection
from game_piece_pos_estimation import GamePiecePosEstimator
from network_manager import NetworkManager

def frame_capture_process(queue : mp.Queue, camera_id : int, resolution : tuple[int, int], fps : int):
    frame_capture = FrameCapture(camera_id, resolution, fps)
    while True:
        frame, timestamp = frame_capture.capture_frame()
        if not queue.full():
            queue.put((frame, timestamp))

def detection_process(queue : mp.Queue, detection_queue : mp.Queue, lower_bound : np.ndarray, upper_bound : np.ndarray):
    color_detection = ColorDetection(lower_bound, upper_bound)
    while True:
        if not queue.empty():
            frame, timestamp = queue.get()
            rect = color_detection.detect_color(frame)
            if rect is None:
                continue
            if not detection_queue.full():
                detection_queue.put((rect, timestamp))

def position_estimation_process(detection_queue : mp.Queue, position_queue : mp.Queue, estimator_data : pd.DataFrame):
    estimator = GamePiecePosEstimator(1280, 720, estimator_data)
    while True:
        if not detection_queue.empty():
            rect, timestamp = detection_queue.get()
            position = estimator.estimate_position(rect)
            if position is None:
                continue
            if not position_queue.full():
                position_queue.put((position, timestamp))

def network_management_process(position_queue : mp.Queue, team_number : int):
    network_manager = NetworkManager(team_number)
    while True:
        if not position_queue.empty():
            position, timestamp = position_queue.get()
            x, y, certainty = position[0], position[1], position[2]
            network_manager.publish_game_piece_position(x, y, 0, certainty)

            # When the game piece is non-symmetrical, you can pass the rotation angle as well
            # network_manager.publish_game_piece_position(x, y, rotation_angle, certainty)
        else:
            # If no position is available, you can publish a default value or wait
            network_manager.publish_game_piece_position(0, 0, 0, 0)


def main():
    camera_id = 0
    
    # Camera resolution and FPS settings
    resolution = (1280, 720)
    camera_fps = 120

    lower_bound = np.array([9, 35, 0])  # Example lower bound for color detection
    upper_bound = np.array([31, 255, 255])  # Example upper bound for color detection

    # Team number for network management
    team_number = 5554  # Team number

    frame_queue = mp.Queue(maxsize=1)
    detection_queue = mp.Queue(maxsize=1)
    position_queue = mp.Queue(maxsize=1)

    # Load estimator data (example data)
    estimator_data = pd.read_csv('Data/2024-Note/FullData.csv')

    processes = [
        mp.Process(target=frame_capture_process, args=(frame_queue, camera_id, resolution, camera_fps)),
        mp.Process(target=detection_process, args=(frame_queue, detection_queue, lower_bound, upper_bound)),
        mp.Process(target=position_estimation_process, args=(detection_queue, position_queue, estimator_data)),
        mp.Process(target=network_management_process, args=(position_queue, team_number))
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    main()