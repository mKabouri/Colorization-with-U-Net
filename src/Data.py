import numpy as np
import cv2
import os
import config
    

def loadData(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

class Data():
    def __init__(self):
        self.labelNames = np.array([loadData(config.labelNamesFile)])
        self.dataset = np.array([loadData(os.path.join(config.dataDir, x)) for x in config.dataFiles])
        self.X_train, self.y_train, self.X_test, self.y_test = self.__getLearningData()
        
    def rowToMatrix(self, batchIndex, rowIndex):
        assert batchIndex < 5 and batchIndex >= 0, 'We have only 5 batches'
        assert rowIndex < 10000 and rowIndex >= 0, 'We have 10000 rows (images) per batch'
        return self.dataset[batchIndex][b'data'][rowIndex].reshape(3, 32, 32).T

    def getClass(self, batchIndex, rowIndex):
        assert batchIndex < 5 and batchIndex >= 0, 'We have only 5 batches'
        assert rowIndex < 10000 and rowIndex >= 0, 'We have 10000 rows (images) per batch'
        return self.labelNames[0][b'label_names'][self.dataset[batchIndex][b'labels'][rowIndex]].decode("utf-8")

    def toGray(self, img):
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    def __getLearningData(self):
        y_train = np.array([x.reshape(3, 32, 32).T for t in self.dataset[:len(self.dataset) - 1] for x in t[b'data']])
        y_test = np.array([x.reshape(3, 32, 32).T for x in self.dataset[len(self.dataset)-1][b'data']])
        X_train = np.array([self.toGray(y) for y in y_train])
        X_test = np.array([self.toGray(y) for y in y_test])
        return X_train, y_train, X_test, y_test
    

if __name__ == '__main__':
    
    data = Data()
    
    print(data.dataset[0].keys(), data.dataset[1].keys())
    #print(data.dataset[len(data.dataset)-1].keys())
    #print(data.labelNames)
    """
    # show an image from dataset   
    img = data.rowToMatrix(0, 2)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print(data.getClass(0, 2))
    
    gray_img = data.toGray(img)
    
    cv2.imshow('image 2', gray_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print(img.shape)
    print(gray_img.shape)
    
    print("Ok")
        
    # Show from X_train and y_train
    cv2.imshow('image X_train', data.X_train[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    cv2.imshow('image y_train', data.y_train[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("Ok")  
    """