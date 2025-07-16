# vision.py - Image Classification using Google ViT
import torch
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import requests
from io import BytesIO

class ImageClassifier:
    def __init__(self):
        self.processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
        self.model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')
    
    def classify_image(self, image_path_or_url, top_k=5):
        """
        Classify image and return top labels with confidence scores
        """
        try:
            # Load image
            if image_path_or_url.startswith(('http://', 'https://')):
                response = requests.get(image_path_or_url)
                image = Image.open(BytesIO(response.content))
            else:
                image = Image.open(image_path_or_url)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Process image
            inputs = self.processor(images=image, return_tensors="pt")
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits[0], dim=-1)
            
            # Get top k predictions
            top_predictions = predictions.topk(top_k)
            
            results = []
            for i in range(top_k):
                label_idx = top_predictions.indices[i].item()
                confidence = top_predictions.values[i].item()
                label = self.model.config.id2label[label_idx]
                results.append({
                    'label': label,
                    'confidence': confidence
                })
            
            return results
            
        except Exception as e:
            return {'error': f'Classification failed: {str(e)}'} 