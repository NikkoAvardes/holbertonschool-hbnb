#!/usr/bin/env python3
"""
Test runner for all HBNB application tests.
This file allows running all tests at once or specific test modules.
"""

import unittest
import sys
import os

# Import all test modules
from tests.test_user_endpoints import TestUserEndpoints
from tests.test_amenity_endpoints import TestAmenityEndpoints
from tests.test_place_endpoints import TestPlaceEndpoints
from tests.test_review_endpoints import TestReviewEndpoints

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_test_suite():
    """Create a test suite with all test cases."""
    test_suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestUserEndpoints,
        TestAmenityEndpoints,
        TestPlaceEndpoints,
        TestReviewEndpoints
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    return test_suite


def run_tests():
    """Run all tests and return the result."""
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = create_test_suite()
    result = runner.run(test_suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
