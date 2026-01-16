"""Test AI service loading"""
print("Testing AI service...")

try:
    from ai_service import get_ai_service
    print("✅ AI service module imported")
    
    ai = get_ai_service()
    print("✅ AI service instance created")
    
    if ai.summarizer:
        print("✅ Summarizer loaded")
        # Test summarization
        test_text = "This is a test. The web crawler system collects data from various sources. It stores the data in MongoDB and provides a dashboard for viewing and searching."
        summary = ai.summarize_text(test_text)
        print(f"✅ Summary test: {summary}")
    else:
        print("❌ Summarizer not loaded")
    
    if ai.chat_model:
        print("✅ Chat model loaded")
        # Test chat
        response = ai.chat("What data do we have?", "We have crawled data from various sources")
        print(f"✅ Chat test: {response}")
    else:
        print("❌ Chat model not loaded")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
