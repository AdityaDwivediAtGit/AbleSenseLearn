import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
import heapq
from typing import List, Dict, Tuple
import json

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextSimplifier:
    """AI-powered text simplification service"""
    
    def __init__(self, use_transformer=True):
        """
        Initialize the text simplifier
        
        Args:
            use_transformer: Whether to use transformer models (requires internet)
        """
        self.use_transformer = use_transformer
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        
        # Simple synonym dictionary for common complex words
        self.synonym_dict = {
            'utilize': 'use',
            'ascertain': 'find out',
            'commence': 'start',
            'terminate': 'end',
            'approximately': 'about',
            'demonstrate': 'show',
            'fabricate': 'make',
            'illuminate': 'light up',
            'magnitude': 'size',
            'necessitate': 'need',
            'obtain': 'get',
            'participate': 'take part',
            'require': 'need',
            'sufficient': 'enough',
            'terminology': 'words',
            'utilization': 'use',
            'velocity': 'speed',
            'comprehend': 'understand',
            'elucidate': 'explain',
            'facilitate': 'help'
        }
        
        # Sentence patterns to simplify
        self.complex_patterns = [
            (r'\bnot only\b.*\bbut also\b', 'both'),
            (r'\bdue to the fact that\b', 'because'),
            (r'\bin order to\b', 'to'),
            (r'\bwith regard to\b', 'about'),
            (r'\bat this point in time\b', 'now'),
            (r'\bprior to\b', 'before'),
            (r'\bsubsequent to\b', 'after'),
        ]
        
    def simplify(self, text: str, level: str = 'intermediate') -> str:
        """
        Simplify text to specified level
        
        Args:
            text: Input text to simplify
            level: Simplification level ('basic', 'intermediate', 'advanced')
            
        Returns:
            Simplified text
        """
        if not text or not text.strip():
            return text
        
        # Step 1: Clean and preprocess
        cleaned_text = self._preprocess_text(text)
        
        # Step 2: Apply simplification based on level
        if level == 'basic':
            simplified = self._simplify_basic(cleaned_text)
        elif level == 'intermediate':
            simplified = self._simplify_intermediate(cleaned_text)
        else:  # advanced
            simplified = self._simplify_advanced(cleaned_text)
        
        # Step 3: Post-process and format
        final_text = self._postprocess_text(simplified)
        
        return final_text
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for simplification"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common punctuation issues
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        text = re.sub(r'([.,!?;:])(\w)', r'\1 \2', text)
        
        return text
    
    def _simplify_basic(self, text: str) -> str:
        """Basic simplification - very simple sentences"""
        sentences = sent_tokenize(text)
        simplified_sentences = []
        
        for sentence in sentences:
            # Replace complex words with simple synonyms
            words = word_tokenize(sentence)
            simple_words = []
            
            for word in words:
                lower_word = word.lower()
                if lower_word in self.synonym_dict:
                    simple_words.append(self.synonym_dict[lower_word])
                else:
                    simple_words.append(word)
            
            # Reconstruct sentence
            simple_sentence = ' '.join(simple_words)
            
            # Break long sentences
            if len(simple_words) > 15:
                # Try to break at conjunctions
                simple_sentence = self._break_long_sentence(simple_sentence)
            
            simplified_sentences.append(simple_sentence)
        
        return ' '.join(simplified_sentences)
    
    def _simplify_intermediate(self, text: str) -> str:
        """Intermediate simplification - balance of simplicity and detail"""
        # Apply pattern replacements
        for pattern, replacement in self.complex_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        sentences = sent_tokenize(text)
        simplified_sentences = []
        
        for sentence in sentences:
            # Remove unnecessary clauses
            sentence = self._remove_unnecessary_clauses(sentence)
            
            # Replace passive voice with active voice where possible
            sentence = self._convert_to_active_voice(sentence)
            
            # Simplify verb phrases
            sentence = self._simplify_verb_phrases(sentence)
            
            simplified_sentences.append(sentence)
        
        return ' '.join(simplified_sentences)
    
    def _simplify_advanced(self, text: str) -> str:
        """Advanced simplification - maintain meaning but simplify structure"""
        # Try to use transformer model if available
        if self.use_transformer:
            try:
                return self._simplify_with_transformer(text)
            except:
                pass  # Fall back to rule-based
        
        # Combine basic and intermediate approaches
        intermediate = self._simplify_intermediate(text)
        
        # Add summarization for very long texts
        if len(word_tokenize(intermediate)) > 100:
            intermediate = self._extractive_summarize(intermediate, ratio=0.7)
        
        return intermediate
    
    def _simplify_with_transformer(self, text: str) -> str:
        """Use transformer model for simplification (requires internet)"""
        try:
            from transformers import pipeline
            
            # Load simplification pipeline
            simplifier = pipeline(
                "text2text-generation",
                model="microsoft/t5-base-finetuned-common_gen",
                max_length=512,
                device=-1  # CPU
            )
            
            # Prepare prompt
            prompt = f"simplify: {text[:500]}"  # Limit length
            
            # Generate simplification
            result = simplifier(prompt, max_length=512, do_sample=False)
            
            if result and len(result) > 0:
                return result[0]['generated_text']
            
        except ImportError:
            print("Transformers library not available. Using rule-based simplification.")
        except Exception as e:
            print(f"Transformer simplification failed: {e}")
        
        return text
    
    def _break_long_sentence(self, sentence: str) -> str:
        """Break long sentence into shorter ones"""
        words = word_tokenize(sentence)
        if len(words) <= 15:
            return sentence
        
        # Try to break at conjunctions
        conjunctions = {'and', 'but', 'or', 'so', 'because', 'although', 'while'}
        
        for i in range(len(words) - 1, 0, -1):
            if words[i].lower() in conjunctions and i > len(words) // 2:
                first_part = ' '.join(words[:i+1])
                second_part = ' '.join(words[i+1:])
                return f"{first_part}. {second_part.capitalize()}"
        
        # If no conjunction found, break in the middle
        mid = len(words) // 2
        first_part = ' '.join(words[:mid])
        second_part = ' '.join(words[mid:])
        return f"{first_part}. {second_part.capitalize()}"
    
    def _remove_unnecessary_clauses(self, sentence: str) -> str:
        """Remove unnecessary relative clauses"""
        # Simple pattern matching for common clause patterns
        patterns = [
            r', which is .*?,',
            r', that is .*?,',
            r', who is .*?,',
            r', whom .*?,',
            r', whose .*?,',
        ]
        
        for pattern in patterns:
            sentence = re.sub(pattern, ',', sentence)
        
        return sentence.strip()
    
    def _convert_to_active_voice(self, sentence: str) -> str:
        """Convert passive voice to active voice where possible"""
        # Simple passive voice patterns
        passive_patterns = [
            (r'(\w+) is (\w+)ed by (\w+)', r'\3 \2s \1'),
            (r'(\w+) are (\w+)ed by (\w+)', r'\3 \2 \1'),
            (r'(\w+) was (\w+)ed by (\w+)', r'\3 \2ed \1'),
            (r'(\w+) were (\w+)ed by (\w+)', r'\3 \2ed \1'),
            (r'(\w+) has been (\w+)ed by (\w+)', r'\3 has \2ed \1'),
            (r'(\w+) have been (\w+)ed by (\w+)', r'\3 have \2ed \1'),
        ]
        
        for pattern, replacement in passive_patterns:
            sentence = re.sub(pattern, replacement, sentence, flags=re.IGNORECASE)
        
        return sentence
    
    def _simplify_verb_phrases(self, sentence: str) -> str:
        """Simplify complex verb phrases"""
        replacements = {
            'is able to': 'can',
            'are able to': 'can',
            'was able to': 'could',
            'were able to': 'could',
            'has the ability to': 'can',
            'have the ability to': 'can',
            'make use of': 'use',
            'take into consideration': 'consider',
            'give rise to': 'cause',
            'put forward': 'suggest',
            'carry out': 'do',
        }
        
        for complex_phrase, simple_phrase in replacements.items():
            sentence = re.sub(
                f'\\b{complex_phrase}\\b',
                simple_phrase,
                sentence,
                flags=re.IGNORECASE
            )
        
        return sentence
    
    def _extractive_summarize(self, text: str, ratio: float = 0.5) -> str:
        """Simple extractive summarization"""
        sentences = sent_tokenize(text)
        
        if len(sentences) <= 3:
            return text
        
        # Calculate sentence scores (simple word frequency)
        word_freq = {}
        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            for word in words:
                if word.isalpha() and word not in self.stopwords:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            score = 0
            for word in words:
                if word in word_freq:
                    score += word_freq[word]
            sentence_scores[i] = score / len(words) if words else 0
        
        # Select top sentences
        num_sentences = max(1, int(len(sentences) * ratio))
        top_indices = heapq.nlargest(
            num_sentences,
            sentence_scores,
            key=sentence_scores.get
        )
        top_indices.sort()
        
        # Return selected sentences
        return ' '.join(sentences[i] for i in top_indices)
    
    def _postprocess_text(self, text: str) -> str:
        """Post-process simplified text"""
        # Ensure proper capitalization
        sentences = sent_tokenize(text)
        sentences = [s.strip() for s in sentences]
        sentences = [s[0].upper() + s[1:] if s else s for s in sentences]
        
        # Join with proper spacing
        result = ' '.join(sentences)
        
        # Fix any double punctuation
        result = re.sub(r'([.,!?;:])\s*\1+', r'\1', result)
        
        return result
    
    def calculate_complexity_score(self, text: str) -> float:
        """
        Calculate text complexity score (0-1, where 1 is most complex)
        
        Args:
            text: Input text
            
        Returns:
            Complexity score
        """
        if not text:
            return 0.0
        
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        
        if not words or not sentences:
            return 0.0
        
        # Calculate metrics
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(w) for w in words) / len(words)
        
        # Count complex words (words with 3+ syllables or in complex word list)
        complex_words = 0
        for word in words:
            if len(word) > 6 or word.lower() in self.synonym_dict:
                complex_words += 1
        
        complexity_ratio = complex_words / len(words) if words else 0
        
        # Normalize scores
        score = (
            min(avg_sentence_length / 20, 1.0) * 0.4 +
            min(avg_word_length / 8, 1.0) * 0.3 +
            complexity_ratio * 0.3
        )
        
        return min(score, 1.0)