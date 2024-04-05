import os
import cv2
import torch
import logging
import matplotlib.pyplot as plt

import numpy as np
import json
import uuid


from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.DEBUG)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
LIBS_FOLDER = 'libs'

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'heic', 'bmp', 'hdr'}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

SHARE_FOLDER = os.path.join(BASE_DIR, 'share')
app.config['SHARE_FOLDER'] = SHARE_FOLDER
if not os.path.exists(app.config['SHARE_FOLDER']):
    os.makedirs(app.config['SHARE_FOLDER'])


def resize_image(image_path, max_dimension=1920):
    """Resizes the image while maintaining the aspect ratio with a maximum width or height."""

    # Read the image
    img = cv2.imread(image_path)

    # Check if the image width or height exceeds the maximum dimension
    if img.shape[1] > max_dimension or img.shape[0] > max_dimension:
        if img.shape[1] > img.shape[0]:  # Image is landscape
            aspect_ratio = img.shape[1] / img.shape[0]
            new_width = max_dimension
            new_height = int(new_width / aspect_ratio)
        else:  # Image is portrait
            aspect_ratio = img.shape[0] / img.shape[1]
            new_height = max_dimension
            new_width = int(new_height / aspect_ratio)

        # Resize the image
        img = cv2.resize(img, (new_width, new_height))

        # Save the resized image back
        cv2.imwrite(image_path, img)

    return img

