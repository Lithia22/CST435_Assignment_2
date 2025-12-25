import os
import time
import glob
from multiprocessing import Pool, cpu_count
from image_filters import ImageProcessor
from pathlib import Path

def process_single_image(image_path):
    """Process a single image with all filters"""
    # This function is executed by individual worker processes in the pool.
    # Each process handles one image independently to enable parallel execution.
    try:
        # Apply all image filters and store the results in the shared output directory.
        # The returned processing time is used for performance evaluation.
        processing_time = ImageProcessor.apply_all_filters(
            image_path, 
            output_dir="results/output_images"
        )
        return processing_time
    except Exception as e:
        # Catch exceptions to prevent a single image failure
        # from stopping the entire multiprocessing workflow.
        print(f"Error processing {image_path}: {e}")
        return 0

def multiprocessing_pipeline(image_folder, num_processes=None):
    """
    Process all images using multiprocessing.Pool
    """
    # Define supported image formats to include in the dataset.
    image_extensions = ['*.jpg', '*.jpeg', '*.png']
    image_paths = []
    
    # Recursively search the dataset directory for all matching image files.
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(image_folder, '**', ext), recursive=True))
    
    # Log the number of images discovered for processing.
    print(f"Found {len(image_paths)} images to process")
    
    # If the number of processes is not specified, default to the CPU core count.
    # This choice aims to maximize parallel CPU utilization for compute-heavy tasks.
    if num_processes is None:
        num_processes = cpu_count()
    
    # Ensure the output directory exists before starting parallel processing.
    Path("results/output_images").mkdir(parents=True, exist_ok=True)
    
    # Record the wall-clock start time for overall execution measurement.
    start_time = time.time()
    
    # Create a multiprocessing pool where each process applies filters to images.
    # The pool manages task distribution and process lifecycle automatically.
    with Pool(processes=num_processes) as pool:
        # Distribute image paths across worker processes using map.
        # This blocks until all images have been processed.
        results = pool.map(process_single_image, image_paths)
    
    # Calculate total wall-clock time taken by the multiprocessing pipeline.
    total_time = time.time() - start_time
    
    # Aggregate individual processing times to compute summary statistics.
    total_processing_time = sum(results)
    avg_time_per_image = total_processing_time / len(results) if results else 0
    
    # Display performance metrics for the current process configuration.
    print(f"\n=== Multiprocessing Results ===")
    print(f"Number of processes: {num_processes}")
    print(f"Total images processed: {len(image_paths)}")
    print(f"Total wall-clock time: {total_time:.2f} seconds")
    print(f"Total processing time (sum): {total_processing_time:.2f} seconds")
    print(f"Average time per image: {avg_time_per_image:.2f} seconds")
    
    # Return structured results for comparison with other parallel approaches.
    return {
        'num_processes': num_processes,
        'num_images': len(image_paths),
        'total_time': total_time,
        'processing_times': results
    }

def run_multiprocessing_experiment(image_folder, process_counts=None):
    """
    Run multiprocessing with different process counts
    """
    # Define default process counts to evaluate scalability behavior.
    if process_counts is None:
        process_counts = [1, 2, 4, 8]
    
    results = {}
    
    # Execute the multiprocessing pipeline using different numbers of processes.
    for num_procs in process_counts:
        print(f"\n{'='*50}")
        print(f"Running with {num_procs} processes...")
        print('='*50)
        
        # Run the pipeline and store the resulting performance data.
        result = multiprocessing_pipeline(image_folder, num_procs)
        results[num_procs] = result
        
        # Introduce a short delay to reduce system load between experiments.
        time.sleep(2)
    
    return results

if __name__ == "__main__":
    # Entry point for standalone execution of the multiprocessing experiment.
    # Specifies the dataset directory used for performance testing.
    dataset_path = "food101_subset"
    if os.path.exists(dataset_path):
        # Run experiments across multiple process configurations.
        results = run_multiprocessing_experiment(dataset_path)
        
        # Save the collected performance data to disk for later analysis.
        import json
        Path("results/performance_data").mkdir(parents=True, exist_ok=True)
        with open('results/performance_data/multiprocessing_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print("Results saved to: results/performance_data/multiprocessing_results.json")
    else:
        # Inform the user if the dataset path does not exist.
        print(f"Dataset path '{dataset_path}' not found!")
