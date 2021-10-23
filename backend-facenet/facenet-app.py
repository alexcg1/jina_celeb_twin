import pretty_errors
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(image_size=160, margin=20)

# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()


img = Image.open("data/alex.jpg")

# Get cropped and prewhitened image tensor
# img_cropped = mtcnn(img, save_path=<optional save path>)
img_cropped = mtcnn(img)

# Calculate embedding (unsqueeze to add batch dimension)
img_embedding = resnet(img_cropped.unsqueeze(0))

# ndarray = img_embedding.numpy()
ndarray = img_embedding.detach().numpy()

# Or, if using for VGGFace2 classification
# resnet.classify = True
# img_probs = resnet(img_cropped.unsqueeze(0))

# print(img_probs)
