# Define the Resume class
class Resume:
    def __init__(self, name, contact, education, experience, skills, summary, achievements):
        self.name = name
        self.contact = contact
        self.education = education
        self.experience = experience
        self.skills = skills
        self.summary = summary
        self.achievements = achievements

    def to_dict(self):
        return {
            "name": self.name,
            "contact": self.contact,
            "education": self.education,
            "experience": self.experience,
            "skills": self.skills,
            "summary": self.summary,
            "achievements": self.achievements,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            contact=data["contact"],
            education=data["education"],
            experience=data["experience"],
            skills=data["skills"],
            summary=data["summary"],
            achievements=data["achievements"],
        )

    def add_skill(self, skill):
        self.skills.append(skill)

    def update_experience(self, experience):
        self.experience = experience

    def __str__(self):
        return f"{self.name}\n{self.contact}\n{self.education}\n{self.experience}\nSkills: {', '.join(self.skills)}\n{self.summary}\nAchievements: {self.achievements}"

# Create a new resume
resume = Resume(
    name="John Doe",
    contact="john@email.com | (555) 555-5555",
    education="BS Computer Science, University ABC",
    experience="Senior Developer at XYZ Corp",
    skills=["Python", "JavaScript", "AWS"],
    summary="Experienced software developer with 5+ years in web development",
    achievements="Led development of enterprise-scale applications"
)

# Convert to dictionary
resume_dict = resume.to_dict()

# Create from dictionary
new_resume = Resume.from_dict(resume_dict)

# Add new skill
resume.add_skill("React")

# Update experience
resume.update_experience("Tech Lead at ABC Corp")

# Print formatted resume
print(str(resume))