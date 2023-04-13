from Train.model import Softmax
from Data.load import load_data
from Data.preprocessing import preprocess
import numpy as np


def train_model():
    
    # load
    X, y = load_data()
    
    # preprocessing
    X_train, X_test, y_train, y_test = preprocess(X, y)
    
    model = Softmax()
    
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    
    # train starts
    print("train starts")
    model.fit(X_train, y_train, epochs=200, validation_data=(X_test, y_test))
    print("train ends")
    
    # y_pred = model.predict(X_test)
    # print(np.argmax(y_pred))
