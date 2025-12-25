import os
import time
import glob
import concurrent.futures
from image_filters import ImageProcessor
from pathlib import Path
import multiprocessing

def process_single_image_futures(image_path):
    """Process a single image with all filters"""
    # This function is executed in a separate process by the ProcessPoolExecutor.
    # It isolates image-level work so that each process handles one image independently.
    try:
        # Apply all image filters and store the output in the designated directory.
        # The processing time returned is used later for performance analysis.
        processing_time = ImageProcessor.apply_all_filters(
            image_path, 
            output_dir="results/output_images"
        )
        return processing_time
    except Exception as e:
        # Catch and log any errors to prevent a single image failure
        # from terminating the entire parallel execution.
        print(f"Error processing {image_path}: {e}")
        return 0

def futures_pipeline(image_folder, num_workers=None):
    """
    Process all images using concurrent.futures ProcessPoolExecutor
    """
    # Define supported image file extensions to be processed.
    image_extensions = ['*.jpg', '*.jpeg', '*.png']
    image_paths = []
    
    # Recursively search the dataset folder for images matching the extensions.
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(image_folder, '**', ext), recursive=True))
    
    # Log the total number of images discovered in the dataset.
    print(f"Found {len(image_paths)} images to process")
    
    # If the number of workers is not specified, default to the number of CPU cores.
    # This choice maximizes CPU utilization for CPU-bound image processing tasks.
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()
    
    # Ensure the output directory exists before starting parallel execution.
    Path("results/output_images").mkdir(parents=True, exist_ok=True)
    
    # Record the wall-clock start time for overall performance measurement.
    start_time = time.time()
    
    # Initialize a ProcessPoolExecutor to enable true parallelism
    # by distributing work across multiple CPU processes.
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Submit one task per image to the executor.
        # Each future is mapped back to its corresponding image path.
        future_to_image = {
            executor.submit(process_single_image_futures, img_path): img_path 
            for img_path in image_paths
        }
        
        # Collect results asynchronously as each task completes.
        # This avoids waiting for tasks in submission order.
        results = []
        for future in concurrent.futures.as_completed(future_to_image):
            img_path = future_to_image[future]
            try:
                # Retrieve the processing time returned by the worker process.
                result = future.result()
                results.append(result)
            except Exception as e:
                # Handle unexpected execution errors at the future level.
                print(f"Image {img_path} generated exception: {e}")
                results.append(0)
    
    # Compute total wall-clock execution time for the entire pipeline.
    total_time = time.time() - start_time
    
    # Aggregate individual processing times to derive summary statistics.
    total_processing_time = sum(results)
    avg_time_per_image = total_processing_time / len(results) if results else 0
    
    # Display performance metrics for the current worker configuration.
    print(f"\n=== Concurrent.Futures Results ===")
    print(f"Number of workers: {num_workers}")
    print(f"Total images processed: {len(image_paths)}")
    print(f"Total wall-clock time: {total_time:.2f} seconds")
    print(f"Total processing time (sum): {total_processing_time:.2f} seconds")
    print(f"Average time per image: {avg_time_per_image:.2f} seconds")
    
    # Return structured results for downstream analysis and comparison.
    return {
        'num_workers': num_workers,
        'num_images': len(image_paths),
        'total_time': total_time,
        'processing_times': results
    }

def run_futures_experiment(image_folder, worker_counts=None):
    """
    Run concurrent.futures with different worker counts
    """
    # Define default worker configurations to evaluate scalability.
    if worker_counts is None:
        worker_counts = [1, 2, 4, 8]
    
    results = {}
    
    # Execute the pipeline multiple times using different worker counts.
    for num_workers in worker_counts:
        print(f"\n{'='*50}")
        print(f"Running with {num_workers} workers...")
        print('='*50)
        
        # Run the parallel pipeline and store the performance results.
        result = futures_pipeline(image_folder, num_workers)
        results[num_workers] = result
        
        # Introduce a short delay to reduce resource contention
        # between consecutive experimental runs.
        time.sleep(2)
    
    return results

if __name__ == "__main__":
    # Entry point for standalone execution.
    # Defines the dataset location used for performance evaluation.
    dataset_path = "food101_subset"
    
    if os.path.exists(dataset_path):
        # Run experiments using multiple worker configurations.
        results = run_futures_experiment(dataset_path)
        
        # Persist results to disk for later visualization or reporting.
        import json
        Path("results/performance_data").mkdir(parents=True, exist_ok=True)
        with open('results/performance_data/futures_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print("Results saved to: results/performance_data/futures_results.json")
    else:
        # Notify the user if the dataset path is invalid or missing.
        print(f"Dataset path '{dataset_path}' not found!")
