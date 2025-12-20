"""Comprehensive tests for error_generator module."""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from error_generator import get_int_env, get_float_env, get_bool_env


class TestGetIntEnv:
    """Test suite for get_int_env function."""

    def test_valid_integer_from_env(self, monkeypatch):
        """Test parsing valid integer from environment."""
        monkeypatch.setenv('TEST_VAR', '42')
        result = get_int_env('TEST_VAR', 10)
        assert result == 42

    def test_default_when_env_not_set(self, monkeypatch):
        """Test returns default when env var not set."""
        monkeypatch.delenv('TEST_VAR', raising=False)
        result = get_int_env('TEST_VAR', 10)
        assert result == 10

    def test_invalid_string_returns_default(self, monkeypatch, capsys):
        """Test returns default when env contains non-integer string."""
        monkeypatch.setenv('TEST_VAR', 'not_a_number')
        result = get_int_env('TEST_VAR', 10)
        assert result == 10
        
        captured = capsys.readouterr()
        assert "not a valid integer" in captured.err
        assert "Using default: 10" in captured.err

    def test_below_minimum_returns_default(self, monkeypatch, capsys):
        """Test value below minimum returns default."""
        monkeypatch.setenv('TEST_VAR', '5')
        result = get_int_env('TEST_VAR', 10, min_val=8)
        assert result == 10
        
        captured = capsys.readouterr()
        assert "below minimum 8" in captured.err

    def test_above_maximum_returns_default(self, monkeypatch, capsys):
        """Test value above maximum returns default."""
        monkeypatch.setenv('TEST_VAR', '100')
        result = get_int_env('TEST_VAR', 50, max_val=80)
        assert result == 50
        
        captured = capsys.readouterr()
        assert "exceeds maximum 80" in captured.err

    def test_value_within_range(self, monkeypatch):
        """Test valid value within min/max range."""
        monkeypatch.setenv('TEST_VAR', '50')
        result = get_int_env('TEST_VAR', 10, min_val=1, max_val=100)
        assert result == 50

    def test_negative_integer(self, monkeypatch):
        """Test parsing negative integer."""
        monkeypatch.setenv('TEST_VAR', '-5')
        result = get_int_env('TEST_VAR', 0)
        assert result == -5

    def test_zero_value(self, monkeypatch):
        """Test parsing zero value."""
        monkeypatch.setenv('TEST_VAR', '0')
        result = get_int_env('TEST_VAR', 10)
        assert result == 0

    def test_float_string_returns_default(self, monkeypatch, capsys):
        """Test float string is invalid for integer."""
        monkeypatch.setenv('TEST_VAR', '3.14')
        result = get_int_env('TEST_VAR', 10)
        assert result == 10
        
        captured = capsys.readouterr()
        assert "not a valid integer" in captured.err


class TestGetFloatEnv:
    """Test suite for get_float_env function."""

    def test_valid_float_from_env(self, monkeypatch):
        """Test parsing valid float from environment."""
        monkeypatch.setenv('TEST_VAR', '3.14')
        result = get_float_env('TEST_VAR', 1.0)
        assert result == 3.14

    def test_integer_as_float(self, monkeypatch):
        """Test parsing integer string as float."""
        monkeypatch.setenv('TEST_VAR', '42')
        result = get_float_env('TEST_VAR', 1.0)
        assert result == 42.0

    def test_default_when_env_not_set(self, monkeypatch):
        """Test returns default when env var not set."""
        monkeypatch.delenv('TEST_VAR', raising=False)
        result = get_float_env('TEST_VAR', 0.5)
        assert result == 0.5

    def test_invalid_string_returns_default(self, monkeypatch, capsys):
        """Test returns default when env contains non-numeric string."""
        monkeypatch.setenv('TEST_VAR', 'invalid')
        result = get_float_env('TEST_VAR', 0.5)
        assert result == 0.5
        
        captured = capsys.readouterr()
        assert "not a valid number" in captured.err

    def test_below_minimum_returns_default(self, monkeypatch, capsys):
        """Test value below minimum returns default."""
        monkeypatch.setenv('TEST_VAR', '0.1')
        result = get_float_env('TEST_VAR', 0.5, min_val=0.3)
        assert result == 0.5
        
        captured = capsys.readouterr()
        assert "below minimum" in captured.err

    def test_above_maximum_returns_default(self, monkeypatch, capsys):
        """Test value above maximum returns default."""
        monkeypatch.setenv('TEST_VAR', '2.0')
        result = get_float_env('TEST_VAR', 0.5, max_val=1.0)
        assert result == 0.5
        
        captured = capsys.readouterr()
        assert "exceeds maximum" in captured.err

    def test_value_within_range(self, monkeypatch):
        """Test valid value within min/max range."""
        monkeypatch.setenv('TEST_VAR', '0.7')
        result = get_float_env('TEST_VAR', 0.5, min_val=0.0, max_val=1.0)
        assert result == 0.7

    def test_scientific_notation(self, monkeypatch):
        """Test parsing scientific notation."""
        monkeypatch.setenv('TEST_VAR', '1.5e-3')
        result = get_float_env('TEST_VAR', 1.0)
        assert result == 0.0015


