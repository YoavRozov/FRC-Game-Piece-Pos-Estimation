import numpy as np
import pandas as pd

class GamePiecePosEstimator:
    """
    A class used to estimate the position of game pieces in the image

    Attributes
    ----------
    width : int
        The width of the image

    height: int
        The height of the image

    data : pandas.DataFrame
        The data frame containing the game piece positions

    Methods
    -------
    estimate_position(rectangle: np.ndarray) -> tuple[int, int]
        Estimates the position of a game piece based on its bounding rectangle
    """
    
    def __init__(self, width: int, height: int, data : pd.DataFrame):
        self.width = width
        self.height = height
        self.data = data
    

    def find_matching_rows(self, df, target, start_tol=25, max_tol=40, step=3) -> tuple[pd.DataFrame, int]:
        """
        Find rows in the dataframe that match the target values within a dynamically
        increasing tolerance. If no rows are found for a very small tolerance, the
        tolerance will be increased until at least one row is found or the maximum
        tolerance is reached.

        Parameters:
            df (pd.DataFrame): DataFrame with the columns.
            target (dict): Target values for each column.
            start_tol (int): Starting tolerance measured in pixels.
            max_tol (int): Maximum allowed tolerance measured in pixels.
            step (int): Increment to increase tolerance on each iteration measured in pixels.

        Returns:
            filtered_df (pd.DataFrame): DataFrame with matching rows.

            used_tol (int): Tolerance at which the matching rows were found.
        """
        tolerance = start_tol
        while tolerance <= max_tol:
            # Create mask using np.isclose for each column
            mask = (
                np.isclose(df['Center_X'], target['Center_X'], atol=tolerance) &
                np.isclose(df['Center_Y'], target['Center_Y'], atol=tolerance) &
                np.isclose(df['Width'], target['Width'], atol=tolerance) &
                np.isclose(df['Height'], target['Height'], atol=tolerance)
            )
            filtered_df = df[mask]
            
            # Check if any row is found
            if not filtered_df.empty:
                print(f"Found rows with tolerance: {tolerance}")
                return filtered_df, tolerance
            
            # Increase the tolerance and try again
            tolerance += step

        # No rows found within maximum tolerance
        print("No rows found within the max tolerance.")
        return df.iloc[[]], tolerance  # Return an empty DataFrame
    
    def estimate_position(self, rectangle: np.ndarray) -> tuple[tuple[float, float], int]:
        """
        Estimates the position of a game piece based on its bounding rectangle.

        Parameters:
            rectangle (np.ndarray): A numpy array containing the bounding rectangle
                                    in the format [x, y, width, height].

        Returns:
            tuple[tuple[int, int], int]: A tuple containing the estimated position
                                          (center_x, center_y) and the estimated certainty.
        """
        x, y, w, h = rectangle
        center_x = x + w // 2
        center_y = y + h // 2
        
        target = {
            'Center_X': center_x,
            'Center_Y': center_y,
            'Width': w,
            'Height': h
        }
        
        matching_rows, used_tol = self.find_matching_rows(self.data, target, 25, 40, 3)
        
        if not matching_rows.empty:
            return (matching_rows['x_position'].mean(), matching_rows['y_position'].mean(), (50 - used_tol))
        
        # If no match is found, return None for position and 0 for certainty
        return None