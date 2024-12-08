from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
# Download link for the finetuned model:
# https://drive.google.com/drive/folders/1x0wKNL8-Aa6pFdkhXxhyr_voHUgR8gX4
# Load the fine-tuned model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("./finetuned_model")
tokenizer = AutoTokenizer.from_pretrained("./finetuned_model")

# Move the model to the appropriate device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

# Define the emotion labels as per your configuration
emotion_labels = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", 
    "curiosity", "desire", "disappointment", "disapproval", "disgust", "embarrassment", 
    "excitement", "fear", "gratitude", "grief", "joy", "love", "nervousness", "optimism", 
    "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"
]

# Function to predict emotions for custom input
def predict_emotions(text, model=model, tokenizer=tokenizer, threshold=0.2):
    """
    Predict emotions from the input text using the fine-tuned model.

    Args:
        text (str): Input text.
        model (transformers.PreTrainedModel): The fine-tuned model.
        tokenizer (transformers.PreTrainedTokenizer): Tokenizer for the model.
        threshold (float): Threshold to filter out low-confidence emotions.

    Returns:
        dict: Predicted emotions with their probabilities.
    """
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
    inputs = {key: value.to(device) for key, value in inputs.items()}  # Move to device (GPU/CPU)

    # Get model predictions
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.sigmoid(logits).squeeze().cpu().numpy()  # Convert logits to probabilities

    # Interpret the predictions
    predicted_emotions = {emotion_labels[i]: probabilities[i] for i in range(len(probabilities)) if probabilities[i] > threshold}
    return predicted_emotions


