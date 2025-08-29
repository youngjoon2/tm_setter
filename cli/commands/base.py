"""Base command class for CLI commands"""

import json
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional


class BaseCommand(ABC):
    """Base class for all CLI commands"""
    
    def __init__(self, config_path: str):
        """Initialize command with configuration path
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file
        
        Returns:
            Configuration dictionary
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load config: {e}", file=sys.stderr)
        return {}
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Save configuration to file
        
        Args:
            config: Configuration to save (uses self.config if None)
        """
        if config is not None:
            self.config = config
            
        # Create directory if it doesn't exist
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Warning: Failed to save config: {e}", file=sys.stderr)
    
    def get_session(self) -> Optional[Dict[str, Any]]:
        """Get current session information
        
        Returns:
            Session dictionary or None if not logged in
        """
        return self.config.get('session')
    
    def set_session(self, session: Dict[str, Any]) -> None:
        """Set session information
        
        Args:
            session: Session data to store
        """
        self.config['session'] = session
        self.save_config()
    
    def clear_session(self) -> None:
        """Clear current session"""
        if 'session' in self.config:
            del self.config['session']
            self.save_config()
    
    def print_success(self, message: str) -> None:
        """Print success message
        
        Args:
            message: Success message to print
        """
        # Use rich if available, otherwise plain text
        try:
            from rich.console import Console
            console = Console()
            console.print(f"[green]✓[/green] {message}")
        except ImportError:
            print(f"✓ {message}")
    
    def print_error(self, message: str) -> None:
        """Print error message
        
        Args:
            message: Error message to print
        """
        try:
            from rich.console import Console
            console = Console()
            console.print(f"[red]✗[/red] {message}", file=sys.stderr)
        except ImportError:
            print(f"✗ {message}", file=sys.stderr)
    
    def print_info(self, message: str) -> None:
        """Print info message
        
        Args:
            message: Info message to print
        """
        try:
            from rich.console import Console
            console = Console()
            console.print(f"[blue]ℹ[/blue] {message}")
        except ImportError:
            print(f"ℹ {message}")
    
    def print_warning(self, message: str) -> None:
        """Print warning message
        
        Args:
            message: Warning message to print
        """
        try:
            from rich.console import Console
            console = Console()
            console.print(f"[yellow]⚠[/yellow] {message}")
        except ImportError:
            print(f"⚠ {message}")
    
    @abstractmethod
    def run(self, **kwargs) -> int:
        """Run the command
        
        Args:
            **kwargs: Command-specific arguments
            
        Returns:
            Exit code (0 for success, non-zero for failure)
        """
        pass