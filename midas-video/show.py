import numpy as np
import matplotlib.pyplot as plt
import cv2

# Load the depth image
depth_image_path = "outputs/output_depthmap.jpg"
depth_img = cv2.imread(depth_image_path, cv2.IMREAD_GRAYSCALE)

# Create a meshgrid for the X and Y coordinates
x = np.linspace(0, depth_img.shape[1], depth_img.shape[1])
y = np.linspace(0, depth_img.shape[0], depth_img.shape[0])
x, y = np.meshgrid(x, y)

# Use the depth image values for Z coordinates
z = depth_img

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis')

# Invert the Y axis for a better view
ax.invert_yaxis()

plt.show()
