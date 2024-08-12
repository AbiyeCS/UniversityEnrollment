from __future__ import absolute_import, unicode_literals

import os
from decimal import Decimal

import joblib
import pandas as pd
from celery import shared_task
from django.conf import settings
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from .ai_utils import train_model
from .models import TrainingModel, FeedbackModel


@shared_task
def retrain_model():
    train_model()


@shared_task
def process_training_file(file_id):
    training_file = TrainingModel.objects.get(id=file_id)
    file_path = training_file.file.path

    # Read the file into a DataFrame
    df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)

    X = df[['gpa_score', 'sports_interest_score', 'extracurricular_interest_score','uni_gpa_weight','uni_sports_weight', 'uni_extracurricular_weight',]]
    y = df['accepted']

    # Prepopulate FeedbackModel instances
    feedback_instances = []
    for index, row in df.iterrows():
        feedback_instance = FeedbackModel(
            gpa_score=Decimal(float(row['gpa_score'])),
            sports_interest_score=Decimal(float(row['sports_interest_score'])),
            extracurricular_interest_score=Decimal(float(row['extracurricular_interest_score'])),
            uni_gpa_weight=Decimal(float(row['uni_gpa_weight'])),
            uni_sports_weight=Decimal(float(row['uni_sports_weight'])),
            uni_extracurricular_weight=Decimal(float(row['uni_extracurricular_weight'])),
            accepted=int(row['accepted'])
        )
        feedback_instances.append(feedback_instance)

    # Bulk create FeedbackModel instances
    FeedbackModel.objects.bulk_create(feedback_instances)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Save the trained model
    model_path = os.path.join(settings.MODEL_ROOT, 'ai_recommendation_model.pkl')
    joblib.dump(model, model_path)
    training_file.accuracy = accuracy
    training_file.model_path = model_path
    training_file.save()
    return accuracy



