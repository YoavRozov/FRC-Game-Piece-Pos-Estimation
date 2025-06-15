# Game Piece Position Estimation

This project is designed to capture frames from a camera, detect game pieces using color detection, estimate their positions, and send the data to a robot using a network connection. The application utilizes multi-processing to ensure efficient processing of the latest available data.

## Project Structure

```
game-piece-pos-estimation
├── RaspberryPiCode
│   ├── main.py                  # Entry point of the application
│   ├── frame_capture.py         # Class for capturing frames from the camera
│   ├── game_piece_detection.py   # Class for detecting game pieces in frames
│   ├── game_piece_pos_estimation.py # Class for estimating positions of detected game pieces
│   ├── network_manager.py        # Class for managing network connections and data publishing
├── requirements.txt              # List of dependencies
└── README.md                     # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd game-piece-pos-estimation
   ```

2. **Install dependencies**:
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:

```bash
python src/main.py
```

This will start the frame capture, game piece detection, position estimation, and network management processes.

## Dependencies

This project requires the following Python packages:

- OpenCV
- NumPy
- Pandas
- ntcore
- cscore

Make sure to install these packages using the `requirements.txt` file provided.

## License

This project is licensed under the AGPL-3.0 License. See the LICENSE file for more details.