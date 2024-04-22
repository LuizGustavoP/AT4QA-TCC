"""
Test File 
"""

from TestCase import TestCase
from GenerateFeature import GenerateFeature

generate_feature =GenerateFeature("generic_api_testing/generator/1.0.2.yml")
generate_feature.createFeature("/business-accounts")
