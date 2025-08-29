"""Unit tests for CLI commands"""

import unittest
import tempfile
import json
import os
from unittest.mock import patch, MagicMock, call
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cli.commands.base import BaseCommand
from cli.commands.login import LoginCommand
from cli.commands.select_db import SelectDBCommand
from cli.commands.select_issue import SelectIssueCommand
from cli.commands.configure import ConfigureCommand


class TestBaseCommand(unittest.TestCase):
    """Test BaseCommand class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'config.json')
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_config_empty(self):
        """Test loading config when file doesn't exist"""
        # Create a concrete subclass for testing
        class TestCommand(BaseCommand):
            def run(self, **kwargs):
                return 0
        
        cmd = TestCommand(self.config_path)
        self.assertEqual(cmd.config, {})
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        class TestCommand(BaseCommand):
            def run(self, **kwargs):
                return 0
        
        cmd = TestCommand(self.config_path)
        test_config = {'key': 'value', 'number': 42}
        cmd.save_config(test_config)
        
        # Create new instance and check if config is loaded
        cmd2 = TestCommand(self.config_path)
        self.assertEqual(cmd2.config, test_config)
    
    def test_session_management(self):
        """Test session get/set/clear operations"""
        class TestCommand(BaseCommand):
            def run(self, **kwargs):
                return 0
        
        cmd = TestCommand(self.config_path)
        
        # Initially no session
        self.assertIsNone(cmd.get_session())
        
        # Set session
        session = {'token': 'abc123', 'username': 'testuser'}
        cmd.set_session(session)
        self.assertEqual(cmd.get_session(), session)
        
        # Clear session
        cmd.clear_session()
        self.assertIsNone(cmd.get_session())


class TestLoginCommand(unittest.TestCase):
    """Test LoginCommand class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'config.json')
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_authenticate_success(self):
        """Test successful authentication"""
        cmd = LoginCommand(self.config_path)
        result = cmd.authenticate('testuser', 'testpass')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], 'testuser')
        self.assertIn('token', result)
        self.assertIn('expires_at', result)
    
    def test_authenticate_empty_credentials(self):
        """Test authentication with empty credentials"""
        cmd = LoginCommand(self.config_path)
        
        result = cmd.authenticate('', 'password')
        self.assertIsNone(result)
        
        result = cmd.authenticate('username', '')
        self.assertIsNone(result)
    
    def test_validate_session(self):
        """Test session validation"""
        cmd = LoginCommand(self.config_path)
        import time
        
        # Valid session
        valid_session = {
            'token': 'test_token',
            'expires_at': time.time() + 3600  # 1 hour from now
        }
        self.assertTrue(cmd.validate_session(valid_session))
        
        # Expired session
        expired_session = {
            'token': 'test_token',
            'expires_at': time.time() - 3600  # 1 hour ago
        }
        self.assertFalse(cmd.validate_session(expired_session))
        
        # Invalid session (no token)
        invalid_session = {'expires_at': time.time() + 3600}
        self.assertFalse(cmd.validate_session(invalid_session))
    
    @patch('cli.commands.login.getpass.getpass')
    @patch('builtins.input')
    def test_run_with_user_id(self, mock_input, mock_getpass):
        """Test run method with pre-provided user ID"""
        mock_getpass.return_value = 'testpass'
        
        cmd = LoginCommand(self.config_path)
        result = cmd.run(user_id='testuser')
        
        self.assertEqual(result, 0)
        session = cmd.get_session()
        self.assertIsNotNone(session)
        self.assertEqual(session['username'], 'testuser')


class TestSelectDBCommand(unittest.TestCase):
    """Test SelectDBCommand class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'config.json')
        
        # Create config with session
        config = {
            'session': {
                'token': 'test_token',
                'username': 'testuser'
            }
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_get_db_options(self):
        """Test getting database options for each level"""
        cmd = SelectDBCommand(self.config_path)
        
        # Level 1 options
        options1 = cmd.get_db_options(1)
        self.assertIsInstance(options1, list)
        self.assertTrue(len(options1) > 0)
        
        # Level 2 options
        options2 = cmd.get_db_options(2)
        self.assertIsInstance(options2, list)
        self.assertTrue(len(options2) > 0)
        
        # Level 3 options
        options3 = cmd.get_db_options(3)
        self.assertIsInstance(options3, list)
        self.assertTrue(len(options3) > 0)
    
    def test_search_options(self):
        """Test searching options"""
        cmd = SelectDBCommand(self.config_path)
        options = ["Production Database", "Development Database", "Test Database"]
        
        # Search for "prod"
        results = cmd.search_options(options, "prod")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "Production Database")
        
        # Search for "database"
        results = cmd.search_options(options, "database")
        self.assertEqual(len(results), 3)
        
        # Search for non-existent
        results = cmd.search_options(options, "xyz")
        self.assertEqual(len(results), 0)
    
    def test_get_selection(self):
        """Test getting current selection"""
        cmd = SelectDBCommand(self.config_path)
        
        # Initially empty
        self.assertEqual(cmd.get_selection(), {})
        
        # After setting selection
        cmd.selection = {'db1': 'A', 'db2': 'B', 'db3': 'C'}
        selection = cmd.get_selection()
        self.assertEqual(selection, {'db1': 'A', 'db2': 'B', 'db3': 'C'})
        
        # Ensure it's a copy
        selection['db1'] = 'X'
        self.assertEqual(cmd.selection['db1'], 'A')


