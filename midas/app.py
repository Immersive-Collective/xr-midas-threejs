import os
import cv2
import torch
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, send_from_directory



app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# ...

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        process_image(filename)
        basename = os.path.basename(filename)
        depth_filename = os.path.join(app.config['OUTPUT_FOLDER'], os.path.splitext(basename)[0] + "_depth.jpg")
        os.rename(os.path.join(app.config['OUTPUT_FOLDER'], "output_depthmap.jpg"), depth_filename)
        return render_template('result.html', filename=basename, depth_filename=os.path.basename(depth_filename))
        #return render_template('result.html', filename="output_depthmap.jpg")

def process_image(filename):
    # img_path is directly filename since filename already has the correct path
    img = cv2.imread(filename)
    
    # Check if the image is loaded correctly
    if img is None:
        raise ValueError(f"Failed to load image at {filename}")
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Load the model
    #model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
    #model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
    model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)
    midas = torch.hub.load("intel-isl/MiDaS", model_type, force_reload=False, trust_repo=True)
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", force_reload=False)

    # model_type = "DPT_Large"  # MiDaS v3 - Large
    # midas = torch.hub.load("intel-isl/MiDaS", model_type)

    # Move the model to GPU if available
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    midas.to(device)
    midas.eval()

    # Load transforms to resize and normalize the image
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
        transform = midas_transforms.dpt_transform
    else:
        transform = midas_transforms.small_transform

    # Apply the transforms
    input_batch = transform(img).to(device)

    # Predict and resize to original resolution
    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    output = prediction.cpu().numpy()
    
    # Save the output as an image
    plt.imsave(os.path.join(app.config['OUTPUT_FOLDER'], "output_depthmap.jpg"), output)


@app.route('/outputs/<filename>')
def outputed_file(filename):
    #return send_from_directory(app.config['OUTPUT_FOLDER'], filename)
    return send_from_directory(os.path.abspath(app.config['OUTPUT_FOLDER']), filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #return send_from_directory(app.config['OUTPUT_FOLDER'], filename)
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    app.run(host='0.0.0.0', port=5050, debug=True)

