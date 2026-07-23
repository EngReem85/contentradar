"""
⚠️ COMMERCIAL FEATURE
This file is part of the Skills Module (Premium Feature)
Licensing: See LICENSE.COMMERCIAL
"""

from typing import List, Dict, Any, Optional
from src.skills.skill_matcher import SkillMatcher
import logging

logger = logging.getLogger(__name__)

class LearningPath:
    """Create personalized learning paths (Premium Feature)"""
    
    def __init__(self, skill_matcher: SkillMatcher, content_df):
        self.skill_matcher = skill_matcher
        self.content_df = content_df
    
    def create_path(self, skill_id: str, 
                    level: str = "beginner", 
                    duration_weeks: int = 4) -> Dict:
        """
        Create a learning plan for a specific skill
        
        Args:
            skill_id: Skill identifier
            level: beginner, intermediate, advanced
            duration_weeks: Duration in weeks
        """
        
        skill_data = self.skill_matcher.skill_extractor.get_skill_details(skill_id)
        if not skill_data:
            logger.warning(f"Skill not found: {skill_id}")
            return {}
        
        # Get content for skill
        content = self._get_content_for_skill(skill_id)
        
        # Split content by level
        if level == "beginner":
            content = content[:10]
        elif level == "intermediate":
            content = content[5:15]
        else:  # advanced
            content = content[10:20]
        
        # Build learning path
        weeks = []
        items_per_week = max(1, len(content) // duration_weeks)
        
        for week in range(duration_weeks):
            start_idx = week * items_per_week
            end_idx = min((week + 1) * items_per_week, len(content))
            
            week_content = content[start_idx:end_idx]
            
            if week_content:
                weeks.append({
                    'week': week + 1,
                    'title': f'Week {week + 1}: {skill_data["skill_name"]} - Part {week + 1}',
                    'description': f'Learn {skill_data["skill_name"]} through curated content',
                    'content': week_content,
                    'objectives': self._generate_week_objectives(skill_data, week)
                })
        
        return {
            'skill': skill_data,
            'level': level,
            'duration_weeks': duration_weeks,
            'total_items': len(content),
            'weeks': weeks,
            'resources': self._get_additional_resources(skill_data)
        }
    
    def _get_content_for_skill(self, skill_id: str) -> List[Dict]:
        """Get content items for a skill"""
        matched_content = []
        skill_data = self.skill_matcher.skill_extractor.get_skill_details(skill_id)
        
        if not skill_data:
            return []
        
        # Search in content dataframe
        keywords = [
            skill_data['skill_name'].lower(),
            *[s.lower() for s in skill_data.get('sub_skills', [])]
        ]
        
        for _, row in self.content_df.iterrows():
            text = f"{row['title']} {row['description']}".lower()
            
            # Check for keyword matches
            matches = sum(1 for kw in keywords if kw in text)
            
            if matches > 0:
                # Extract skills from content
                skills = self.skill_matcher.match_content_to_skills(row.to_dict())
                
                # Check if skill is present
                if any(s['skill_id'] == skill_id for s in skills):
                    matched_content.append({
                        'content': row.to_dict(),
                        'match_score': matches / len(keywords),
                        'skills': skills
                    })
        
        # Sort by match score
        matched_content.sort(key=lambda x: x['match_score'], reverse=True)
        return matched_content
    
    def _generate_week_objectives(self, skill_data: Dict, week: int) -> List[str]:
        """Generate weekly objectives"""
        sub_skills = skill_data.get('sub_skills', [])
        
        if week < len(sub_skills):
            return [
                f"Understand {sub_skills[week]}",
                f"Watch content about {sub_skills[week]}",
                f"Apply {sub_skills[week]} in practice"
            ]
        else:
            return [
                f"Review {skill_data['skill_name']}",
                "Assess progress",
                "Identify strengths and weaknesses"
            ]
    
    def _get_additional_resources(self, skill_data: Dict) -> List[Dict]:
        """Get additional learning resources"""
        return [
            {
                'type': 'book',
                'title': f'Book: {skill_data["skill_name"]} Fundamentals',
                'recommendation': 'Recommended reading for deeper understanding'
            },
            {
                'type': 'course',
                'title': f'Course: Master {skill_data["skill_name"]}',
                'recommendation': 'Structured course with practical exercises'
            }
        ]