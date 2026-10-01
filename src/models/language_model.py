import torch
import torch.nn as nn
from torch.nn import functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class EnterpriseLanguageModel:
    def __init__(
        self,
        model_name: str = "gpt2",
        device: str = "cpu"
    ):
        self.model_name = model_name
        self.device = device
        self.tokenizer = None
        self.model = None
        
        self._initialize_model()
    
    def _initialize_model(self):
        logger.info(f"Initializing model: {self.model_name}")
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map=self.device,
            trust_remote_code=True
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        logger.info("Model initialized successfully")
    
    def generate(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        num_return_sequences: int = 1
    ) -> List[str]:
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=num_return_sequences,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        responses = self.tokenizer.batch_decode(
            outputs,
            skip_special_tokens=True
        )
        
        return responses
    
    def encode(self, text: str) -> torch.Tensor:
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(
                **inputs,
                output_hidden_states=True
            )
        
        return outputs.hidden_states[-1][:, -1, :].squeeze()
    
    def save_checkpoint(self, path: str):
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        logger.info(f"Checkpoint saved to {path}")