class TestSelectIssueCommand(unittest.TestCase):
    """Test SelectIssueCommand class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'config.json')
        
        # Create config with session
        config = {
            'session': {
                'token': 'test_token',
                'username': 'testuser'
            }
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_fetch_issues(self):
        """Test fetching issues"""
        cmd = SelectIssueCommand(self.config_path)
        
        # Fetch without filter
        issues, total = cmd.fetch_issues(limit=5)
        self.assertIsInstance(issues, list)
        self.assertTrue(len(issues) <= 5)
        self.assertIsInstance(total, int)
        
        # Fetch with filter
        issues, total = cmd.fetch_issues(filter_text="PROJ-10", limit=10)
        self.assertIsInstance(issues, list)
        
        # Test pagination
        page1_issues, _ = cmd.fetch_issues(page=1, limit=5)
        page2_issues, _ = cmd.fetch_issues(page=2, limit=5)
        
        # Ensure different pages have different content (if enough items)
        if len(page1_issues) > 0 and len(page2_issues) > 0:
            self.assertNotEqual(page1_issues[0]['key'], page2_issues[0]['key'])
    
    def test_set_db_filter(self):
        """Test setting DB filter"""
        cmd = SelectIssueCommand(self.config_path)
        
        db_selection = {'db1': 'A', 'db2': 'B', 'db3': 'C'}
        cmd.set_db_filter(db_selection)
        self.assertEqual(cmd.db_filter, db_selection)


class TestConfigureCommand(unittest.TestCase):
    """Test ConfigureCommand class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'config.json')
        
        # Create config with session
        config = {
            'session': {
                'token': 'test_token',
                'username': 'testuser'
            }
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_get_available_repos(self):
        """Test getting available repositories"""
        cmd = ConfigureCommand(self.config_path)
        repos = cmd.get_available_repos()
        
        self.assertIsInstance(repos, list)
        self.assertTrue(len(repos) > 0)
        self.assertIn("main-repository", repos)
    
    def test_get_available_versions(self):
        """Test getting available versions"""
        cmd = ConfigureCommand(self.config_path)
        versions = cmd.get_available_versions()
        
        self.assertIsInstance(versions, list)
        self.assertTrue(len(versions) > 0)
        # Check version format
        for version in versions:
            self.assertTrue(version.startswith('v'))
    
    def test_get_configuration(self):
        """Test getting configuration"""
        cmd = ConfigureCommand(self.config_path)
        
        # Initially empty
        self.assertEqual(cmd.get_configuration(), {})
        
        # After setting configuration
        cmd.configuration = {'repo': 'test-repo', 'version': 'v1.0.0'}
        config = cmd.get_configuration()
        self.assertEqual(config, {'repo': 'test-repo', 'version': 'v1.0.0'})
        
        # Ensure it's a copy
        config['repo'] = 'modified'
        self.assertEqual(cmd.configuration['repo'], 'test-repo')
    
    def test_run_skip(self):
        """Test run with skip option"""
        cmd = ConfigureCommand(self.config_path)
        result = cmd.run(skip=True)
        
        self.assertEqual(result, 0)
        self.assertEqual(cmd.get_configuration(), {})


if __name__ == '__main__':
    unittest.main()