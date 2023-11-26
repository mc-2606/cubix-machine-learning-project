import cv2

# Read a sample image
image = cv2.imread('your_image.jpg')  # Replace 'your_image.jpg' with the path to your image

# Specify the new width and height
new_width = 320
new_height = 240

# Resize the image
resized_image = cv2.resize(image, (new_width, new_height))

# Display the original and resized images
cv2.imshow('Original Image', image)
cv2.imshow('Resized Image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()