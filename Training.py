import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.utils import to_categorical
from Model import model
import Globals

def image_to_binary_array(image_path):
    img = Image.open(image_path)
    img = img.convert("L")
    img = img.resize((Globals.WIDTH, Globals.HEIGHT))
    img_array = np.array(img)
    binary_array = (img_array > 128).astype(int) 
    return binary_array.reshape((Globals.WIDTH, Globals.HEIGHT, 1))

Globals.CHARSNormalized = []
labels = []

for char in Globals.CHARS:
    folder = Globals.getPath(char)
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            image_path = os.path.join(folder, filename)
            Globals.CHARSNormalized.append(image_to_binary_array(image_path))
            labels.append(Globals.CHARS.index(char))

X = np.array(Globals.CHARSNormalized)
y = to_categorical(labels)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model.fit(X_train, y_train, epochs=25, batch_size=25, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

model.save("model.h5")