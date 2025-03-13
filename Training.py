import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.utils import to_categorical
from Model import model

def image_to_binary_array(image_path, size=(10, 10)):
    img = Image.open(image_path)
    img = img.convert("L")
    img = img.resize(size)
    img_array = np.array(img)
    binary_array = (img_array > 128).astype(int) 
    return binary_array.reshape((10, 10, 1))

chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
charsNormalized = []
labels = []

for char in chars:
    folder = f"TrainingModel/{char}"
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            image_path = os.path.join(folder, filename)
            charsNormalized.append(image_to_binary_array(image_path))
            labels.append(chars.index(char))

X = np.array(charsNormalized)
y = to_categorical(labels)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

model.save("model.h5")