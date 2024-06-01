"""
Script: train.py

Trains a [DistilBERT](https://huggingface.co/docs/transformers/en/model_doc/distilbert) for predicting if a given text is hateful or not.

If a text is not hateful, the "labels" column will be 0. If a text is hateful, the "labels" column will be 1.
"""

import numpy as np
import pandas as pd
import torch
from lib import filepaths
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)

from datasets import Dataset

# Check if a GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load dataset
df = pd.read_csv(filepaths.datasets / "BAN-PL_1.csv")

# Original size
print("Original size:", len(df))

# Reduce dataset size to 1% for faster training (optional)
df = df.sample(frac=0.01, random_state=42)

# Reduced size
print("Reduced size:", len(df))

# Split dataset into train and test
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Convert DataFrame to Hugging Face Dataset
train_dataset = Dataset.from_pandas(train_df)  # type: ignore
test_dataset = Dataset.from_pandas(test_df)  # type: ignore

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("Geotrend/distilbert-base-pl-cased")
model = AutoModelForSequenceClassification.from_pretrained(
    "Geotrend/distilbert-base-pl-cased", num_labels=2
).to(device)


# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding=True)


train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# Define the data collator
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)


# Define the compute metrics function
def compute_metrics(p):
    pred, labels = p
    pred = np.argmax(pred, axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, pred, average="binary"
    )
    acc = accuracy_score(labels, pred)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}


# Define the training arguments
training_args = TrainingArguments(
    output_dir=str(filepaths.models / "results"),
    eval_strategy="epoch",
    learning_rate=5e-5,  # Increased learning rate
    per_device_train_batch_size=32,  # Larger batch size
    per_device_eval_batch_size=32,  # Larger evaluation batch size
    num_train_epochs=1,  # Reduced number of epochs
    weight_decay=0.01,
    gradient_accumulation_steps=2,  # Simulate larger batch size
    fp16=torch.cuda.is_available(),  # Enable mixed precision training if GPU is available
    logging_dir=str(filepaths.models / "logs"),
    logging_steps=1,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained(filepaths.models)
tokenizer.save_pretrained(filepaths.models)
