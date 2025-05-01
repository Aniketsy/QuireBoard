from openai import OpenAI
import json

class Generator:
    def __init__(self):
        self.client = OpenAI()  # Make sure to set OPENAI_API_KEY in environment variables
        
    def generate_resume(self, job_description: str, user_data: dict) -> str:
        # Generate an optimized resume using AI
        prompt = self._create_prompt(job_description, user_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional resume writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            enhanced_content = response.choices[0].message.content
            user_data['experience'] = enhanced_content
            return self.format_resume(user_data)
            
        except Exception as e:
            print(f"Error generating resume: {str(e)}")
            return self.format_resume(user_data)  # Fallback to basic format

    def format_resume(self, user_data: dict) -> str:
        # Enhanced formatting with professional layout
        return f"""
Professional Resume

{user_data.get('name', '')}
{user_data.get('contact', '')}
{'=' * 50}

PROFESSIONAL SUMMARY
{user_data.get('summary', 'Experienced professional with a track record of success.')}

EDUCATION
{user_data.get('education', '')}

PROFESSIONAL EXPERIENCE
{user_data.get('experience', '')}

SKILLS
{self.extract_relevant_skills(user_data.get('skills', []))}

ACHIEVEMENTS
{user_data.get('achievements', '')}
"""

    def extract_relevant_skills(self, skills: list) -> str:
        # Group skills by category
        skill_categories = {
            'Technical': [],
            'Soft': [],
            'Tools': []
        }
        
        for skill in skills:
            # Add logic to categorize skills
            if any(tech in skill.lower() for tech in ['python', 'java', 'sql', 'html']):
                skill_categories['Technical'].append(skill)
            elif any(tool in skill.lower() for tool in ['git', 'jira', 'office']):
                skill_categories['Tools'].append(skill)
            else:
                skill_categories['Soft'].append(skill)
                
        # Format skills by category
        formatted_skills = []
        for category, category_skills in skill_categories.items():
            if category_skills:
                formatted_skills.append(f"{category}: {', '.join(category_skills)}")
                
        return '\n'.join(formatted_skills)

    def _create_prompt(self, job_description: str, user_data: dict) -> str:
        return f"""
Please enhance the following professional experience to better match this job description:

Job Description:
{job_description}

Current Experience:
{user_data.get('experience', '')}

Please rewrite the experience section to:
1. Highlight relevant skills and achievements
2. Use strong action verbs
3. Include quantifiable results
4. Match keywords from the job description
5. Maintain professional tone
"""