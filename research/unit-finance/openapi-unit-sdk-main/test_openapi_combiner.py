#!/usr/bin/env python3
"""
Test suite for OpenAPI Schema Combiner
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from openapi_combiner import OpenAPICombiner


class TestOpenAPICombiner(unittest.TestCase):
    """Test cases for the OpenAPI combiner functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
    def tearDown(self):
        """Clean up after each test."""
        # Remove temporary directory and files
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_test_file(self, filename: str, content: dict) -> Path:
        """Helper to create a test JSON file."""
        file_path = self.test_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(content, f, indent=2)
        return file_path
    
    def test_simple_ref_resolution(self):
        """Test basic $ref resolution with a simple reference."""
        # Create referenced schema file
        schema_content = {
            "get": {
                "summary": "Get application",
                "operationId": "getApplication",
                "responses": {
                    "200": {
                        "description": "Success"
                    }
                }
            }
        }
        self.create_test_file("schemas/application.json", schema_content)
        
        # Create main OpenAPI file with reference
        openapi_content = {
            "openapi": "3.0.2",
            "paths": {
                "/applications/{id}": {
                    "$ref": "./schemas/application.json"
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        
        # Combine and verify
        combiner = OpenAPICombiner(self.test_dir)
        result = combiner.combine(str(main_file))
        
        # Verify the ref was resolved
        self.assertNotIn("$ref", result["paths"]["/applications/{id}"])
        self.assertEqual(
            result["paths"]["/applications/{id}"]["get"]["summary"],
            "Get application"
        )
    
    def test_json_pointer_resolution(self):
        """Test resolution of $ref with JSON pointer."""
        # Create schema file with multiple definitions
        schema_content = {
            "application": {
                "get": {
                    "summary": "Get application",
                    "operationId": "getApplication"
                }
            },
            "applications": {
                "get": {
                    "summary": "List applications",
                    "operationId": "listApplications"
                },
                "post": {
                    "summary": "Create application",
                    "operationId": "createApplication"
                }
            }
        }
        self.create_test_file("schemas/applicationPaths.json", schema_content)
        
        # Create OpenAPI file with JSON pointer refs
        openapi_content = {
            "openapi": "3.0.2",
            "paths": {
                "/applications/{id}": {
                    "$ref": "./schemas/applicationPaths.json#/application"
                },
                "/applications": {
                    "$ref": "./schemas/applicationPaths.json#/applications"
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        
        # Combine and verify
        combiner = OpenAPICombiner(self.test_dir)
        result = combiner.combine(str(main_file))
        
        # Verify correct sections were extracted
        self.assertEqual(
            result["paths"]["/applications/{id}"]["get"]["operationId"],
            "getApplication"
        )
        self.assertEqual(
            result["paths"]["/applications"]["get"]["operationId"],
            "listApplications"
        )
        self.assertEqual(
            result["paths"]["/applications"]["post"]["operationId"],
            "createApplication"
        )
    
    def test_nested_refs(self):
        """Test resolution of nested $ref references."""
        # Create deepest schema
        response_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "status": {"type": "string"}
            }
        }
        self.create_test_file("schemas/responses.json", {
            "ApplicationResponse": response_schema
        })
        
        # Create middle schema that references the deep schema
        path_schema = {
            "get": {
                "summary": "Get application",
                "responses": {
                    "200": {
                        "description": "Success",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "./responses.json#/ApplicationResponse"
                                }
                            }
                        }
                    }
                }
            }
        }
        self.create_test_file("schemas/paths.json", {
            "application": path_schema
        })
        
        # Create main file
        openapi_content = {
            "openapi": "3.0.2",
            "paths": {
                "/applications/{id}": {
                    "$ref": "./schemas/paths.json#/application"
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        
        # Combine and verify
        combiner = OpenAPICombiner(self.test_dir)
        result = combiner.combine(str(main_file))
        
        # Verify nested refs were resolved
        schema = result["paths"]["/applications/{id}"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
        self.assertNotIn("$ref", schema)
        self.assertEqual(schema["type"], "object")
        self.assertIn("id", schema["properties"])
        self.assertIn("status", schema["properties"])
    
    def test_multiple_refs_same_file(self):
        """Test multiple references to the same file are handled correctly."""
        schema_content = {
            "getUser": {
                "get": {
                    "summary": "Get user",
                    "operationId": "getUser"
                }
            },
            "updateUser": {
                "patch": {
                    "summary": "Update user",
                    "operationId": "updateUser"
                }
            }
        }
        self.create_test_file("schemas/users.json", schema_content)
        
        openapi_content = {
            "openapi": "3.0.2",
            "paths": {
                "/users/{id}": {
                    "$ref": "./schemas/users.json#/getUser"
                },
                "/users/{id}/update": {
                    "$ref": "./schemas/users.json#/updateUser"
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        
        combiner = OpenAPICombiner(self.test_dir)
        result = combiner.combine(str(main_file))
        
        # Both refs should be resolved
        self.assertEqual(
            result["paths"]["/users/{id}"]["get"]["operationId"],
            "getUser"
        )
        self.assertEqual(
            result["paths"]["/users/{id}/update"]["patch"]["operationId"],
            "updateUser"
        )
    
    def test_preserves_non_ref_content(self):
        """Test that content without $ref is preserved as-is."""
        openapi_content = {
            "openapi": "3.0.2",
            "info": {
                "title": "Test API",
                "version": "1.0.0",
                "description": "A test API"
            },
            "servers": [
                {"url": "https://api.example.com"}
            ],
            "paths": {
                "/health": {
                    "get": {
                        "summary": "Health check",
                        "responses": {
                            "200": {"description": "OK"}
                        }
                    }
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        
        combiner = OpenAPICombiner(self.test_dir)
        result = combiner.combine(str(main_file))
        
        # Verify all content is preserved
        self.assertEqual(result["openapi"], "3.0.2")
        self.assertEqual(result["info"]["title"], "Test API")
        self.assertEqual(result["info"]["version"], "1.0.0")
        self.assertEqual(result["servers"][0]["url"], "https://api.example.com")
        self.assertEqual(
            result["paths"]["/health"]["get"]["summary"],
            "Health check"
        )
    
    def test_handles_missing_file(self):
        """Test graceful handling of missing referenced files."""
        openapi_content = {
            "openapi": "3.0.2",
            "paths": {
                "/applications": {
                    "$ref": "./schemas/missing.json#/application"
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        
        combiner = OpenAPICombiner(self.test_dir)
        result = combiner.combine(str(main_file))
        
        # Should keep the original $ref when file is missing
        self.assertEqual(
            result["paths"]["/applications"]["$ref"],
            "./schemas/missing.json#/application"
        )
    
    def test_handles_invalid_pointer(self):
        """Test handling of invalid JSON pointers."""
        schema_content = {
            "application": {
                "get": {"summary": "Get application"}
            }
        }
        self.create_test_file("schemas/paths.json", schema_content)
        
        openapi_content = {
            "openapi": "3.0.2",
            "paths": {
                "/applications": {
                    "$ref": "./schemas/paths.json#/nonexistent"
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        
        combiner = OpenAPICombiner(self.test_dir)
        result = combiner.combine(str(main_file))
        
        # Should keep the original $ref when pointer is invalid
        self.assertEqual(
            result["paths"]["/applications"]["$ref"],
            "./schemas/paths.json#/nonexistent"
        )
    
    def test_complex_unit_api_structure(self):
        """Test with a structure similar to the Unit API."""
        # Create application paths schema
        app_paths = {
            "application": {
                "get": {
                    "summary": "Get Application",
                    "operationId": "getApplication",
                    "tags": ["applications"],
                    "parameters": [
                        {
                            "name": "applicationId",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response"
                        }
                    }
                }
            },
            "applications": {
                "get": {
                    "summary": "List Applications",
                    "operationId": "listApplications",
                    "tags": ["applications"]
                },
                "post": {
                    "summary": "Create Application",
                    "operationId": "createApplication",
                    "tags": ["applications"]
                }
            }
        }
        self.create_test_file("schemas/application/applicationPaths.json", app_paths)
        
        # Create account paths schema
        account_paths = {
            "account": {
                "get": {
                    "summary": "Get Account",
                    "operationId": "getAccount",
                    "tags": ["accounts"]
                }
            },
            "accounts": {
                "get": {
                    "summary": "List Accounts",
                    "operationId": "listAccounts",
                    "tags": ["accounts"]
                }
            }
        }
        self.create_test_file("schemas/account/accountPaths.json", account_paths)
        
        # Create main OpenAPI file
        openapi_content = {
            "openapi": "3.0.2",
            "info": {
                "title": "Unit OpenAPI specifications",
                "version": "0.2.3"
            },
            "servers": [
                {"url": "https://api.s.unit.sh"}
            ],
            "paths": {
                "/applications/{applicationId}": {
                    "$ref": "./schemas/application/applicationPaths.json#/application"
                },
                "/applications": {
                    "$ref": "./schemas/application/applicationPaths.json#/applications"
                },
                "/accounts/{accountId}": {
                    "$ref": "./schemas/account/accountPaths.json#/account"
                },
                "/accounts": {
                    "$ref": "./schemas/account/accountPaths.json#/accounts"
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        
        # Combine and verify
        combiner = OpenAPICombiner(self.test_dir)
        result = combiner.combine(str(main_file))
        
        # Verify structure is preserved
        self.assertEqual(result["info"]["title"], "Unit OpenAPI specifications")
        self.assertEqual(len(result["paths"]), 4)
        
        # Verify application paths
        self.assertEqual(
            result["paths"]["/applications/{applicationId}"]["get"]["operationId"],
            "getApplication"
        )
        self.assertEqual(
            result["paths"]["/applications"]["get"]["operationId"],
            "listApplications"
        )
        self.assertEqual(
            result["paths"]["/applications"]["post"]["operationId"],
            "createApplication"
        )
        
        # Verify account paths
        self.assertEqual(
            result["paths"]["/accounts/{accountId}"]["get"]["operationId"],
            "getAccount"
        )
        self.assertEqual(
            result["paths"]["/accounts"]["get"]["operationId"],
            "listAccounts"
        )
        
        # Verify no $ref remain
        paths_str = json.dumps(result["paths"])
        self.assertNotIn("$ref", paths_str)
    
    def test_output_file_creation(self):
        """Test that output file is created correctly."""
        schema_content = {
            "application": {
                "get": {"summary": "Get application"}
            }
        }
        self.create_test_file("schemas/paths.json", schema_content)
        
        openapi_content = {
            "openapi": "3.0.2",
            "paths": {
                "/applications/{id}": {
                    "$ref": "./schemas/paths.json#/application"
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        output_file = self.test_path / "combined.json"
        
        combiner = OpenAPICombiner(self.test_dir)
        combiner.combine(str(main_file), str(output_file))
        
        # Verify output file exists and contains correct data
        self.assertTrue(output_file.exists())
        
        with open(output_file, 'r') as f:
            result = json.load(f)
        
        self.assertEqual(
            result["paths"]["/applications/{id}"]["get"]["summary"],
            "Get application"
        )


class TestRealWorldScenarios(unittest.TestCase):
    """Test real-world scenarios and edge cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def create_test_file(self, filename: str, content: dict) -> Path:
        """Helper to create a test JSON file."""
        file_path = self.test_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(content, f, indent=2)
        return file_path
    
    def test_all_refs_resolved(self):
        """Verify that no $ref strings remain in the final output."""
        # Create a complex nested structure
        definitions = {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"}
                }
            }
        }
        self.create_test_file("schemas/definitions.json", definitions)
        
        responses = {
            "UserResponse": {
                "description": "User response",
                "content": {
                    "application/json": {
                        "schema": {
                            "$ref": "./definitions.json#/User"
                        }
                    }
                }
            }
        }
        self.create_test_file("schemas/responses.json", responses)
        
        paths = {
            "getUser": {
                "get": {
                    "summary": "Get user",
                    "responses": {
                        "200": {
                            "$ref": "./responses.json#/UserResponse"
                        }
                    }
                }
            }
        }
        self.create_test_file("schemas/paths.json", paths)
        
        openapi_content = {
            "openapi": "3.0.2",
            "paths": {
                "/users/{id}": {
                    "$ref": "./schemas/paths.json#/getUser"
                }
            }
        }
        main_file = self.create_test_file("openapi.json", openapi_content)
        
        combiner = OpenAPICombiner(self.test_dir)
        result = combiner.combine(str(main_file))
        
        # Convert to string and verify no $ref remains
        result_str = json.dumps(result)
        self.assertNotIn('"$ref"', result_str)
        
        # Verify the nested structure was properly resolved
        user_schema = result["paths"]["/users/{id}"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
        self.assertEqual(user_schema["type"], "object")
        self.assertIn("id", user_schema["properties"])
        self.assertIn("name", user_schema["properties"])


def run_tests():
    """Run all tests and provide a summary."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestOpenAPICombiner))
    suite.addTests(loader.loadTestsFromTestCase(TestRealWorldScenarios))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())