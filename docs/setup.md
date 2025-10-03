# Game Piece Position Estimation - Step by step guide

Welcome! This guide walks you through setting up the project, generating images with Blender, processing data, and using the pose estimation algorithm to predict a game piece’s position relative to a robot.


## Prerequisites

- **Operating system**: Windows, macOS, or Linux
- **Python**: 3.10+ (3.11 recommended)
- **Blender**: 4.5 or newer (older versions may fail to open the provided `.blend` file)
- **Git** (optional, for cloning)

!!! note "Python installation"
    If Python isn't installed, please install it first, you can use this guide: [Python installation guide](https://github.com/YoavRozov/FRC-Programming-Intro/blob/main/Chapter%205%20-%20Computer%20Vision/InstallationGuide.pdf).
    
    After installation, ensure `python`/`pip` are available from your terminal.

---

## Download the project

=== "Using Git"

    ```bash
    # Navigate to the folder where you want the repository
    cd <PATH_TO_YOUR_CODE_FOLDER>

    # Clone the repository
    git clone https://github.com/YoavRozov/FRC-Game-Piece-Pos-Estimation.git
    ```

=== "Download ZIP"

    1. Click **Code → Download ZIP** on the repository page.
    2. After the download completes, **extract** the ZIP to your desired folder.

---

## Program setup (Python)

Open a terminal/command prompt and navigate to the project folder you cloned/extracted in the previous step.

=== "Windows (PowerShell/CMD)"

    ```bat
    cd <PATH_TO_PROJECT_ROOT>
    ```

=== "macOS / Linux (Bash)"

    ```bash
    cd <PATH_TO_PROJECT_ROOT>
    ```

### (Recommended) Create a virtual environment

=== "Windows"

    ```bat
    python -m venv .venv
    .venv\Scripts\activate
    ```

=== "macOS / Linux"

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

### Install required packages

From the project root:

```bash
pip install -r requirements.txt
```

---

## Blender

