import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
class CaptionEnhancer:
    def __init__(self):
        pass

    def enhance_caption(self, base_caption, classification_labels):
        try:
            # Support both dict and string caption input
            if isinstance(base_caption, dict):
                caption = base_caption.get('caption', '')
            else:
                caption = base_caption

            labels = [item['label'] for item in classification_labels if item.get('confidence', 1.0) > 0.1]

            # Remove common prefixes
            caption = re.sub(r'^(a photo of|an image of|a picture of)\s*', '', caption, flags=re.IGNORECASE)

            # Capitalize first letter
            if caption:
                caption = caption[0].upper() + caption[1:]

            # Add context if labels are relevant
            relevant_labels = self._filter_relevant_labels(labels, caption)

            if relevant_labels:
                top_label = relevant_labels[0].replace('_', ' ')
                if top_label.lower() not in caption.lower():
                    caption = f"{caption.rstrip('.')}. This appears to be related to {top_label}."

            caption = self._clean_caption(caption)

            return {
                'original_caption': base_caption if isinstance(base_caption, str) else base_caption.get('caption', ''),
                'enhanced_caption': caption,
                'used_labels': relevant_labels[:3]
            }

        except Exception as e:
            return {'error': f'Caption enhancement failed: {str(e)}'}

    def _filter_relevant_labels(self, labels, caption):
        generic_labels = ['object', 'item', 'thing', 'stuff', 'other']
        filtered_labels = [label for label in labels if label.lower() not in generic_labels]

        caption_words = caption.lower().split()
        relevant_labels = []

        for label in filtered_labels:
            label_words = label.lower().replace('_', ' ').split()
            if not any(word in caption_words for word in label_words):
                relevant_labels.append(label)

        return relevant_labels[:5]

    def _clean_caption(self, caption):
        caption = re.sub(r'\s+', ' ', caption)
        if caption and not caption.endswith(('.', '!', '?')):
            caption += '.'
        caption = re.sub(r'\.{2,}', '.', caption)
        return caption.strip()


if __name__ == "__main__":
    enhancer = CaptionEnhancer()
    test_caption = "a young boy in a yellow shirt and blue jeans"
    test_labels = [
        {"label": "sweatshirt", "confidence": 0.9},
        {"label": "sunglass", "confidence": 0.8},
        {"label": "maraca", "confidence": 0.7},
        {"label": "jersey, T-shirt, tee shirt", "confidence": 0.6},
        {"label": "sunglasses, dark glasses, shades", "confidence": 0.5}
    ]
    result = enhancer.enhance_caption(test_caption, test_labels)
    print("=== ENHANCER TEST OUTPUT ===")
    print("Original Caption:", result['original_caption'])
    print("Enhanced Caption:", result['enhanced_caption'])
    print("Used Labels:", result['used_labels'])
    print("============================") 