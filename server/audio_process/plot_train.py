import pandas as pd
import matplotlib.pyplot as plt
import os
# Replace 'your_file.csv' with the actual path to your CSV file
csv_file_path = os.path.join(os.path.dirname(__file__), 'history.csv')

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Access each column separately
train_loss = df['Train loss']
train_accuracy = df['Train accuracy']
train_precision = df['Train precision']
train_recall = df['Train recall']
validate_loss = df['Validate loss']
validate_accuracy = df['Validate accuracy']
validate_precision = df['Validate precision']
validate_recall = df['Validate recall']

fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 8))

# Plot training metrics
axes[0].plot(df['Train loss'], label='Train Loss')
axes[0].plot(df['Validate loss'], label='Validate Loss')
axes[0].legend()
axes[1].plot(df['Train accuracy'], label='Train Accuracy')
axes[1].plot(df['Validate accuracy'], label='Validate Accuracy')
axes[1].legend()
axes[2].plot(df['Train precision'], label='Train Precision')
axes[2].plot(df['Validate precision'], label='Validate Precision')
axes[2].legend()
axes[3].plot(df['Train recall'], label='Train Recall')
axes[3].plot(df['Validate recall'], label='Validate Recall')
axes[3].legend()
# axes[0].set_title('Training Metrics')

# Plot validation metrics
# axes[1].set_title('Validation Metrics')

# Adjust layout to prevent overlapping
plt.tight_layout()

# Show the plots
plt.show()
