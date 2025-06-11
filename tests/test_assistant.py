import unittest
from backend.utils.screen_recognizer import ScreenRecognizer
from backend.utils.problem_solver import ProblemSolver, ProblemType
from backend.utils.essay_writer import EssayWriter

class TestLocalAIAssistant(unittest.TestCase):
    def setUp(self):
        self.screen_recognizer = ScreenRecognizer()
        self.problem_solver = ProblemSolver()
        self.essay_writer = EssayWriter()
    
    def test_screen_analysis(self):
        """Test screen content analysis"""
        # Test with a small region
        region = (0, 0, 100, 100)
        analysis = self.screen_recognizer.analyze_screen_content(region)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('text_content', analysis)
        self.assertIn('word_count', analysis)
    
    def test_problem_solving(self):
        """Test math and physics problem solving"""
        # Test math problem
        math_problem = "Solve for x: 2x + 5 = 13"
        problem = self.problem_solver.parse_problem(math_problem)
        solution = self.problem_solver.solve_problem(problem)
        
        self.assertEqual(problem.type, ProblemType.MATH)
        self.assertIn('solution', solution)
        self.assertIn('steps', solution)
        
        # Test physics problem
        physics_problem = "A car travels 100 meters in 10 seconds. What is its velocity?"
        problem = self.problem_solver.parse_problem(physics_problem)
        solution = self.problem_solver.solve_problem(problem)
        
        self.assertEqual(problem.type, ProblemType.PHYSICS)
        self.assertIn('solution', solution)
        self.assertIn('physics_analysis', solution)
    
    def test_essay_writing(self):
        """Test essay generation"""
        # Test different essay types
        essay_types = ['analytical', 'persuasive', 'descriptive', 'narrative']
        for essay_type in essay_types:
            essay = self.essay_writer.generate_essay(
                topic="The Impact of Technology",
                essay_type=essay_type,
                tone="formal",
                length="medium"
            )
            
            self.assertIn('content', essay)
            self.assertIn('outline', essay)
            self.assertIn('metadata', essay)
            self.assertEqual(essay['metadata']['type'], essay_type)
    
    def test_text_search(self):
        """Test text search functionality"""
        search_text = "test"
        matches = self.screen_recognizer.find_text_on_screen(search_text)
        
        self.assertIsInstance(matches, list)
        for match in matches:
            self.assertIn('text', match)
            self.assertIn('start', match)
            self.assertIn('end', match)
    
    def test_equation_detection(self):
        """Test mathematical equation detection"""
        equations = self.screen_recognizer.detect_math_equations()
        
        self.assertIsInstance(equations, list)
        for equation in equations:
            self.assertIn('equation', equation)
            self.assertIn('type', equation)

if __name__ == '__main__':
    unittest.main() 