"""
Test File 
"""

from TestCase import TestCase
from GenerateFeature import GenerateFeature

generate_feature =GenerateFeature("generic_api_testing/generator/example.yml")
generate_feature.create_feature("/example")
