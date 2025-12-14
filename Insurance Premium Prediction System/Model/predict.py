import pandas as pd
import pickle

# Import the model
with open('Model/insurance_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Get class labels from the model
class_labels = model.classes_.tolist()  # This will be ['Low', 'Medium', 'High']


def predict_output(user_input: dict):

    input_df = pd.DataFrame([user_input])
    
    predicted_class = model.predict(input_df)[0]  # Predict the class

    # Get Probablitites for each class
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    # Create mapping {class: probability}
    class_probabilities = dict(zip(class_labels, map(lambda p: round(p,4), probabilities)))

    return {
        "predicted_category": predicted_class,
        "Confidence": confidence,
        "class_probabilities": class_probabilities
    }