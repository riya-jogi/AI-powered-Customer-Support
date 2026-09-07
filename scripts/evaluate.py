import json
import statistics
from pathlib import Path

from app.ai.engine import AIEngine


DATASET_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "triage_dataset.json"
)

REQUIRED_FIELDS = {
    "id",
    "message",
    "expected_category",
    "expected_priority",
    "expected_needs_human",
    "difficulty",
}


def load_dataset() -> list[dict]:
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    if not isinstance(dataset, dict):
        raise ValueError("Dataset root must be a JSON object.")

    records = dataset.get("records")

    if not isinstance(records, list):
        raise ValueError(
            "Dataset must contain a 'records' list."
        )

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(
                f"Dataset record {index} must be a JSON object."
            )

        missing_fields = REQUIRED_FIELDS - record.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"Dataset record {index} is missing required fields: "
                f"{missing}."
            )

    return records


def calculate_accuracy(
    correct: int,
    total: int,
) -> float:
    if total == 0:
        return 0.0

    return (correct / total) * 100


def main():
    dataset = load_dataset()

    engine = AIEngine()

    results = []

    category_correct = 0
    priority_correct = 0
    human_correct = 0

    latencies = []
    total_input_tokens = 0
    total_output_tokens = 0
    total_tokens = 0
    total_cost = 0.0

    for index, item in enumerate(dataset, start=1):
        message = item["message"]

        print(
            f"\n[{index}/{len(dataset)}] "
            f"Processing {item['id']}..."
        )

        try:
            result = engine.triage(message)

            decision = result.decision

            category_match = (
                decision.category
                == item["expected_category"]
            )

            priority_match = (
                decision.priority
                == item["expected_priority"]
            )

            human_match = (
                decision.needs_human
                == item["expected_needs_human"]
            )

            if category_match:
                category_correct += 1

            if priority_match:
                priority_correct += 1

            if human_match:
                human_correct += 1

            latencies.append(result.latency_ms)

            if result.input_tokens is not None:
                total_input_tokens += result.input_tokens

            if result.output_tokens is not None:
                total_output_tokens += result.output_tokens

            if result.total_tokens is not None:
                total_tokens += result.total_tokens

            if result.estimated_cost_usd is not None:
                total_cost += result.estimated_cost_usd

            results.append(
                {
                    "id": item["id"],
                    "message": message,
                    "expected": {
                        "category": item["expected_category"],
                        "priority": item["expected_priority"],
                        "needs_human": item["expected_needs_human"],
                    },
                    "actual": {
                        "category": decision.category,
                        "priority": decision.priority,
                        "needs_human": decision.needs_human,
                        "confidence": decision.confidence,
                        "summary": decision.summary,
                        "suggested_action": decision.suggested_action,
                    },
                    "metrics": {
                        "latency_ms": result.latency_ms,
                        "input_tokens": result.input_tokens,
                        "output_tokens": result.output_tokens,
                        "total_tokens": result.total_tokens,
                        "estimated_cost_usd": result.estimated_cost_usd,
                    },
                    "matches": {
                        "category": category_match,
                        "priority": priority_match,
                        "needs_human": human_match,
                    },
                }
            )

            print(
                f"  Category: {decision.category} "
                f"({'✓' if category_match else '✗'})"
            )

            print(
                f"  Priority: {decision.priority} "
                f"({'✓' if priority_match else '✗'})"
            )

            print(
                f"  Human: {decision.needs_human} "
                f"({'✓' if human_match else '✗'})"
            )

        except Exception as exc:
            print(f"  ERROR: {exc}")

            results.append(
                {
                    "id": item["id"],
                    "message": message,
                    "error": str(exc),
                }
            )

    total = len(dataset)

    category_accuracy = calculate_accuracy(
        category_correct,
        total,
    )

    priority_accuracy = calculate_accuracy(
        priority_correct,
        total,
    )

    human_accuracy = calculate_accuracy(
        human_correct,
        total,
    )

    average_latency = (
        statistics.mean(latencies)
        if latencies
        else 0.0
    )

    median_latency = (
        statistics.median(latencies)
        if latencies
        else 0.0
    )

    report = {
        "total_messages": total,
        "category_accuracy": category_accuracy,
        "priority_accuracy": priority_accuracy,
        "human_escalation_accuracy": human_accuracy,
        "average_latency_ms": average_latency,
        "median_latency_ms": median_latency,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens": total_tokens,
        "total_estimated_cost_usd": total_cost,
        "results": results,
    }

    failures = [
        result
        for result in results
        if "error" in result
        or ("matches" in result and not all(result["matches"].values()))
    ]
    report["failures"] = failures

    output_path = (
        Path(__file__).resolve().parent.parent
        / "evaluation_results.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\n")
    print("=" * 60)
    print("FRONTLINE AI EVALUATION")
    print("=" * 60)

    print(f"Total messages: {total}")

    print(
        f"Category accuracy: "
        f"{category_accuracy:.2f}%"
    )

    print(
        f"Priority accuracy: "
        f"{priority_accuracy:.2f}%"
    )

    print(
        f"Human escalation accuracy: "
        f"{human_accuracy:.2f}%"
    )

    print(
        f"Average latency: "
        f"{average_latency:.2f} ms"
    )

    print(
        f"Median latency: "
        f"{median_latency:.2f} ms"
    )

    print(
        f"Total input tokens: "
        f"{total_input_tokens}"
    )

    print(
        f"Total output tokens: "
        f"{total_output_tokens}"
    )

    print(
        f"Total tokens: "
        f"{total_tokens}"
    )

    print(
        f"Estimated cost: "
        f"${total_cost:.6f}"
    )

    print("=" * 60)

    print(f"\nFailures: {len(failures)}")

    for failure in failures:
        if "error" in failure:
            print(f"- {failure['id']}: ERROR: {failure['error']}")
        else:
            print(
                f"- {failure['id']}: "
                f"expected={failure['expected']} "
                f"actual={failure['actual']}"
            )

    print(
        f"\nDetailed report saved to: "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()