def rgb_to_hex_format(rgb):
    return "0x{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def extract_colors(image_path, n_colors=32):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB color space
    img = cv2.resize(img, (150, 150))  # optional, to reduce computation
    
    # Reshape the data
    data = img.reshape((-1, 3))
    
    # Use KMeans from cv2 to get the dominant colors
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.2)
    _, labels, centers = cv2.kmeans(data.astype(np.float32), n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    return centers.tolist()  # Convert numpy array to list


# def extract_colors(image_path, n_colors=10):
#     img = cv2.imread(image_path)
#     img = cv2.resize(img, (150, 150))  # optional, to reduce computation
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # Convert to LAB color space
    
#     # Reshape the data
#     data = img.reshape((-1, 3))
    
#     # Use KMeans from cv2 to get the dominant colors
#     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.2)
#     _, labels, centers = cv2.kmeans(data.astype(np.float32), n_colors, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    
#     centers = cv2.cvtColor(centers.reshape((1, n_colors, 3)), cv2.COLOR_LAB2BGR).reshape((n_colors, 3))

#     return centers.tolist()  # Convert numpy array to list


# def extract_colors(image_path, n_colors=10):
#     img = cv2.imread(image_path)
#     img = cv2.resize(img, (150, 150))  # optional, to reduce computation

#     # Reshape the data
#     data = img.reshape((-1, 3))

#     # Use KMeans from cv2 to get the dominant colors
#     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.2)
#     _, labels, centers = cv2.kmeans(data.astype(np.float32), n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

#     return centers.tolist()  # Convert numpy array to list

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')  # Note: Renamed from upload.html to index.html

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Replace spaces with underscores in the filename
    file.filename = file.filename.replace(' ', '_')

    # Handle filenames with multiple dots
    parts = file.filename.split('.')
    if len(parts) > 2:
        filename_without_ext = '_'.join(parts[:-1])
        extension = parts[-1]
        file.filename = f"{filename_without_ext}.{extension}"

    if allowed_file(file.filename):
        ext = os.path.splitext(file.filename)[1].lower()  # Convert extension to lowercase
        if ext == ".jpeg":
            ext = ".jpg"
        base_name = os.path.splitext(file.filename)[0]
        filename = os.path.join(app.config['UPLOAD_FOLDER'], base_name + ext)
        file.save(filename)

        resize_image(filename)
        process_image(filename)
        
        # Create the thumbnail
        base, ext = os.path.splitext(filename)
        if ext.lower() == ".jpeg":
            ext = ".jpg"
        thumbnail_filename = f"{base}_th{ext}"
        create_thumbnail(filename, thumbnail_filename)

        basename = os.path.basename(filename)
        depth_filename = os.path.join(app.config['OUTPUT_FOLDER'], os.path.splitext(basename)[0] + "_depth.jpg")
        os.rename(os.path.join(app.config['OUTPUT_FOLDER'], "output_depthmap.jpg"), depth_filename)

        # Create UUID and save information
        image_uuid = str(uuid.uuid4())
        share_info = {"original_filename": basename}
        with open(os.path.join(app.config['SHARE_FOLDER'], image_uuid + ".json"), 'w') as json_file:
            json.dump(share_info, json_file)

        shareable_link = url_for('share_image', uuid=image_uuid, _external=True)

        return jsonify({
            "image_url": url_for('uploaded_file', filename=basename),
            "depth_image_url": url_for('outputed_file', filename=os.path.basename(depth_filename)),
            "shareable_link": shareable_link
        })

    return jsonify({"error": "File type not allowed"}), 400



def create_thumbnail(image_path, thumbnail_path, thumbnail_size=(256, 256)):
    """Creates a thumbnail of the image preserving its aspect ratio."""
    img = cv2.imread(image_path)
    
    # Calculate aspect ratio and dimensions
    width, height = img.shape[1], img.shape[0]
    new_width, new_height = thumbnail_size
    aspect = width / float(height)
    if aspect > 1:  # landscape
        new_width = thumbnail_size[0]
        new_height = int(new_width / aspect)
    else:  # portrait and square
        new_height = thumbnail_size[1]
        new_width = int(new_height * aspect)

    # Resize the image
    thumbnail = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Save the thumbnail
    cv2.imwrite(thumbnail_path, thumbnail)


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
    #model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

    deploy_env = os.environ.get('DEPLOY_ENV', 'local')

    if deploy_env == 'server':
        model_type = "DPT_Large"
    else:
        model_type = "MiDaS_small"
    logging.info("deploy_env: %s model_type: %s", deploy_env, model_type)

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

    # Extract colors and save to a JSON file

    # colors = extract_colors(os.path.join(app.config['OUTPUT_FOLDER'], "output_depthmap.jpg"))
    # hex_format_colors = [rgb_to_hex_format(color) for color in colors]
    # with open(os.path.join(app.config['OUTPUT_FOLDER'], os.path.splitext(os.path.basename(filename))[0] + "_colors.json"), 'w') as json_file:
    #     json.dump(hex_format_colors, json_file)
    colors = extract_colors(filename)
    hex_format_colors = [rgb_to_hex_format(color) for color in colors]
    with open(os.path.join(app.config['OUTPUT_FOLDER'], os.path.splitext(os.path.basename(filename))[0] + "_colors.json"), 'w') as json_file:
        json.dump(hex_format_colors, json_file)


@app.route('/libs/<filename>')
def libs_file(filename):
    return send_from_directory(os.path.abspath(app.config['LIBS_FOLDER']), filename)

@app.route('/outputs/<filename>')
def outputed_file(filename):
    return send_from_directory(os.path.abspath(app.config['OUTPUT_FOLDER']), filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.abspath(app.config['UPLOAD_FOLDER']), filename)

@app.route('/get-images')
def get_images():
    share_folder = 'share'  # Assuming your share folder is named 'share'
    json_files = [f for f in os.listdir(share_folder) if f.endswith('.json')]

    image_list = []

    for json_filename in json_files:
        json_path = os.path.join(share_folder, json_filename)
        try:
            with open(json_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                image_list.append({
                    "file": data['original_filename'],
                    "uid": json_filename.rsplit('.', 1)[0]  # remove .json extension to get UID
                })
        except Exception as e:
            print(f"Error reading or decoding {json_path}: {str(e)}")

    return jsonify({"images": image_list})


@app.route('/share/<uuid>')
def share_image(uuid):
    try:
        with open(os.path.join(app.config['SHARE_FOLDER'], uuid + ".json"), 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except:
        return jsonify({"error": "Invalid UUID"}), 400


@app.route('/image/<string:uid>')
def share_by_uid(uid):
    return render_template('index.html', uid=uid)        

 
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    app.run(host='0.0.0.0', port=5050, debug=True)


