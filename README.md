# CST435: Parallel Image Processing on GCP

A system that applies 5 image filters to Food-101 photos using two parallel programming paradigms:

1. `multiprocessing.Pool`
2. `concurrent.futures.ProcessPoolExecutor`

## GCP Deployment

### 1. Create VM Instance

- **Machine Type**: e2-standard-4 (4 vCPU, 16GB RAM)
- **Boot Disk**: 30GB, Ubuntu 22.04 LTS **x86/64**
- **Firewall**: Allow HTTP/HTTPS traffic

### 2. Setup Commands (GCP SSH)

```bash
# Update system
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git

# Clone and setup
git clone https://github.com/Lithia22/CST435_Assignment_2.git
cd CST435_Assignment_2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the program
python main.py
```

## 3. Download Results from GCP

After running `python main.py`, you'll get these files:

```
results/
├── performance_comparison.png        # Performance graphs
├── performance_data/                 # JSON results
└── output_images/                    # All processed images
```

### Download Individual Files:

1. Select **"Download file"** in SSH
2. Enter path **(replace `username` with your actual username)**:
   - `/home/username/CST435_Assignment_2/results/performance_comparison.png`
   - `/home/username/CST435_Assignment_2/results/performance_data/multiprocessing_results.json`
   - `/home/username/CST435_Assignment_2/results/performance_data/futures_results.json`
   - `/home/username/CST435_Assignment_2/results/output_images/740385_gray.jpg`

### Download All Files (ZIP):

1. Select **"Download file"** in SSH
2. Enter: `/home/username/CST435_Assignment_2/results.zip`

**Note:** ZIP file is large so may take longer time to download.

## Filtered Results

|                  Original Image                   |                              Grayscale                               |                              Gaussian Blur                              |                            Edge Detection                             |                             Image Sharpening                              |                           Brightness Adjustment                            |
| :-----------------------------------------------: | :------------------------------------------------------------------: | :---------------------------------------------------------------------: | :-------------------------------------------------------------------: | :-----------------------------------------------------------------------: | :------------------------------------------------------------------------: |
| <img src="food101_subset/740385.jpg" width="150"> | <img src="sample_results/output_images/740385_gray.jpg" width="150"> | <img src="sample_results/output_images/740385_blurred.jpg" width="150"> | <img src="sample_results/output_images/740385_edges.jpg" width="150"> | <img src="sample_results/output_images/740385_sharpened.jpg" width="150"> | <img src="sample_results/output_images/740385_brightened.jpg" width="150"> |

**Note**: Sample outputs are stored in sample_results folder for demo. Your actual results will be generated in `results/` folder.

## Group Members

- **Lithia A/P Kisnen** - 163850
- **Tejashree Laxmi A/P Kanthan** - 163506
- **Dershyani A/P B.Thessaruva** - 164062
- **Kavitashini A/P Seluvarajoo** - 164329
