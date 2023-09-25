
# Midas2 3D Terrain Visualization



https://github.com/Immersive-Collective/xr-midas-threejs/assets/27820237/f454a6f4-7307-4e6f-a9d1-8308d52de7c6



This repository showcases an application that leverages the capabilities of the Midas2 model to generate depth data from a single image. The depth data, indicative of the distance of each object in the image from the camera, is then transformed into a 3D terrain representation using ThreeJS.

## Overview:
- **Midas2 Integration**: The core functionality extracts depth information from a given 2D image using the state-of-the-art Midas2 model. This depth map provides a grayscale representation where the brightness of each pixel corresponds to its relative depth.
  
- **ThreeJS Visualization**: The derived depth data is then fed into ThreeJS, a popular 3D graphics library in JavaScript, to render a 3D terrain. The terrain is a visual representation of the original image but with elevations and depressions based on depth.

## Use Case:
This demo can be particularly useful for:
- Visualizing depth in photographs where it's not immediately discernible.
- Generating 3D models from 2D images for various graphics or gaming applications.
- Understanding and experimenting with depth estimation models and 3D graphics rendering.

Join us in exploring the fascinating convergence of depth estimation and 3D visualization!


---

## Depth Map Generation using MiDaS and Flask

This project uses the MiDaS model for generating depth maps from images, integrated into a Flask application. Users can upload images through a web interface, and the depth maps will be computed and displayed.

### Prerequisites

- Python 3.7 or newer
- pip (Python package manager)
- CUDA-compatible GPU (if available, for faster computation)

### Installation

1. **Clone the repository**:

   ```
   git clone https://github.com/your-repo-link.git
   cd your-repo-directory/
   ```

   Replace `your-repo-link` with the actual repository link and `your-repo-directory` with the name of the directory.

2. **Set up a virtual environment** (optional, but recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages**:

   ```
   pip install flask torch torchvision opencv-python matplotlib
   ```

### Running the Application

1. **Start the Flask app**:

   ```
   python your-script-name.py
   ```

   Replace `your-script-name.py` with the name of the script.

2. Open a web browser and navigate to:

   ```
   http://localhost:5050/
   ```

3. **Use the web interface**:

   - Click on the "Upload" button to select an image.
   - Once the image is uploaded, wait for the depth map to be generated.
   - The generated depth map will be displayed on the next page.

### Troubleshooting

1. **CUDA Errors**: If you face issues related to CUDA or don't have a GPU, you can modify the line:

   ```python
   device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
   ```

   to

   ```python
   device = torch.device("cpu")
   ```

   to force the model to run on the CPU.

2. **File Upload Issues**: Ensure the `uploads` and `outputs` directories exist. They should be automatically created when the application starts, but if they're not, you can manually create them in the root directory of 
the project.

### Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

---

This README provides a basic overview of how to set up and run the Flask application. Depending on the complexity and requirements of your project, you may need to provide more detailed instructions or include additional 
sections.
