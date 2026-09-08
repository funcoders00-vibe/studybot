import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000/api/v1"

def run_tests():
    session = requests.Session()
    print("=== STUDYBOT AI CHATBOT VERIFICATION ===")

    # 1. Test unauthenticated gating
    print("\n1. Testing unauthenticated access gating...")
    res = session.get(f"{BASE_URL}/auth/me")
    assert res.status_code == 401, f"Expected 401, got {res.status_code}"
    print("✓ Unauthenticated access correctly rejected with 401")

    # 2. Login
    print("\n2. Logging in as Tamil (tamil@example.com)...")
    res = session.post(f"{BASE_URL}/auth/login", json={
        "email": "tamil@example.com",
        "password": "studybot-local-password"
    })
    assert res.status_code == 200, f"Login failed: {res.text}"
    user_data = res.json()["data"]["user"]
    print(f"✓ Logged in successfully: {user_data['name']} ({user_data['email']})")

    # 3. Verify session
    res = session.get(f"{BASE_URL}/auth/me")
    assert res.status_code == 200
    print("✓ Session cookie authenticated successfully")

    # 4. Create Chat Session
    print("\n3. Creating new Chat Session...")
    res = session.post(f"{BASE_URL}/chat/sessions", json={"title": "Indian Polity & Freedom Struggle"})
    assert res.status_code == 200, f"Failed to create session: {res.text}"
    session_info = res.json()["data"]
    chat_id = session_info["id"]
    print(f"✓ Chat session created with ID: {chat_id}")

    # 5. List Chat Sessions
    res = session.get(f"{BASE_URL}/chat/sessions")
    assert res.status_code == 200
    sessions = res.json()["data"]
    assert any(s["id"] == chat_id for s in sessions)
    print(f"✓ Found session {chat_id} in sessions list (total sessions: {len(sessions)})")

    # 6. Chat Interaction 1: Explain Indian Constitution
    print("\n4. Testing explanation request: 'Explain the Indian Constitution in simple language.'")
    res = session.post(f"{BASE_URL}/chat/sessions/{chat_id}/messages", json={
        "content": "Explain the Indian Constitution in simple language."
    })
    assert res.status_code == 200, f"Failed message: {res.text}"
    msg_data = res.json()["data"]
    print(f"✓ AI Response received:")
    print(f"   Intent/Action: {msg_data.get('action')}")
    print(f"   Response snippet: {msg_data['message'][:180]}...")

    # 7. Chat Interaction 2: Pasted Study Content
    print("\n5. Testing pasted study content...")
    pasted_text = (
        "India achieved independence from British rule on August 15, 1947. "
        "The Constituent Assembly set up a Drafting Committee on August 29, 1947, under the chairmanship of Dr. B.R. Ambedkar. "
        "The Constitution was adopted on November 26, 1949, and came into full legal effect on January 26, 1950, celebrated as Republic Day."
    )
    res = session.post(f"{BASE_URL}/chat/sessions/{chat_id}/messages", json={
        "content": pasted_text
    })
    assert res.status_code == 200, f"Failed pasted text: {res.text}"
    pasted_resp = res.json()["data"]
    print(f"✓ Pasted content processed:")
    print(f"   Response snippet: {pasted_resp['message'][:180]}...")

    # 8. Chat Interaction 3: Generate MCQs from pasted content
    print("\n6. Testing 'Generate 3 MCQs from this' (grounded in pasted text)...")
    res = session.post(f"{BASE_URL}/chat/sessions/{chat_id}/messages", json={
        "content": "Generate 3 MCQs from this"
    })
    assert res.status_code == 200, f"Failed MCQ generation: {res.text}"
    mcq_resp = res.json()["data"]
    print(f"✓ MCQ Response Action: {mcq_resp.get('action')}")
    mcqs = mcq_resp.get("mcqs", [])
    print(f"✓ Number of MCQs generated in chat: {len(mcqs)}")
    assert len(mcqs) > 0, "Expected at least 1 MCQ"
    for i, q in enumerate(mcqs):
        q_text = q.get('question') or q.get('question_text')
        print(f"   Q{i+1}: {q_text}")
        if 'options' in q and isinstance(q['options'], dict):
            print(f"       A: {q['options'].get('A')} | B: {q['options'].get('B')}")
            print(f"       C: {q['options'].get('C')} | D: {q['options'].get('D')}")
        else:
            print(f"       A: {q.get('option_a')} | B: {q.get('option_b')}")
            print(f"       C: {q.get('option_c')} | D: {q.get('option_d')}")
        print(f"       Correct: {q['correct_option']} | Explanation: {q.get('explanation', '')[:60]}...")
        assert q['correct_option'] in ['A', 'B', 'C', 'D'], f"Invalid option {q['correct_option']}"

    # 9. Chat Interaction 4: Practice intent redirection
    print("\n7. Testing Practice intent: 'I want to practice 5 questions on Indian Polity'...")
    res = session.post(f"{BASE_URL}/chat/sessions/{chat_id}/messages", json={
        "content": "I want to practice 5 questions on Indian Polity"
    })
    assert res.status_code == 200
    practice_resp = res.json()["data"]
    assert practice_resp.get("action") == "OPEN_PRACTICE", f"Expected OPEN_PRACTICE, got {practice_resp.get('action')}"
    params = practice_resp.get("parameters", {})
    print(f"✓ Redirection Action: {practice_resp.get('action')}")
    print(f"   Prefilled Parameters: {params}")
    assert params.get("question_count") == 5 or params.get("question_count") == "5"

    # 10. Chat Interaction 5: Mock Test intent redirection
    print("\n8. Testing Mock Test intent: 'Start a mock test on Indian National Movement for 45 minutes with 20 questions'...")
    res = session.post(f"{BASE_URL}/chat/sessions/{chat_id}/messages", json={
        "content": "Start a mock test on Indian National Movement for 45 minutes with 20 questions"
    })
    assert res.status_code == 200
    mock_resp = res.json()["data"]
    assert mock_resp.get("action") == "OPEN_MOCK_TEST", f"Expected OPEN_MOCK_TEST, got {mock_resp.get('action')}"
    mock_params = mock_resp.get("parameters", {})
    print(f"✓ Redirection Action: {mock_resp.get('action')}")
    print(f"   Prefilled Parameters: {mock_params}")
    assert mock_params.get("duration_minutes") == 45 or mock_params.get("duration_minutes") == "45"
    assert mock_params.get("question_count") == 20 or mock_params.get("question_count") == "20"

    # 11. Practice Test Execution using Chat Content Source
    print("\n9. Testing Practice Test execution using source='CHAT_CONTENT'...")
    res = session.post(f"{BASE_URL}/practice/start", json={
        "number_of_questions": 3,
        "difficulty": "MIXED",
        "source": "CHAT_CONTENT",
        "chat_session_id": chat_id,
        "custom_topic": "Pasted Notes on Indian Independence"
    })
    assert res.status_code == 200, f"Failed practice start: {res.text}"
    prac_test = res.json()["data"]
    test_id = prac_test["test_id"]
    
    # Fetch questions from /tests/{test_id}
    res = session.get(f"{BASE_URL}/tests/{test_id}")
    assert res.status_code == 200
    test_data = res.json()["data"]
    questions = test_data["questions"]
    print(f"✓ Practice Test started with ID: {test_id}, {len(questions)} questions")
    assert len(questions) == 3
    # Check that answers are NOT exposed to the user during test
    for q in questions:
        assert "correct_option" not in q or q.get("correct_option") is None, "SECURITY RISK: correct_option exposed in test questions!"
    print("✓ Answers are properly hidden during active test session")

    # Submit practice test answers
    print("   Submitting practice answers...")
    answers = [{"question_id": q["id"], "selected_option": "A"} for q in questions]
    res = session.post(f"{BASE_URL}/tests/{test_id}/submit", json={"answers": answers})
    assert res.status_code == 200, f"Failed to submit test: {res.text}"
    sub_res = res.json()["data"]
    print(f"✓ Test submitted: Correct {sub_res['correct_answers']}/{sub_res['total_questions']} ({sub_res['score_percentage']}%)")

    # 12. Mock Test Execution with Custom Topic and Duration
    print("\n10. Testing Mock Test execution with custom topic & duration...")
    res = session.post(f"{BASE_URL}/mock-tests/start", json={
        "custom_topic": "Tamil Nadu Heritage & History",
        "number_of_questions": 5,
        "duration_minutes": 20,
        "difficulty": "MEDIUM",
        "chat_session_id": chat_id
    })
    assert res.status_code == 200, f"Failed mock test start: {res.text}"
    mock_test = res.json()["data"]
    mock_id = mock_test["test_id"]

    # Fetch questions from /tests/{mock_id}
    res = session.get(f"{BASE_URL}/tests/{mock_id}")
    assert res.status_code == 200
    mock_data = res.json()["data"]
    mock_qs = mock_data["questions"]
    print(f"✓ Mock Test started with ID: {mock_id}, {len(mock_qs)} questions, duration: {mock_data.get('duration_minutes', 20)}m")
    assert len(mock_qs) == 5

    # Submit mock test answers
    mock_answers = [{"question_id": q["id"], "selected_option": "B"} for q in mock_qs]
    res = session.post(f"{BASE_URL}/tests/{mock_id}/submit", json={"answers": mock_answers})
    assert res.status_code == 200
    print("✓ Mock Test submitted successfully")

    # Review test
    res = session.get(f"{BASE_URL}/tests/{mock_id}/review")
    assert res.status_code == 200
    review_data = res.json()["data"]
    print(f"✓ Mock Test review loaded with explanations for {len(review_data)} questions")

    # 13. Test Syllabus & PYQ Grounding for General Questions
    print("\n11. Testing question generation grounded in official syllabus & PYQs...")
    res = session.post(f"{BASE_URL}/chat/sessions/{chat_id}/messages", json={
        "content": "Generate 2 MCQs on Directive Principles of State Policy based on TNPSC syllabus"
    })
    assert res.status_code == 200
    dpsp_resp = res.json()["data"]
    dpsp_mcqs = dpsp_resp.get("mcqs", [])
    print(f"✓ Generated {len(dpsp_mcqs)} questions for DPSP")
    for q in dpsp_mcqs:
        q_text = q.get('question') or q.get('question_text')
        print(f"   - {q_text}")
        if 'options' in q and isinstance(q['options'], dict):
            print(f"     Options: A: {q['options'].get('A')}, B: {q['options'].get('B')}, C: {q['options'].get('C')}, D: {q['options'].get('D')}")
        else:
            print(f"     Options: A: {q.get('option_a')}, B: {q.get('option_b')}, C: {q.get('option_c')}, D: {q.get('option_d')}")
        print(f"     Source: {q.get('source_book', 'TNPSC')} / Ans: {q.get('correct_option')}")

    print("\n==============================================")
    print("🎉 ALL END-TO-END VERIFICATION CHECKS PASSED!")
    print("==============================================")

if __name__ == "__main__":
    run_tests()
