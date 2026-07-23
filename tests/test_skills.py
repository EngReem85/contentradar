import pytest
import json
from pathlib import Path
from src.skills.skill_extractor import SkillExtractor
from src.utils.config import Config

def test_skill_extractor_load():
    """Test skill extractor loads successfully"""
    extractor = SkillExtractor()
    assert extractor.skills_db is not None
    assert len(extractor.skills_db) >= 0

def test_extract_skills_from_text():
    """Test extracting skills from text"""
    extractor = SkillExtractor()
    
    # Create a test skill file
    skills_dir = Config.SKILLS_DIR
    skills_dir.mkdir(parents=True, exist_ok=True)
    
    test_skill = {
        "skill_name": "Test Skill",
        "sub_skills": ["sub1", "sub2"],
        "content_examples": [
            {"skill_demo": "Test demo content"}
        ]
    }
    
    test_file = skills_dir / "test_skill.json"
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_skill, f)
    
    # Reload extractor
    extractor = SkillExtractor()
    
    # Test extraction
    text = "This is a test about Test Skill and sub1"
    skills = extractor.extract_skills_from_text(text)
    
    assert len(skills) > 0
    
    # Cleanup
    test_file.unlink()

def test_skill_extractor_empty_text():
    """Test extractor with empty text"""
    extractor = SkillExtractor()
    result = extractor.extract_skills_from_text("")
    assert result == []

def test_skill_extractor_no_skills():
    """Test extractor with no skills database"""
    extractor = SkillExtractor()
    extractor.skills_db = {}
    extractor.skill_keywords = {}
    
    result = extractor.extract_skills_from_text("test")
    assert result == []