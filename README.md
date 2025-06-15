# Game Piece Position Estimation

This project provides a complete pipeline and full source code for a novel algorithm for object pose estimation, specifically designed for FRC (FIRST Robotics Competition) game pieces. The approach is based on a data-driven, image-matching method that enables extremely fast and accurate estimation of object positions from camera images.

## Key Features

- **Extremely Fast and Accurate**: The algorithm leverages a precomputed dataset of rendered images and their corresponding real-world positions, allowing for rapid and robust pose estimation at runtime.
- **Full Source Code and Explanations**: The repository includes all Python source code and detailed explanations of the algorithm, data generation, and processing steps.
- **Pipeline Architecture**: Utilizes multi-processing to maximize throughput, ensuring the latest camera data is always processed and stale data is discarded.
- **FRC-Ready**: Designed for use on Raspberry Pi or similar hardware, with integration for FRC networking (NetworkTables).

## How It Works

1. **Preprocessing (Offline, One-Time)**
   - Use Blender to render thousands of images of the game piece from all relevant positions and angles, with known camera parameters (The provided Blender Files include rendering scripts).
   - Each image is annotated with its real-world position and orientation (If the game piece is non-symmetrical).
   - The resulting dataset is stored as a CSV file.

2. **Runtime (On-Robot)**
   - Capture frames from a fixed-position camera.
   - Detect the game piece in the image using color or ML-based detection.
   - Extract the bounding rectangle (and optionally, orientation) of the detected object.
   - Match the detected rectangle to the closest entry in the precomputed dataset using a fast search algorithm.
   - Output the estimated real-world position (and orientation) of the game piece.

## Limitations

- **Requires Fixed Camera Position**: The camera must remain in the exact same position and orientation as during the Blender rendering phase.
- **Long Preprocessing Time**: Generating the dataset in Blender can take around 2 hours, depending on CPU, number of images, and resolution.
- **Not Suitable for Dynamic Camera Setups**: Any change in camera pose requires re-rendering the dataset.

## Project Structure

```
game-piece-pos-estimation
├── RaspberryPiCode
│   ├── main.py                  # Entry point of the application
│   ├── frame_capture.py         # Frame capture class
│   ├── game_piece_detection.py  # Game piece detection class
│   ├── game_piece_pos_estimation.py # Pose estimation class
│   ├── network_manager.py       # NetworkTables integration
├── Data/                        # Precomputed datasets (CSV, Blender Files, Output of Blender Files)
├── PositionEstimation/          # Data (from Blender) processing scripts and notebooks to showcase the algorithm
├── SimpleColorDetection/        # Color detection calibration and demos
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YoavRozov/FRC-Game-Piece-Pos-Estimation.git
   cd game-piece-pos-estimation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Dataset (if needed)**:
   - Use the Blender files inside "Data" or create your own to generate the required dataset
   - Use the the Jupyter notebooks in `PositionEstimation/` to process the dataset from Blender and convert it to a CSV dataset for your specific game piece and camera setup.

4. **Run the Application**:
   ```bash
   python RaspberryPiCode/main.py
   ```

## Dependencies

- OpenCV
- NumPy
- Pandas
- ntcore
- cscore

## License

This project is licensed under the AGPL-3.0 License. See the LICENSE file for more details.