from backend.services.query.intent_detector import IntentDetector


detector = IntentDetector()

def test_detect_intent_finds_learning_intent():
    intents = detector.detect_intent(["learn", "python"])
    assert ("Learning", 50) in intents


def test_detect_intent_finds_pdf_intent():
    intents = detector.detect_intent(["python", "pdf"])
    assert ("PDF", 50) in intents




def test_detect_intent_can_find_multiple_intents():
    intents = detector.detect_intent(["learn", "pdf"])
    intent_names = [intent[0] for intent in intents]
    assert "Learning" in intent_names
    assert "PDF" in intent_names

def test_detect_intent_returns_empty_list_without_matches():
    intents = detector.detect_intent(["python", "programming"])
    assert intents == []



def test_detect_intent_handles_empty_tokens():
    intents = detector.detect_intent([])
    assert intents == []