from app.ai.engine import AIEngine


def main():
    engine = AIEngine()

    message = "मेरा पेमेंट फेल हो गया लेकिन मेरे बैंक अकाउंट से पैसे कट गए।"

    decision = engine.triage(message)

    print("\nAI DECISION")
    print("=" * 50)
    print(decision.model_dump_json(indent=2))


if __name__ == "__main__":
    main()