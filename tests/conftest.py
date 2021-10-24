import os
import sys

# Make server accessible for tests
api_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.insert(0, api_dir)
