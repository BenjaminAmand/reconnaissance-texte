class Network:
    def __init__(self, network):
        self.network = network
        
    def apply_network(self, matrix):
        for i in range(10):
            if matrix[0][i] == 1:
                print(i)
    
