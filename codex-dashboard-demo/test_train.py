import json
from pathlib import Path

import train


def test_train_and_evaluate_returns_dict_and_expected_keys(tmp_path, monkeypatch):
    result_path = tmp_path / "results.json"
    monkeypatch.setattr(train, "RESULT_PATH", str(result_path))

    results = train.train_and_evaluate()

    assert isinstance(results, dict)
    assert "cross_validation" in results
    assert "oof_evaluation" in results
    assert "test_evaluation" in results
    assert "dataset" in results
    assert "model_name" in results


def test_test_accuracy_is_between_zero_and_one(tmp_path, monkeypatch):
    result_path = tmp_path / "results.json"
    monkeypatch.setattr(train, "RESULT_PATH", str(result_path))

    results = train.train_and_evaluate()
    accuracy = results["test_evaluation"]["accuracy"]

    assert 0.0 <= accuracy <= 1.0


def test_results_json_is_created(tmp_path, monkeypatch):
    result_path = tmp_path / "results.json"
    monkeypatch.setattr(train, "RESULT_PATH", str(result_path))

    results = train.train_and_evaluate()

    assert result_path.exists()

    saved = json.loads(result_path.read_text(encoding="utf-8"))
    assert isinstance(saved, dict)
    assert saved["test_evaluation"]["accuracy"] == results["test_evaluation"]["accuracy"]


def test_cross_validation_metrics_exist(tmp_path, monkeypatch):
    result_path = tmp_path / "results.json"
    monkeypatch.setattr(train, "RESULT_PATH", str(result_path))

    results = train.train_and_evaluate()
    cv = results["cross_validation"]

    assert "scores" in cv
    assert "mean_accuracy" in cv
    assert "std_accuracy" in cv
    assert 0.0 <= cv["mean_accuracy"] <= 1.0
    assert cv["std_accuracy"] >= 0.0
