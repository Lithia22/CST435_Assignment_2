import os
import sys

def setup_results_folder():
    """Create results folder structure"""
    results_dir = "results"
    
    # Remove old results
    import shutil
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    
    # Create fresh structure
    os.makedirs(os.path.join(results_dir, "performance_data"), exist_ok=True)
    os.makedirs(os.path.join(results_dir, "output_images"), exist_ok=True)
    
    return results_dir

def zip_results(results_dir):
    """Create zip file of results"""
    import zipfile
    
    zip_filename = "results.zip"
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(results_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arcname)
        
        print(f"Results saved to: {zip_filename}")
        return zip_filename
        
    except Exception as e:
        print(f"Failed to create zip: {e}")
        return None

def run_all():
    """Run the complete pipeline"""
    print("=" * 60)
    print("PARALLEL IMAGE PROCESSING - CST435")
    print("=" * 60)
    
    # Setup
    results_dir = setup_results_folder()
    
    # Verify dataset
    if not os.path.exists("food101_subset"):
        print("Dataset not found: food101_subset/")
        print("Please ensure the dataset folder exists with images.")
        return
    
    # Import modules
    sys.path.append('src')
    from multiprocessing_impl import run_multiprocessing_experiment
    from concurrent_futures_impl import run_futures_experiment
    from performance_analysis import plot_comparison
    
    # Run parallel implementations
    mp_results = run_multiprocessing_experiment("food101_subset", [1, 2, 4, 8], results_dir)
    futures_results = run_futures_experiment("food101_subset", [1, 2, 4, 8], results_dir)
    
    # Generate performance analysis
    plot_comparison(mp_results, futures_results, results_dir)
    
    # Create downloadable zip
    zip_results(results_dir)
    
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    run_all()