from typing import Dict, Any, Optional, List, Union
import re
import sympy
from sympy import symbols, solve, Eq, Symbol
import numpy as np
from dataclasses import dataclass
from enum import Enum

class ProblemType(Enum):
    MATH = "math"
    PHYSICS = "physics"

@dataclass
class Problem:
    text: str
    type: ProblemType
    variables: Dict[str, Symbol]
    equations: List[Eq]
    known_values: Dict[str, float]
    unknown_variables: List[str]

class ProblemSolver:
    def __init__(self):
        self.math_patterns = {
            'equation': r'([\w\d\s+\-*/=()]+)',
            'inequality': r'([\w\d\s+\-*/=<>≤≥()]+)',
            'expression': r'([\w\d\s+\-*/()]+)'
        }
        
        self.physics_patterns = {
            'kinematics': r'(velocity|speed|acceleration|distance|time|displacement)',
            'dynamics': r'(force|mass|acceleration|weight|friction)',
            'energy': r'(energy|work|power|kinetic|potential)',
            'electricity': r'(current|voltage|resistance|power|circuit)'
        }
    
    def parse_problem(self, problem_text: str) -> Problem:
        """
        Parse a problem text into a structured Problem object.
        
        Args:
            problem_text: The text of the problem
            
        Returns:
            Problem object containing parsed information
        """
        # Determine problem type
        problem_type = self._determine_problem_type(problem_text)
        
        # Extract variables
        variables = self._extract_variables(problem_text)
        
        # Extract equations
        equations = self._extract_equations(problem_text)
        
        # Extract known values
        known_values = self._extract_known_values(problem_text)
        
        # Determine unknown variables
        unknown_variables = self._determine_unknowns(variables, known_values)
        
        return Problem(
            text=problem_text,
            type=problem_type,
            variables=variables,
            equations=equations,
            known_values=known_values,
            unknown_variables=unknown_variables
        )
    
    def solve_problem(self, problem: Problem) -> Dict[str, Any]:
        """
        Solve a parsed problem.
        
        Args:
            problem: The Problem object to solve
            
        Returns:
            Dictionary containing solution and steps
        """
        try:
            if problem.type == ProblemType.MATH:
                return self._solve_math_problem(problem)
            else:
                return self._solve_physics_problem(problem)
                
        except Exception as e:
            raise Exception(f"Problem solving failed: {str(e)}")
    
    def _determine_problem_type(self, text: str) -> ProblemType:
        """
        Determine if the problem is math or physics based.
        """
        # Check for physics keywords
        for pattern in self.physics_patterns.values():
            if re.search(pattern, text, re.IGNORECASE):
                return ProblemType.PHYSICS
        
        return ProblemType.MATH
    
    def _extract_variables(self, text: str) -> Dict[str, Symbol]:
        """
        Extract variables from problem text.
        """
        variables = {}
        
        # Find all potential variables (words that could be variables)
        potential_vars = re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', text)
        
        # Filter out common words and create symbols
        for var in potential_vars:
            if var.lower() not in ['the', 'and', 'or', 'in', 'on', 'at', 'to', 'for']:
                variables[var] = symbols(var)
        
        return variables
    
    def _extract_equations(self, text: str) -> List[Eq]:
        """
        Extract equations from problem text.
        """
        equations = []
        
        # Find all potential equations
        for pattern in self.math_patterns.values():
            matches = re.finditer(pattern, text)
            for match in matches:
                try:
                    # Try to parse as equation
                    expr = match.group(1).strip()
                    if '=' in expr:
                        left, right = expr.split('=')
                        equations.append(Eq(sympy.sympify(left), sympy.sympify(right)))
                except:
                    continue
        
        return equations
    
    def _extract_known_values(self, text: str) -> Dict[str, float]:
        """
        Extract known values from problem text.
        """
        known_values = {}
        
        # Find number-variable pairs
        pairs = re.finditer(r'(\d+(?:\.\d+)?)\s*([a-zA-Z][a-zA-Z0-9]*)', text)
        for pair in pairs:
            value, var = pair.groups()
            known_values[var] = float(value)
        
        return known_values
    
    def _determine_unknowns(self, variables: Dict[str, Symbol], 
                          known_values: Dict[str, float]) -> List[str]:
        """
        Determine which variables are unknown.
        """
        return [var for var in variables.keys() if var not in known_values]
    
    def _solve_math_problem(self, problem: Problem) -> Dict[str, Any]:
        """
        Solve a math problem.
        """
        # Substitute known values into equations
        equations = []
        for eq in problem.equations:
            for var, value in problem.known_values.items():
                if var in problem.variables:
                    eq = eq.subs(problem.variables[var], value)
            equations.append(eq)
        
        # Solve system of equations
        solutions = solve(equations, [problem.variables[var] for var in problem.unknown_variables])
        
        # Format solution
        result = {
            'solution': {},
            'steps': []
        }
        
        if isinstance(solutions, list):
            for i, var in enumerate(problem.unknown_variables):
                result['solution'][var] = float(solutions[i])
                result['steps'].append(f"{var} = {solutions[i]}")
        
        return result
    
    def _solve_physics_problem(self, problem: Problem) -> Dict[str, Any]:
        """
        Solve a physics problem.
        """
        # First solve any mathematical equations
        math_solution = self._solve_math_problem(problem)
        
        # Add physics-specific analysis
        result = {
            'solution': math_solution['solution'],
            'steps': math_solution['steps'],
            'physics_analysis': self._analyze_physics_problem(problem)
        }
        
        return result
    
    def _analyze_physics_problem(self, problem: Problem) -> Dict[str, Any]:
        """
        Analyze a physics problem for additional insights.
        """
        analysis = {
            'problem_type': None,
            'principles': [],
            'units': {}
        }
        
        # Determine physics problem type
        for category, pattern in self.physics_patterns.items():
            if re.search(pattern, problem.text, re.IGNORECASE):
                analysis['problem_type'] = category
                break
        
        # Extract units
        unit_pattern = r'(\d+(?:\.\d+)?)\s*([a-zA-Z][a-zA-Z0-9]*)\s*(m|s|kg|N|J|W|V|A|Ω)'
        units = re.finditer(unit_pattern, problem.text)
        for unit in units:
            value, var, unit = unit.groups()
            analysis['units'][var] = unit
        
        return analysis 