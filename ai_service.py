"""
AI Service for Chat and Summarization
Uses lightweight local models (DistilBART, GPT-2)
"""
from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

class AIService:
    def __init__(self):
        """Initialize lightweight AI models"""
        self.summarizer = None
        self.chat_model = None
        
        try:
            print("🤖 Loading AI models (this may take a moment)...")
            
            # Use DistilBART for summarization (smaller, faster)
            print("   Loading summarization model (DistilBART)...")
            self.summarizer = pipeline(
                "summarization",
                model="sshleifer/distilbart-cnn-12-6",
                device=-1  # CPU
            )
            print("   ✅ Summarization model loaded")
            
            # Use GPT-2 small for chat (lightweight)
            print("   Loading chat model (GPT-2 small)...")
            self.chat_model = pipeline(
                "text-generation",
                model="gpt2",
                device=-1  # CPU
            )
            print("   ✅ Chat model loaded")
            
            print("✅ AI Service ready!")
        except Exception as e:
            print(f"❌ Error loading AI models: {e}")
            print("   AI features will be limited")
    
    def summarize_text(self, text, max_length=130, min_length=30):
        """
        Summarize text content
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            
        Returns:
            Summary text
        """
        if not self.summarizer:
            return "AI summarization not available. Models failed to load."
        
        try:
            # Clean and truncate text
            text = text.strip()
            if len(text) < 50:
                return text
            
            # DistilBART can handle up to 1024 tokens
            if len(text) > 1000:
                text = text[:1000]
            
            result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            
            return result[0]['summary_text']
        except Exception as e:
            return f"Error summarizing: {str(e)}"
    
    def summarize_data_items(self, items, max_items=10):
        """
        Summarize multiple data items
        
        Args:
            items: List of data items from MongoDB
            max_items: Maximum number of items to summarize
            
        Returns:
            Combined summary
        """
        if not items:
            return "No data to summarize"
        
        # Combine content from items
        combined_text = ""
        for item in items[:max_items]:
            title = item.get('title', '')
            content = item.get('content', '')
            if title:
                combined_text += f"{title}. "
            if content:
                combined_text += f"{content[:200]} "
        
        # Limit total text length
        if len(combined_text) > 1000:
            combined_text = combined_text[:1000]
        
        if len(combined_text) < 50:
            return combined_text
        
        return self.summarize_text(combined_text, max_length=150, min_length=50)
    
    def chat(self, message, context=""):
        """
        Chat with AI about the data
        
        Args:
            message: User message
            context: Context from database
            
        Returns:
            AI response
        """
        if not self.chat_model:
            return "AI chat not available. Models failed to load."
        
        try:
            # Create a prompt with context
            if context:
                prompt = f"Data context: {context[:300]}\n\nQuestion: {message}\nAnswer:"
            else:
                prompt = f"Question: {message}\nAnswer:"
            
            # Generate response
            response = self.chat_model(
                prompt,
                max_length=len(prompt.split()) + 50,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                pad_token_id=50256
            )
            
            # Extract the generated text
            generated = response[0]['generated_text']
            
            # Get only the answer part
            if "Answer:" in generated:
                answer = generated.split("Answer:")[-1].strip()
                # Clean up the answer
                answer = answer.split("\n")[0].strip()
                if len(answer) > 10:
                    return answer
            
            # Fallback to rule-based response
            return self._rule_based_response(message, context)
            
        except Exception as e:
            print(f"Chat error: {e}")
            return self._rule_based_response(message, context)
    
    def _rule_based_response(self, message, context):
        """Fallback rule-based responses"""
        message_lower = message.lower()
        
        if "how many" in message_lower or "count" in message_lower:
            return f"Based on the available data, I can see information about your crawled content. {context[:200] if context else 'No data available yet.'}"
        
        elif "what" in message_lower or "tell me" in message_lower:
            if context:
                summary = self.summarize_text(context[:800], max_length=100, min_length=30)
                return f"Here's what I found: {summary}"
            else:
                return "I don't have enough data to answer that. Try crawling some sources first!"
        
        elif "summarize" in message_lower:
            if context:
                return self.summarize_text(context[:800])
            else:
                return "No data available to summarize."
        
        else:
            if context:
                return f"I can help you understand your crawled data. Here's a quick summary: {self.summarize_text(context[:800], max_length=80, min_length=30)}"
            else:
                return "I'm your AI assistant! Ask me to summarize data, count items, or tell you about your crawled content. Start by crawling some sources first."
    
    def analyze_data(self, items):
        """
        Analyze data items and provide insights
        
        Args:
            items: List of data items
            
        Returns:
            Analysis summary
        """
        if not items:
            return "No data to analyze"
        
        # Count by type
        types = {}
        sources = {}
        total_images = 0
        total_content_length = 0
        
        for item in items:
            item_type = item.get('type', 'unknown')
            types[item_type] = types.get(item_type, 0) + 1
            
            source = item.get('source_url', 'unknown')
            sources[source] = sources.get(source, 0) + 1
            
            if 'images' in item:
                total_images += len(item['images'])
            
            content = item.get('content', '')
            total_content_length += len(content)
        
        # Create analysis
        analysis = f"📊 Analysis of {len(items)} items:\n\n"
        analysis += f"Content Types:\n"
        for k, v in types.items():
            analysis += f"  • {k.upper()}: {v} items\n"
        
        analysis += f"\nStatistics:\n"
        analysis += f"  • Total Images: {total_images}\n"
        analysis += f"  • Unique Sources: {len(sources)}\n"
        analysis += f"  • Average Content Length: {total_content_length // len(items) if items else 0} characters\n"
        
        # Get AI summary of content
        if len(items) > 0 and self.summarizer:
            analysis += f"\n📝 AI-Generated Summary:\n"
            summary = self.summarize_data_items(items, max_items=5)
            analysis += f"{summary}"
        
        return analysis

# Global AI service instance
ai_service = None

def get_ai_service():
    """Get or create AI service instance"""
    global ai_service
    if ai_service is None:
        ai_service = AIService()
    return ai_service
