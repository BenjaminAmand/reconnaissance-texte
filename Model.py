import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Définir le modèle
model = Sequential()

# Couche convolutionnelle + max pooling
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(10, 10, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Ajouter une autre couche convolutionnelle
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Aplatir les sorties des couches précédentes
model.add(Flatten())

# Couche dense avec 128 neurones
model.add(Dense(128, activation='relu'))

# Couche de sortie pour 36 classes (A-Z + 0-9)
model.add(Dense(36, activation='softmax'))

# Compiler le modèle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])