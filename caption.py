# caption.py - Image to Text using Salesforce BLIP
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests
from io import BytesIO

class ImageCaptioner:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    def generate_caption(self, image_path_or_url, max_length=50):
        """
        Generate basic caption for image
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
            inputs = self.processor(image, return_tensors="pt")
            
            # Generate caption
            out = self.model.generate(**inputs, max_length=max_length, num_beams=5)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            
            return {'caption': caption}
            
        except Exception as e:
            return {'error': f'Caption generation failed: {str(e)}'}
    
    def generate_conditional_caption(self, image_path_or_url, prompt="a photo of", max_length=50):
        """
        Generate caption with conditional prompt
        """
        try:
            # Load image
            if image_path_or_url.startswith(('http://', 'https://')):
                response = requests.get(image_path_or_url)
                image = Image.open(BytesIO(response.content))
            else:
                image = Image.open(image_path_or_url)
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Process with prompt
            inputs = self.processor(image, prompt, return_tensors="pt")
            
            # Generate caption
            out = self.model.generate(**inputs, max_length=max_length, num_beams=5)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            
            return {'caption': caption}
            
        except Exception as e:
            return {'error': f'Conditional caption generation failed: {str(e)}'} 