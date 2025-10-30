import torch
from diffusers import StableDiffusionPipeline, StableDiffusionXLPipeline
import logging
import yaml
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self, config_path="config/config.yaml"):
        self.config = self.load_config(config_path)
        self.device = self.config['model']['device']
        self.dtype = torch.float16 if self.config['model']['dtype'] == "fp16" else torch.float32
        self.pipeline = self.load_model()
        
    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def load_model(self):
        model_name = self.config['model']['name']
        logger.info(f"Loading model: {model_name}")
        
        # Проверяем доступность GPU
        if self.device == "cuda" and not torch.cuda.is_available():
            logger.warning("CUDA not available, falling back to CPU")
            self.device = "cpu"
            self.dtype = torch.float32
        
        # Загружаем pipeline в зависимости от модели
        if "xl" in model_name.lower():
            pipeline = StableDiffusionXLPipeline.from_pretrained(
                model_name,
                torch_dtype=self.dtype,
                use_safetensors=True,
                variant="fp16" if self.dtype == torch.float16 else None
            )
        else:
            pipeline = StableDiffusionPipeline.from_pretrained(
                model_name,
                torch_dtype=self.dtype,
                use_safetensors=True,
                variant="fp16" if self.dtype == torch.float16 else None
            )
        
        pipeline = pipeline.to(self.device)
        
        # Оптимизация для GPU
        if self.device == "cuda":
            pipeline.enable_attention_slicing()
            pipeline.enable_memory_efficient_attention()
            
        logger.info("Model loaded successfully")
        return pipeline
    
    def generate(self, prompt, negative_prompt="", **kwargs):
        # Объединяем настройки из конфига и переданные параметры
        config = self.config['generation'].copy()
        config.update(kwargs)
        
        with torch.autocast(self.device) if self.device == "cuda" else torch.cpu_mode():
            result = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=config['num_inference_steps'],
                guidance_scale=config['guidance_scale'],
                width=config['width'],
                height=config['height']
            )
        
        return result.images[0]
    