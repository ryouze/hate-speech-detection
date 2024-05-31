# predict.py


import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("./models")
model = AutoModelForSequenceClassification.from_pretrained("./models")

# Ensure the model uses the GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def predict(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Make prediction
    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    confidence, predicted_class = torch.max(probabilities, dim=-1)

    return predicted_class.item(), confidence.item()


while True:
    prediction, confidence = predict(input("Enter text: "))

    # print(
    #     f"Prediction: {'Hate speech (1)' if prediction == 1 else 'Not hate speech (0)'}"
    # )
    print(f"Confidence: {confidence:.4f}")
