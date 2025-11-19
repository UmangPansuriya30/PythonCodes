import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Load images
img1 = cv2.imread("./images/1.png")
img2 = cv2.imread("./images/2.png")

# Convert to grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

cv2.imshow("Gray Image 1", gray1)
cv2.imshow("Gray Image 2", gray2)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Resize second image to match the first (if needed)
gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))
img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

# Compute SSIM
score, diff = ssim(gray1, gray2, full=True)
print("SSIM Score:", score)

# Scale diff to 0–255
diff = (diff * 255).astype("uint8")

# Threshold to create a binary mask of differences
_, thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# Create a red mask
red_mask = np.zeros_like(img1)
red_mask[:, :] = (0, 0, 255)  # pure red

# Apply red where differences exist
diff_mask = img1.copy()
diff_mask[thresh == 255] = red_mask[thresh == 255]

# Save results
cv2.imwrite("./images/diff_mask_red.png", diff_mask)
cv2.imwrite("./images/diff_gray.png", diff)      # optional: raw SSIM map
cv2.imwrite("./images/diff_thresh.png", thresh)  # optional: binary mask