class TestGetBoolEnv:
    """Test suite for get_bool_env function."""

    @pytest.mark.parametrize("value,expected", [
        ('true', True),
        ('True', True),
        ('TRUE', True),
        ('1', True),
        ('yes', True),
        ('YES', True),
        ('on', True),
        ('ON', True),
        ('false', False),
        ('False', False),
        ('0', False),
        ('no', False),
        ('off', False),
        ('', False),
        ('anything_else', False),
    ])
    def test_bool_parsing(self, monkeypatch, value, expected):
        """Test various boolean string values."""
        monkeypatch.setenv('TEST_VAR', value)
        result = get_bool_env('TEST_VAR', False)
        assert result == expected

    def test_default_when_not_set(self, monkeypatch):
        """Test returns default when env var not set."""
        monkeypatch.delenv('TEST_VAR', raising=False)
        result = get_bool_env('TEST_VAR', True)
        assert result == True


class TestMainFunction:
    """Test suite for main execution function."""

    @patch('error_generator.time.sleep')
    @patch('error_generator.random.random')
    @patch('error_generator.random.randint')
    def test_dry_run_mode(self, mock_randint, mock_random, mock_sleep, 
                          monkeypatch, capsys):
        """Test dry run mode doesn't exit."""
        monkeypatch.setenv('DRY_RUN', 'true')
        monkeypatch.setenv('INTERVAL_SECONDS', '1')
        mock_random.return_value = 0.5
        mock_randint.return_value = 42
        
        # Make sleep raise exception after first call to break loop
        mock_sleep.side_effect = [None, KeyboardInterrupt()]
        
        from error_generator import main
        
        with pytest.raises(KeyboardInterrupt):
            main()
        
        captured = capsys.readouterr()
        assert "Exiting with code: 42" in captured.out
        assert "dry_run=True" in captured.out

    @patch('error_generator.sys.exit')
    @patch('error_generator.time.sleep')
    @patch('error_generator.random.random')
    @patch('error_generator.random.randint')
    def test_special_code_triggered(self, mock_randint, mock_random, 
                                    mock_sleep, mock_exit, monkeypatch, capsys):
        """Test special exit code is used when probability triggers."""
        monkeypatch.setenv('DRY_RUN', 'false')
        monkeypatch.setenv('SPECIAL_EXIT_CODE', '200')
        monkeypatch.setenv('SPECIAL_CODE_CHANCE', '0.3')
        
        mock_random.return_value = 0.1  # Less than 0.3, triggers special
        mock_exit.side_effect = SystemExit(200)  # Simulate actual exit
        
        from error_generator import main
        
        with pytest.raises(SystemExit):
            main()
        
        captured = capsys.readouterr()
        assert "Exiting with code: 200" in captured.out
        mock_exit.assert_called_once_with(200)

    @patch('error_generator.sys.exit')
    @patch('error_generator.time.sleep')
    @patch('error_generator.random.random')
    @patch('error_generator.random.randint')
    def test_normal_code_triggered(self, mock_randint, mock_random, 
                                   mock_sleep, mock_exit, monkeypatch, capsys):
        """Test normal exit code range when special not triggered."""
        monkeypatch.setenv('DRY_RUN', 'false')
        monkeypatch.setenv('MIN_EXIT_CODE', '10')
        monkeypatch.setenv('MAX_EXIT_CODE', '50')
        
        mock_random.return_value = 0.9  # Greater than default 0.3
        mock_randint.return_value = 25
        mock_exit.side_effect = SystemExit(25)
        
        from error_generator import main
        
        with pytest.raises(SystemExit):
            main()
        
        captured = capsys.readouterr()
        assert "Exiting with code: 25" in captured.out
        mock_randint.assert_called_once_with(10, 50)
        mock_exit.assert_called_once_with(25)

    def test_min_max_swap(self, monkeypatch, capsys):
        """Test min/max values are swapped when min > max."""
        monkeypatch.setenv('MIN_EXIT_CODE', '100')
        monkeypatch.setenv('MAX_EXIT_CODE', '50')
        monkeypatch.setenv('DRY_RUN', 'true')
        monkeypatch.setenv('INTERVAL_SECONDS', '1')
        
        from error_generator import main
        
        with patch('error_generator.time.sleep', side_effect=KeyboardInterrupt):
            with pytest.raises(KeyboardInterrupt):
                main()
        
        captured = capsys.readouterr()
        assert "Swapping values" in captured.err
        assert "min_code=50, max_code=100" in captured.out

    def test_configuration_output(self, monkeypatch, capsys):
        """Test configuration is printed on startup."""
        monkeypatch.setenv('MIN_EXIT_CODE', '10')
        monkeypatch.setenv('MAX_EXIT_CODE', '199')
        monkeypatch.setenv('INTERVAL_SECONDS', '5')
        monkeypatch.setenv('SPECIAL_EXIT_CODE', '200')
        monkeypatch.setenv('SPECIAL_CODE_CHANCE', '0.3')
        monkeypatch.setenv('DRY_RUN', 'true')
        
        from error_generator import main
        
        with patch('error_generator.time.sleep', side_effect=KeyboardInterrupt):
            with pytest.raises(KeyboardInterrupt):
                main()
        
        captured = capsys.readouterr()
        assert "Configuration:" in captured.out
        assert "min_code=10" in captured.out
        assert "max_code=199" in captured.out
        assert "interval=5s" in captured.out
        assert "special_code=200" in captured.out
        assert "30.0% chance" in captured.out
        assert "dry_run=True" in captured.out