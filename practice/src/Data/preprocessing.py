from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

def preprocess(X,y):
    
    data_X = X.values
    data_y = y.values
    
    X_train, X_test, y_train, y_test = train_test_split(data_X, data_y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    y_train_encoded = to_categorical(y_train)
    y_test_encoded = to_categorical(y_test)
    
    return X_train_scaled, X_test_scaled, y_train_encoded, y_test_encoded
