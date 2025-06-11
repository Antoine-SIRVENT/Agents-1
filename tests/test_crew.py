import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from nltosql.crew import Nltosql
from crewai import Crew

def test_crew_creation():
    crew = Nltosql().crew()
    assert isinstance(crew, Crew)


