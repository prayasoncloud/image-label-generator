import boto3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO

def detect_labels_with_bounding_boxes(bucket_name, folder_name):
    """Detects labels in the images stored in Amazon S3 bucket using Amazon Rekognition."""
    # Initialize the Rekognition client
    rekognition = boto3.client('rekognition')

    labels_per_image = {}

    # List objects in the specified folder
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=folder_name):
        object_key = obj.key
        if object_key.endswith('.jpg') or object_key.endswith('.jpeg') or object_key.endswith('.png'):
            # Call Rekognition's detect_labels API
            response = rekognition.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name': object_key
                    }
                },
                MaxLabels=10  # Adjust the number of labels as needed
            )
            labels_per_image[object_key] = response['Labels']

    return labels_per_image

def visualize_labels_with_bounding_boxes(bucket_name, labels_per_image):
    """Visualizes labels with bounding boxes on the images using Matplotlib."""
    # Initialize S3 client
    s3 = boto3.client('s3')

    # Iterate over each image and its labels
    for object_key, labels in labels_per_image.items():
        # Get image from S3 bucket
        obj = s3.get_object(Bucket=bucket_name, Key=object_key)
        image_bytes = obj['Body'].read()
        img = Image.open(BytesIO(image_bytes))

        # Display the image
        plt.figure(figsize=(10, 8))
        plt.imshow(img)
        ax = plt.gca()

        # Plot bounding boxes
        for label in labels:
            for instance in label.get('Instances', []):
                box = instance['BoundingBox']
                left = img.width * box['Left']
                top = img.height * box['Top']
                width = img.width * box['Width']
                height = img.height * box['Height']

                # Create a Rectangle patch
                rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor='r', facecolor='none')

                # Add the patch to the Axes
                ax.add_patch(rect)

                # Add label name near the bounding box with leader lines
                label_text = label['Name']
                label_confidence = round(label['Confidence'], 2)
                label_position = (left + width / 2, top - 5)

                # Draw a leader line from the center of the bounding box to the label position
                ax.plot([left + width / 2, label_position[0]], [top, label_position[1]], color='r', linewidth=1)

                # Add label text
                plt.text(*label_position, f"{label_text} ({label_confidence}%)", color='r', fontsize=8)



        plt.axis('off')
        plt.title(f"Image: {object_key}")
        plt.show()

def main():
    """Main function to analyze images stored in Amazon S3 bucket."""
    # Replace 'your-bucket-name' with the appropriate bucket name
    bucket_name = 'rekognition-custom-projects-us-east-2-34935d4dc7'

    # Replace 'your-folder-name' with the folder name in the S3 bucket containing the images
    folder_name = 'mkdir'

    # Detect labels using Amazon Rekognition
    labels_per_image = detect_labels_with_bounding_boxes(bucket_name, folder_name)

    # Visualize labels with bounding boxes
    visualize_labels_with_bounding_boxes(bucket_name, labels_per_image)

if __name__ == "__main__":
    main()
