# xr-midas-threejs
# XR 2.5: Flask Meets Three.js

<img width="1728" alt="Screenshot 2023-09-26 at 12 11 50" src="https://github.com/Immersive-Collective/xr-midas-threejs/assets/27820237/98e9d6d1-d7c3-4657-b55c-ed42dd90e7e0">



https://github.com/Immersive-Collective/xr-midas-threejs/assets/27820237/d922d189-532f-4d3f-a20a-443a8e46f810




# Demos
https://github.com/Immersive-Collective/xr-midas-threejs/assets/27820237/fba5d4ec-add5-4ce4-840c-fe2858364474
https://github.com/Immersive-Collective/xr-midas-threejs/assets/27820237/cac396c4-49f9-45c3-83ca-9fe7632fb8b1


# Live Demo
https://metaboy.tech:5050/

Welcome to the XR 2.5 project. This application is an integration of Flask, a lightweight Python web framework, and Three.js, a popular JavaScript library for 3D graphics. The project lets users upload images which are then processed and rendered using Three.js in a virtual environment.

## Table of Contents

- [Features](#features)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
  
## Features

1. **Flask Backend** - Handle image uploads and serve static assets.
2. **Three.js Frontend** - Render 3D graphics based on uploaded images, including depth perception.
3. **3D Physics with Rapier.js** - Simulate realistic physics for 3D objects.
4. **WebXR Integration** - View rendered graphics in virtual reality environments.

## Setup & Installation

### Prerequisites
- Python 3.x
- Node.js and npm (if you wish to extend the frontend assets)

### Steps

1. Clone the repository:
```bash
git clone <repository_url>
cd <repository_dir>
```

2. Install Flask and other Python dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) If you're modifying frontend assets:
```bash
npm install
# Make changes and build assets
npm run build
```

4. Run the Flask application:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Visit `http://localhost:5000` in your browser.

## Usage

1. **Upload Images**: Use the UI to upload an image. The preview of the image will be shown, and a 3D render based on depth perception will be created using Three.js.
2. **Interact with the 3D Render**: Navigate the 3D scene using mouse controls. Zoom, rotate, and pan to view the image from different angles.
3. **VR Mode**: If you have a VR headset, you can use the WebXR integration to view the 3D scene in virtual reality.
4. **Export Models**: Use the built-in functions to export the 3D model in GLTF or GLB format.

## Code Structure

- `app.py`: The Flask application file. Contains routes and logic for uploading and serving files.
- `static/`: Directory containing static assets like JS libraries, styles, and other assets.
    - `libs/`: Libraries like Three.js, Rapier, etc.
    - `styles/`: CSS styles for the UI.
    - `images/`: Placeholder and other images.
- `index.html`: The main UI that combines Flask and Three.js functionalities. It integrates the image upload functionality and sets up the 3D scene.

---

## Development & Customization

You can extend the functionalities by:
- Adding more 3D models or assets in the `static/` directory.
- Integrate more Three.js addons or modify the existing ones in `index.html`.
- Enhance the backend features in `app.py`.

---

## Support

For issues, bugs, or feature requests, please raise an issue or pull request on the GitHub repository. 

## Acknowledgements

Thanks to the contributors of Three.js, Flask, Rapier.js, and other libraries/tools used in this project.

---
