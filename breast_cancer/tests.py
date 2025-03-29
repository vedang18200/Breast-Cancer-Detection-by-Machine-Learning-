<<<<<<< HEAD
from django.test import TestCase

# Create your tests here.
=======
# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

# Create a larger and balanced dataset
data = {
    'text': [
        # Spam examples
        'Get cheap loans now!', 'Exclusive offer just for you!', 'Win a free iPhone!',
        'Earn money fast!', 'Your account has been hacked!', 'Congratulations! You won a lottery!',
        'Claim your prize now!', 'Buy now and save big!', 'Limited time offer!',
        'Your last chance to win big!', 'Sign up for free!', 'Act now, get rich quick!',
        'You have won a free ticket!', 'Click here to claim your prize!', 'You are the lucky winner!',
        'Get paid for your opinions!', 'Earn money working from home!',
        # Non-spam examples
        'Hello, how are you?', 'Meeting at 10 AM tomorrow.', 'Your appointment is confirmed.',
        'Let’s catch up over coffee.', 'I miss you!', 'Your subscription has expired.',
        'Thanks for your email!', 'Looking forward to our meeting.', 'Have a great day!',
        'Your package is on the way!', 'This is not spam, trust us!', 'I have attached the document.',
        'Let’s discuss your project.', 'Your report is ready.', 'Get your free trial today.',
        'Let’s plan a lunch meeting.'
    ],
    'label': [
        # 1 = Spam, 0 = Non-Spam
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # Spam (17)
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # Non-Spam (16)
    ]
}

# Print dataset details
print(f'Number of texts: {len(data["text"])}')  # Number of texts
print(f'Number of labels: {len(data["label"])}')  # Number of labels

# Adjust the number of labels to match the number of texts
if len(data['text']) > len(data['label']):
    data['label'] += [0] * (len(data['text']) - len(data['label']))
    print(f'Number of labels after adjustment: {len(data["label"])}')

# Ensure the lengths match
assert len(data['text']) == len(data['label']), "Lengths do not match!"

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Split the dataset into features and labels
X = df['text']  # Features: email text
y = df['label']  # Labels: spam or non-spam

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Convert text into numerical features
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

# Create Naive Bayes model
naive_bayes_model = MultinomialNB()

# Train the model with training data
naive_bayes_model.fit(X_train_counts, y_train)

# Predict labels for the test data
y_pred = naive_bayes_model.predict(X_test_counts)

# Evaluate the model
accuracy = metrics.accuracy_score(y_test, y_pred)

# Generate a full classification report
full_report = metrics.classification_report(y_test, y_pred, target_names=["Non-Spam", "Spam"])

# Display results
print(f'Accuracy: {accuracy}')
print(full_report)
>>>>>>> 96ab150 (GUI update)
