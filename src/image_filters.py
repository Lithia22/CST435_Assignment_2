import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

class ImageProcessor:
    # This class groups all image filtering operations into a single, reusable component.
    # Each method is static since no shared state is required between filter operations.
    
    @staticmethod
    def apply_grayscale(image_path):
        """Convert RGB image to grayscale using luminance formula"""
        # Read the image from disk using OpenCV.
        img = cv2.imread(image_path)
        if img is None:
            # Return None if the image cannot be loaded (e.g., invalid path or corrupted file).
            return None
        
        # Convert the image to grayscale using OpenCV's optimized implementation,
        # which internally applies the luminance-based conversion.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray
    
    @staticmethod
    def apply_gaussian_blur(image_path):
        """Apply 3x3 Gaussian kernel for smoothing"""
        # Load the image in its original color format.
        img = cv2.imread(image_path)
        if img is None:
            # Safely handle missing or unreadable images.
            return None
        
        # Apply a 3x3 Gaussian blur to reduce noise and smooth the image.
        # A small kernel is used to balance smoothing with detail preservation.
        blurred = cv2.GaussianBlur(img, (3, 3), 0)
        return blurred
    
    @staticmethod
    def apply_edge_detection(image_path):
        """Sobel filter for edge detection"""
        # Load the image directly in grayscale for edge detection.
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            # Return None if image loading fails.
            return None
        
        # Apply Sobel operators in the horizontal (x) and vertical (y) directions.
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        
        # Compute the gradient magnitude to combine edge responses
        # from both directions into a single edge map.
        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        
        # Clip values to valid image range and convert to 8-bit format.
        magnitude = np.uint8(np.clip(magnitude, 0, 255))
        
        return magnitude
    
    @staticmethod
    def apply_sharpening(image_path):
        """Enhance edges and details"""
        # Load the image using PIL to leverage its built-in sharpening filter.
        img = Image.open(image_path)
        
        # Apply a predefined sharpening filter to enhance fine details.
        sharpened = img.filter(ImageFilter.SHARPEN)
        
        # Convert the result back to a NumPy array for consistency
        # with OpenCV-based processing.
        sharpened_np = np.array(sharpened)
        
        # If the output is grayscale, convert it to a 3-channel image
        # to maintain consistent output formats across filters.
        if len(sharpened_np.shape) == 2:
            sharpened_np = cv2.cvtColor(sharpened_np, cv2.COLOR_GRAY2BGR)
        
        return sharpened_np
    
    @staticmethod
    def apply_brightness_adjustment(image_path, factor=1.5):
        """Increase or decrease image brightness"""
        # Load the image using PIL to simplify brightness manipulation.
        img = Image.open(image_path)
        
        # Create a brightness enhancer and apply the adjustment factor.
        # Values >1 increase brightness, while values <1 darken the image.
        enhancer = ImageEnhance.Brightness(img)
        brightened = enhancer.enhance(factor)
        
        # Convert the processed image to a NumPy array for saving with OpenCV.
        brightened_np = np.array(brightened)
        
        # Ensure the output is a 3-channel image for consistency.
        if len(brightened_np.shape) == 2:
            brightened_np = cv2.cvtColor(brightened_np, cv2.COLOR_GRAY2BGR)
        
        return brightened_np
    
    @staticmethod
    def apply_all_filters(image_path, output_dir="processed"):
        """
        Apply all 5 filters sequentially to one image
        Returns processing time
        """
        import time
        
        # Record the start time to measure total processing duration.
        start_time = time.time()
        
        # Apply each filter independently using the original image path.
        # This design ensures filters do not depend on the output of previous filters.
        gray = ImageProcessor.apply_grayscale(image_path)
        blurred = ImageProcessor.apply_gaussian_blur(image_path)
        edges = ImageProcessor.apply_edge_detection(image_path)
        sharpened = ImageProcessor.apply_sharpening(image_path)
        brightened = ImageProcessor.apply_brightness_adjustment(image_path)
        
        # Save all filtered outputs if an output directory is specified.
        if output_dir:
            import os
            from pathlib import Path
            
            # Create the output directory if it does not already exist.
            Path(output_dir).mkdir(exist_ok=True)
            
            # Extract the base filename without the extension for naming outputs.
            filename = Path(image_path).stem
            
            # Write each filtered image to disk with descriptive suffixes.
            cv2.imwrite(f"{output_dir}/{filename}_gray.jpg", gray)
            cv2.imwrite(f"{output_dir}/{filename}_blurred.jpg", blurred)
            cv2.imwrite(f"{output_dir}/{filename}_edges.jpg", edges)
            cv2.imwrite(f"{output_dir}/{filename}_sharpened.jpg", sharpened)
            cv2.imwrite(f"{output_dir}/{filename}_brightened.jpg", brightened)
        
        # Capture the end time after all processing and saving is complete.
        end_time = time.time()
        
        # Return total processing time for performance evaluation.
        return end_time - start_time
