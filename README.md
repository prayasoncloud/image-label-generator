
# Image labels generator using Amazon Rekoginition

In this project, we developed a Python app to generate the process of analyzing images stored in an Amazon S3 bucket.Use of Amazon Rekognition, our script detects labels associated with objects within the images and visualizes the results with bounding boxes and labels using the Matplotlib library.


## 🛠 Services
AWS S3, Amazon Rekognition, AWS CLI, AWS SDK, Boto3 and Python..


![alt text](https://github.com/prayasoncloud/image-label-generator/blob/main/chart-diagram.png)


Install Dependencies:
Ensure you have Python installed on your system. Additionally, you need to install the required Python packages. You can install them using pip:


**pip install boto3 matplotlib Pillow**

Configure AWS CLI:
Make sure you have the AWS CLI installed and configured on your system with the appropriate IAM user credentials. You can configure it by running:


**aws configure**

Follow the prompts to enter your Access Key ID, Secret Access Key, AWS Region, and output format.


Run the app:

**python main.py**

This command will run the app, fetch the image from the specified S3 bucket, detect labels using Amazon Rekognition, and visualize the results with bounding boxes using Matplotlib
