import argparse
import os
import unittest


def discover_and_run_tests(test_id=None):
    """Discover and run test cases, optionally filtering by test ID."""
    test_directory = "src"

    # Discover all test cases
    test_loader = unittest.TestLoader()
    all_tests = test_loader.discover(test_directory, pattern="*.py")

    if test_id:
        # Filter tests by ID, using the class name pattern
        filtered_suite = unittest.TestSuite()
        for test_suite in all_tests:
            if f"Test{test_id}Solution" in str(test_suite):
                filtered_suite.addTest(test_suite)
        test_suite = filtered_suite
    else:
        # Use all tests if no filter is provided
        test_suite = all_tests

    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    # Exit with appropriate status code
    if result.wasSuccessful():
        print("\nAll tests passed!")
        exit(0)
    else:
        print("\nSome tests failed.")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run unittests.")
    parser.add_argument(
        "--id",
        type=str,
        help="Run tests for a specific problem ID (e.g., 123 for Test123Solution).",
    )
    args = parser.parse_args()

    discover_and_run_tests(test_id=args.id)
