import sys

from networksecurity.exception.exception import NetworkSecurityException


class NetworkModel:
    
    def __init__(self,preprocessor, model) -> None:
        """
        The function initializes the model and preprocessing object.

        :param model: The model that you want to use for prediction
        :param preprocessing_object: This is the object that will be used to preprocess the data
        """
        try:
            self.model = model
            self.preprocessor = preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    def predict(self, X):
        """
        The function takes in a dataframe, preprocesses it, and then makes a prediction using the model

        :param X: The input data for which we want to make predictions
        :return: The predicted values for the input data X.
        """
        try:
            X_preprocessed = self.preprocessor.transform(X)
            return self.model.predict(X_preprocessed)
        except Exception as e:
            raise NetworkSecurityException(e, sys)