from app.ai.engine import AIEngine


def main():
    engine = AIEngine()

    message = "My payment was deducted but my order failed."

    result = engine.triage(message)

    print("\nAI DECISION")
    print("=" * 50)
    print(result.decision.model_dump_json(indent=2))

    print("\nAI USAGE")
    print("=" * 50)
    print(f"Latency: {result.latency_ms:.2f} ms")
    print(f"Input tokens: {result.input_tokens}")
    print(f"Output tokens: {result.output_tokens}")
    print(f"Total tokens: {result.total_tokens}")
    print(f"Estimated cost: ${result.estimated_cost_usd}")


if __name__ == "__main__":
    main()