1. Download and install Blender from: **[blender.org](https://www.blender.org/download)**
2. Open the `template.blend` file included in this repository.

!!! warning
    If the file doesn't open, ensure you're using **Blender 4.5 or newer**. Older versions may not be compatible.

### Setup Blender-Python packages

1. In Blender, click **Windows → Toggle System Console** so you can see script output.
2. Navigate to the **Scripting** tab.
3. In the script drop-down, select **`Install requirements`**.
4. Click **Run** and verify there are **no errors** in the console.


<video controls>
  <source src="media/BlenderSetup.mp4" type="video/mp4">
  <source src="media/BlenderSetup.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

---

## Blender setup & Image Generation

### 4.1 Capture reference images
Connect your robot's camera to your computer.

Run the `image_capture.py` script and capture a few photos with the game piece clearly in frame. These will be used to calibrate the camera.

!!! tip
    Take these photos on a floor with a **tile grid pattern** (e.g., a classroom floor). Aligning Blender’s grid to a real grid makes calibration much easier.

### 4.2 Calibrate the camera in Blender

1. Open `template.blend`.
2. Measure your robot’s **camera height** above the ground and its **rotation**.
3. Click the **camera icon** (in the viewport) to view through the camera.
4. Select the **camera** in the Outliner.
    - Open **Object Data Properties → Background Images**, enable it, and load one of the photos captured in the last step.
    - Adjust **position** and **rotation** under **Object Properties**.
    - Adjust **Field of View** and **Sensor Size** under **Object Data Properties**.
5. Align the camera so Blender’s grid **matches the floor’s grid** in your background image. You can also modify Blender’s grid size to match the **physical tile size** on your floor.

!!! tip "Optional: fSpy for a head start"
    You can use [fSpy](https://fspy.io) to get a close initial camera estimate. Helpful video tutorials:

    - [How to Install fSpy Photo Matching Software](https://www.youtube.com/watch?v=0x2ZffQQNJY)
    - [How to Install the fSpy Importer Add-on for Blender](https://www.youtube.com/watch?v=1HOqnb1Uji4)
    - [How to Match a Photo with fSpy](https://www.youtube.com/watch?v=7pgDrQzThH0)

<video controls>
  <source src="media/CameraSetup.mp4" type="video/mp4">
  <source src="media/CameraSetup.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

### 4.3 Import the game piece model

1. Download the official game piece model (e.g., from FIRST’s website) and export/save it as `.stl` from SolidWorks.
2. In Blender: **File → Import → STL**, select the saved model.
3. After import, you will likely need to **scale by 0.001 (1/1000)** because SolidWorks uses **millimeters** and Blender uses **meters**.
4. With the object selected, open **Object Properties → Scale** and set the scale.
5. Press `F3`, search for **`Origin to Geometry`**, and press **Enter** to center the origin.
<video controls>
  <source src="media/GamePieceImport.mp4" type="video/mp4">
  <source src="media/GamePieceImport.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

### 4.4 Define the working area with `FOV_Plane`

1. Open the **Camera Plane Set Up** tab.
2. Click the **camera icon** (in the viewport) to switch to the camera’s view.
3. As you can see the viewport is split so you have a **left** (camera view) and **right** (top-down) view.
4. In the left view, use **Move** (from the top toolbar). In the right/top view:
    - Select the **plane** object named `FOV_Plane`.
    - Press `Tab` to enter **Edit Mode**.
    - Select vertices and move them along **X** and **Y** to match the camera FOV visible in the left view.
!!! tip
    Use `s` → `x` on your keyboard to scale two or more vertices on the x axis.

<video controls>
  <source src="media/CameraPlaneSetup.mp4" type="video/mp4">
  <source src="media/CameraPlaneSetup.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

### 4.5 Run the main Blender script
1. Select the imported game piece, go to **Material Properties** and select the `Red` material
1. **Windows → Toggle System Console** (if not already open) to view outputs.
2. Go to the **Scripting** tab and select the **`main`** file from the dropdown.
3. Review configuration variables at the top of the script and adjust as needed.
4. **Run** the script and wait for rendering to complete.

<video controls>
  <source src="media/RunMainScript.mp4" type="video/mp4">
  <source src="media/RunMainScript.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

---

## Process Blender data

After rendering finishes, open the **`ProcessBlenderData.ipynb`** Jupyter notebook and run all cells.

**Output:** a `CSV` containing all possible game piece positions and their **bounding rectangles** in the generated images.

---

## Estimate the position

Open the **`PoseEstimation.ipynb`** notebook to accurately predict the game piece’s position relative to the robot given the **bounding rectangle** in an image.

!!!note
    For a production-ready example, see the **`RaspberryPiCode/`** folder for integrating the algorithm on-device.

---

## Troubleshooting

**Blender file won’t open**  
Ensure you’re using **Blender 4.4+**. Update Blender if necessary.

**`pip install -r requirements.txt` fails**

- Activate your virtual environment first.  
- Upgrade pip: `python -m pip install --upgrade pip`  
- On macOS/Linux, try `pip3` instead of `pip` if multiple Python versions exist.

**Background image won’t show in camera view**

- Confirm you enabled **Background Images** in **Object Data Properties** for the camera.  
- Check the **opacity** and that you’re actually viewing through the camera.

**Imported STL is too big/small**

- SolidWorks uses **mm**, Blender uses **m**. Scale by **0.001** or **1000** accordingly.  
- Apply scale if needed (`Ctrl+A → Scale`).

**`main` script can’t find paths/files**

- Confirm paths are correct and files exist in the expected folders.  
- Run Blender from the project root or adjust path handling in the script.

---

## Attributions

- Blender® is a registered trademark of the Blender Foundation.
- fSpy is a community project for camera matching.
- FIRST® references for the game piece model.