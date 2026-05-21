import json
from pathlib import Path

import numpy as np
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_val_predict,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42
RESULT_PATH = "results.json"
CV_N_JOBS = 1
TEST_SIZE = 0.2


def load_dataset():
    dataset = load_wine()
    return {
        "name": "Wine",
        "data": dataset.data,
        "target": dataset.target,
        "feature_names": list(dataset.feature_names),
        "class_names": list(dataset.target_names),
    }


def build_model():
    return Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=2000, random_state=RANDOM_STATE)),
    ])


def split_dataset(features, labels):
    return train_test_split(
        features,
        labels,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=labels,
    )


def evaluate_cross_validation(model, features, labels):
    repeated_cv = RepeatedStratifiedKFold(
        n_splits=5,
        n_repeats=5,
        random_state=RANDOM_STATE,
    )
    oof_cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    cv_scores = cross_val_score(
        model,
        features,
        labels,
        cv=repeated_cv,
        scoring="accuracy",
        n_jobs=CV_N_JOBS,
    )

    oof_predictions = cross_val_predict(
        model,
        features,
        labels,
        cv=oof_cv,
        n_jobs=CV_N_JOBS,
    )

    return {
        "cross_validation": {
            "strategy": "RepeatedStratifiedKFold",
            "n_splits": 5,
            "n_repeats": 5,
            "scoring": "accuracy",
            "scores": [float(score) for score in cv_scores],
            "mean_accuracy": float(np.mean(cv_scores)),
            "std_accuracy": float(np.std(cv_scores)),
        },
        "oof_predictions": oof_predictions,
        "oof_strategy": {
            "strategy": "StratifiedKFold",
            "n_splits": 5,
        },
    }


def build_classification_summary(y_true, y_pred, class_names):
    report = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )
    matrix = confusion_matrix(y_true, y_pred)

    return {
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
    }


def evaluate_test_set(model, x_train, y_train, x_test, y_test, class_names):
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    summary = build_classification_summary(y_test, predictions, class_names)
    summary["accuracy"] = float(accuracy_score(y_test, predictions))

    return summary


def build_results(dataset_info, x_train, x_test, y_train, oof_result, test_result):
    oof_summary = build_classification_summary(
        y_train,
        oof_result["oof_predictions"],
        dataset_info["class_names"],
    )

    return {
        "dataset": dataset_info["name"],
        "model_name": "LogisticRegression + StandardScaler",
        "random_state": RANDOM_STATE,
        "n_samples_total": int(len(dataset_info["data"])),
        "n_features": int(dataset_info["data"].shape[1]),
        "feature_names": dataset_info["feature_names"],
        "class_names": dataset_info["class_names"],
        "train_size": int(len(x_train)),
        "test_size": int(len(x_test)),
        "cross_validation": oof_result["cross_validation"],
        "oof_evaluation": {
            **oof_result["oof_strategy"],
            **oof_summary,
            "accuracy": float(oof_summary["classification_report"]["accuracy"]),
        },
        "test_evaluation": test_result,
    }


def save_results(results, result_path=RESULT_PATH):
    Path(result_path).write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def train_and_evaluate(result_path=RESULT_PATH):
    dataset_info = load_dataset()
    x_train, x_test, y_train, y_test = split_dataset(
        dataset_info["data"],
        dataset_info["target"],
    )

    model = build_model()
    oof_result = evaluate_cross_validation(model, x_train, y_train)
    test_result = evaluate_test_set(
        build_model(),
        x_train,
        y_train,
        x_test,
        y_test,
        dataset_info["class_names"],
    )

    results = build_results(
        dataset_info,
        x_train,
        x_test,
        y_train,
        oof_result,
        test_result,
    )
    save_results(results, result_path=result_path)
    return results


if __name__ == "__main__":
    results = train_and_evaluate()

    print("\n=== Model Summary ===")
    print("Dataset:", results["dataset"])
    print("Model:", results["model_name"])
    print("Train size:", results["train_size"])
    print("Test size:", results["test_size"])

    print("\n=== Cross Validation ===")
    print(
        f"CV Accuracy: {results['cross_validation']['mean_accuracy']:.4f} "
        f"(± {results['cross_validation']['std_accuracy']:.4f})"
    )

    print("\n=== Test Evaluation ===")
    print(f"Test Accuracy: {results['test_evaluation']['accuracy']:.4f}")

    print("\nresults.json 파일 저장 완료")
