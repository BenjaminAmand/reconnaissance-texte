import os

WIDTH = 10
HEIGHT = 10
CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
CHARSALIASES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "minA", "minB", "minC", "minD", "minE", "minF", "minG", "minH", "minI", "minJ", "minK", "minL", "minM", "minN", "minO", "minP", "minQ", "minR", "minS", "minT", "minU", "minV", "minW", "minX", "minY", "minZ"]

def getPath(char):
    if not os.path.exists(f"{WIDTH}x{HEIGHT}/TrainingModel"):
        for c in CHARS:
            os.makedirs(f"{WIDTH}x{HEIGHT}/TrainingModel/{CHARSALIASES[CHARS.index(c)]}")
    return f"{WIDTH}x{HEIGHT}/TrainingModel/{CHARSALIASES[CHARS.index(char)]}"