"""
⚠️ COMMERCIAL FEATURE
This file is part of the Skills Module (Premium Feature)
Licensing: See LICENSE.COMMERCIAL
"""

from typing import List, Dict, Any
import numpy as np
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class SkillAnalyzer:
    """Analyze skill patterns and progress (Premium Feature)"""
    
    def __init__(self, skill_extractor, user_manager):
        self.skill_extractor = skill_extractor
        self.user_manager = user_manager
    
    def analyze_user_skills(self, user_id: str) -> Dict:
        """Analyze user's skill profile"""
        
        # Get user ratings
        ratings = self.user_manager.get_ratings(user_id)
        
        if not ratings:
            return {'error': 'No ratings found for user'}
        
        # Analyze skill distribution
        skill_counts = Counter()
        skill_ratings = {}
        
        for item_id, rating_data in ratings.items():
            # Get content skills
            content = self.user_manager.get_content(item_id)
            if content:
                skills = self.skill_extractor.extract_skills_from_text(
                    f"{content.get('title', '')} {content.get('description', '')}"
                )
                
                for skill in skills:
                    skill_id = skill['skill_id']
                    skill_counts[skill_id] += 1
                    
                    if skill_id not in skill_ratings:
                        skill_ratings[skill_id] = []
                    skill_ratings[skill_id].append(rating_data['rating'])
        
        # Calculate averages
        skill_profiles = []
        for skill_id, count in skill_counts.most_common(10):
            avg_rating = np.mean(skill_ratings.get(skill_id, [0]))
            skill_data = self.skill_extractor.get_skill_details(skill_id)
            
            skill_profiles.append({
                'skill_id': skill_id,
                'skill_name': skill_data.get('skill_name', skill_id) if skill_data else skill_id,
                'count': count,
                'avg_rating': avg_rating,
                'proficiency': min(100, (avg_rating / 5) * 100)  # Convert to percentage
            })
        
        return {
            'user_id': user_id,
            'total_skills': len(skill_counts),
            'skill_profiles': skill_profiles,
            'top_skill': skill_profiles[0]['skill_name'] if skill_profiles else None,
            'recommendations': self._generate_recommendations(skill_profiles)
        }
    
    def _generate_recommendations(self, skill_profiles: List[Dict]) -> List[str]:
        """Generate recommendations based on skill profile"""
        recommendations = []
        
        for skill in skill_profiles:
            if skill['proficiency'] < 50:
                recommendations.append(f"Practice {skill['skill_name']} more")
            elif skill['proficiency'] > 80:
                recommendations.append(f"Consider advanced {skill['skill_name']} content")
        
        if not recommendations:
            recommendations = ["Keep up the good work!"]
        
        return recommendations[:3]  # Top 3 recommendations