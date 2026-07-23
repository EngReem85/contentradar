"""
⚠️ COMMERCIAL FEATURE
This file is part of the Skills Module (Premium Feature)
Licensing: See LICENSE.COMMERCIAL
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.utils.config import Config
import logging

logger = logging.getLogger(__name__)

class SkillExtractor:
    """Extract skills from content (Premium Feature)"""
    
    def __init__(self):
        self.skills_db = self._load_skills_db()
        self.skill_keywords = self._build_keyword_index()
        logger.info(f"Loaded {len(self.skills_db)} skills from database")
    
    def _load_skills_db(self) -> Dict:
        """Load skills database"""
        skills_dir = Config.SKILLS_DIR
        skills_db = {}
        
        if not skills_dir.exists():
            logger.warning(f"Skills directory not found: {skills_dir}")
            return skills_db
        
        for json_file in skills_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    skill_data = json.load(f)
                    skill_id = json_file.stem
                    skills_db[skill_id] = skill_data
                    logger.debug(f"Loaded skill: {skill_id}")
            except Exception as e:
                logger.error(f"Error loading {json_file}: {e}")
        
        return skills_db
    
    def _build_keyword_index(self) -> Dict:
        """Build keyword index"""
        keyword_index = {}
        
        for skill_id, skill_data in self.skills_db.items():
            # Add skill name
            keywords = [skill_data.get('skill_name', '').lower()]
            
            # Add sub-skills
            keywords.extend([s.lower() for s in skill_data.get('sub_skills', [])])
            
            # Add content examples
            for example in skill_data.get('content_examples', []):
                keywords.extend(example.get('skill_demo', '').lower().split())
            
            # Index keywords
            for keyword in keywords:
                if keyword and keyword not in keyword_index:
                    keyword_index[keyword] = []
                if keyword:
                    keyword_index[keyword].append(skill_id)
        
        return keyword_index
    
    def extract_skills_from_text(self, text: str) -> List[Dict]:
        """Extract skills from text"""
        if not text or not self.skills_db:
            return []
        
        text_lower = text.lower()
        found_skills = {}
        
        for keyword, skill_ids in self.skill_keywords.items():
            if keyword in text_lower:
                for skill_id in skill_ids:
                    if skill_id not in found_skills:
                        found_skills[skill_id] = {
                            'skill_id': skill_id,
                            'skill_data': self.skills_db.get(skill_id, {}),
                            'matches': set()
                        }
                    found_skills[skill_id]['matches'].add(keyword)
        
        # Prepare results
        results = []
        for skill_id, data in found_skills.items():
            if data['skill_data']:
                results.append({
                    'skill_id': skill_id,
                    'skill_name': data['skill_data'].get('skill_name', ''),
                    'category': data['skill_data'].get('category', ''),
                    'confidence': len(data['matches']) / max(1, len(self.skill_keywords)),
                    'matches': list(data['matches']),
                    'related_content': data['skill_data'].get('content_examples', [])
                })
        
        return sorted(results, key=lambda x: x['confidence'], reverse=True)
    
    def get_skill_details(self, skill_id: str) -> Optional[Dict]:
        """Get details for a specific skill"""
        return self.skills_db.get(skill_id)
    
    def get_all_skills(self) -> List[Dict]:
        """Get all skills"""
        return list(self.skills_db.values())