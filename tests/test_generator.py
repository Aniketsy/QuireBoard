import unittest
from src.ai.generator import Generator

class TestGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = Generator()

    def test_generate_resume(self):
        resume_data = {
            'name': 'John Doe',
            'contact': 'john.doe@example.com',
            'education': 'Bachelor of Science in Computer Science',
            'experience': '3 years of experience in software development',
            'skills': ['Python', 'JavaScript', 'Machine Learning']
        }
        job_description = "Looking for a software developer with experience in Python and JavaScript."
        expected_output = (
            "Name: John Doe\n"
            "Contact: john.doe@example.com\n"
            "Education: Bachelor of Science in Computer Science\n"
            "Experience: 3 years of experience in software development\n"
            "Skills: Python, JavaScript"
        )
        generated_resume = self.generator.generate_resume(resume_data, job_description)
        self.assertEqual(generated_resume.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()