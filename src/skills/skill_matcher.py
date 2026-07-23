"""
⚠️ COMMERCIAL FEATURE
This file is part of the Skills Module (Premium Feature)
Licensing: See LICENSE.COMMERCIAL
"""

from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.skills.skill_extractor import SkillExtractor
import logging

logger = logging.getLogger(__name__)

class SkillMatcher:
    """Match content with skills (Premium Feature)"""
    
    def __init__(self, skill_extractor: SkillExtractor, embedder_model):
        self.skill_extractor = skill_extractor
        self.embedder = embedder_model
        self.skill_embeddings = self._embed_skills()
    
    def _embed_skills(self) -> Dict:
        """Generate embeddings for skills"""
        skill_embeddings = {}
        
        for skill_id, skill_data in self.skill_extractor.skills_db.items():
            # Create descriptive text for skill
            skill_text = f"""
                {skill_data.get('skill_name', '')}
                {' '.join(skill_data.get('sub_skills', []))}
                {' '.join([ex.get('skill_demo', '') for ex in skill_data.get('content_examples', [])])}
            """
            skill_embeddings[skill_id] = self.embedder.encode(skill_text)
        
        return skill_embeddings
    
    def match_content_to_skills(self, content: Dict) -> List[Dict]:
        """Match content with skills"""
        
        # Extract skills from text
        text = f"{content.get('title', '')} {content.get('description', '')}"
        extracted_skills = self.skill_extractor.extract_skills_from_text(text)
        
        # If skills found, return them
        if extracted_skills:
            return extracted_skills
        
        # If no skills found, use embeddings
        content_emb = self.embedder.encode(text)
        
        # Calculate similarity with all skills
        similarities = {}
        for skill_id, skill_emb in self.skill_embeddings.items():
            sim = cosine_similarity(
                content_emb.reshape(1, -1),
                skill_emb.reshape(1, -1)
            )[0][0]
            similarities[skill_id] = sim
        
        # Sort by similarity
        sorted_skills = sorted(
            similarities.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        results = []
        for skill_id, score in sorted_skills:
            if score > 0.3:  # Similarity threshold
                skill_data = self.skill_extractor.get_skill_details(skill_id)
                if skill_data:
                    results.append({
                        'skill_id': skill_id,
                        'skill_name': skill_data.get('skill_name', ''),
                        'category': skill_data.get('category', ''),
                        'confidence': float(score),
                        'matches': [],
                        'related_content': skill_data.get('content_examples', [])
                    })
        
        return results