import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from aiadmin.models import TrainingModel, FeedbackModel
from sapms import settings
from university_panel.models import UniversityAIWeight


def collect_data():
    feed_back_models = FeedbackModel.objects.all()
    data = []

    for obj in feed_back_models:
        data.append([
            obj.gpa_score,
            obj.sports_interest_score,
            obj.extracurricular_interest_score,
            obj.uni_gpa_weight,
            obj.uni_sports_weight,
            obj.uni_extracurricular_weight,
            obj.accepted
        ])

    df = pd.DataFrame(data, columns=[
        'gpa_score', 'sports_interest_score', 'extracurricular_interest_score',
        'uni_gpa_weight', 'uni_sports_weight', 'uni_extracurricular_weight', 'accepted'
    ])

    # Drop rows with missing values
    df.dropna(inplace=True)

    return df


def train_model():
    df = collect_data()
    if df is None:
        print("These is no data to train on")
        return False
    X = df.drop(columns=['accepted'])
    y = df['accepted']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Save the model
    training_file = TrainingModel.objects.create()
    model_path = os.path.join(settings.MODEL_ROOT, 'ai_recommendation_model.pkl')
    joblib.dump(model, model_path)
    training_file.accuracy = accuracy
    training_file.model_path = model_path
    training_file.save()


def load_model():
    model_path = os.path.join(settings.MODEL_ROOT, 'ai_recommendation_model.pkl')
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    else:
        return None


def create_feedback_entry(application, accepted_status):
    try:
        university_weights = UniversityAIWeight.objects.get(university_profile=application.university)
        FeedbackModel.objects.create(
            gpa_score=application.student.education_gpa_score or 0,
            sports_interest_score=application.student.sports_interest_score or 0,
            extracurricular_interest_score=application.student.extracurricular_interest_score or 0,
            uni_gpa_weight=university_weights.gpa_weight,
            uni_sports_weight=university_weights.sports_interest_weight,
            uni_extracurricular_weight=university_weights.extracurricular_interest_weight,
            accepted=accepted_status
        )
    except UniversityAIWeight.DoesNotExist:
        print(f"University weights not found for university: {application.university}")
