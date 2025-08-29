"""Configure command for optional settings"""

from typing import Optional, List, Dict, Any

from cli.commands.base import BaseCommand


class ConfigureCommand(BaseCommand):
    """Handle optional configuration settings"""
    
    def __init__(self, config_path: str):
        """Initialize configure command
        
        Args:
            config_path: Path to configuration file
        """
        super().__init__(config_path)
        self.configuration: Dict[str, Any] = {}
        
    def get_available_repos(self) -> List[str]:
        """Get list of available repositories
        
        Returns:
            List of repository names
        """
        # TODO: Replace with actual API call or config
        return [
            "main-repository",
            "backend-services",
            "frontend-app",
            "mobile-app",
            "data-pipeline",
            "infrastructure",
            "documentation"
        ]
    
    def get_available_versions(self) -> List[str]:
        """Get list of available binary SW versions
        
        Returns:
            List of version strings
        """
        # TODO: Replace with actual API call or config
        return [
            "v3.0.0",
            "v2.5.1",
            "v2.5.0",
            "v2.4.3",
            "v2.4.2",
            "v2.4.1",
            "v2.4.0",
            "v2.3.0",
            "v2.2.0",
            "v2.1.0",
            "v2.0.0",
            "v1.9.0"
        ]
    
    def prompt_repository(self, pre_selected: Optional[str] = None) -> Optional[str]:
        """Prompt for repository selection
        
        Args:
            pre_selected: Pre-selected repository name
            
        Returns:
            Selected repository or None if skipped
        """
        if pre_selected:
            # Validate pre-selected value
            repos = self.get_available_repos()
            if pre_selected in repos:
                return pre_selected
            else:
                self.print_warning(f"Repository '{pre_selected}' not found")
                # Fall through to interactive selection
        
        print("\nRepository Configuration")
        print("-" * 40)
        
        # Get available repos
        repos = self.get_available_repos()
        
        try:
            from rich.console import Console
            from rich.columns import Columns
            
            console = Console()
            console.print("Available repositories:", style="cyan")
            columns = Columns(repos, equal=True, expand=False)
            console.print(columns)
        except ImportError:
            print("Available repositories:")
            for i, repo in enumerate(repos, 1):
                print(f"  {i:2}. {repo}")
        
        prompt = "\nEnter repository name or number (press Enter to skip): "
        user_input = input(prompt).strip()
        
        if not user_input:
            return None
        
        # Check if input is a number
        try:
            choice = int(user_input)
            if 1 <= choice <= len(repos):
                selected = repos[choice - 1]
                self.print_info(f"Selected repository: {selected}")
                return selected
        except ValueError:
            # Treat as repository name
            if user_input in repos:
                self.print_info(f"Selected repository: {user_input}")
                return user_input
            else:
                # Try partial match
                matches = [r for r in repos if user_input.lower() in r.lower()]
                if len(matches) == 1:
                    self.print_info(f"Selected repository: {matches[0]}")
                    return matches[0]
                elif len(matches) > 1:
                    print("Multiple matches found:")
                    for i, match in enumerate(matches, 1):
                        print(f"  {i}. {match}")
                    sub_choice = input(f"Select (1-{len(matches)}): ").strip()
                    try:
                        idx = int(sub_choice) - 1
                        if 0 <= idx < len(matches):
                            self.print_info(f"Selected repository: {matches[idx]}")
                            return matches[idx]
                    except (ValueError, IndexError):
                        pass
        
        self.print_warning("Invalid selection, skipping repository configuration")
        return None
    
    def prompt_version(self, pre_selected: Optional[str] = None) -> Optional[str]:
        """Prompt for version selection
        
        Args:
            pre_selected: Pre-selected version
            
        Returns:
            Selected version or None if skipped
        """
        if pre_selected:
            # Validate pre-selected value
            versions = self.get_available_versions()
            if pre_selected in versions:
                return pre_selected
            else:
                self.print_warning(f"Version '{pre_selected}' not found")
                # Fall through to interactive selection
        
        print("\nBinary SW Version Configuration")
        print("-" * 40)
        
        # Get available versions
        versions = self.get_available_versions()
        
        try:
            from rich.console import Console
            from rich.table import Table
            
            console = Console()
            table = Table(show_header=False, box=None)
            
            # Create 3 columns
            for i in range(0, len(versions), 3):
                row = []
                for j in range(3):
                    if i + j < len(versions):
                        row.append(f"{i+j+1:2}. {versions[i+j]}")
                    else:
                        row.append("")
                table.add_row(*row)
            
            console.print("Available versions:", style="cyan")
            console.print(table)
        except ImportError:
            print("Available versions:")
            for i, version in enumerate(versions, 1):
                print(f"  {i:2}. {version}")
        
        prompt = "\nEnter version or number (press Enter to skip): "
        user_input = input(prompt).strip()
        
        if not user_input:
            return None
        
        # Check if input is a number
        try:
            choice = int(user_input)
            if 1 <= choice <= len(versions):
                selected = versions[choice - 1]
                self.print_info(f"Selected version: {selected}")
                return selected
        except ValueError:
            # Treat as version string
            if user_input in versions:
                self.print_info(f"Selected version: {user_input}")
                return user_input
            # Try with 'v' prefix if not present
            if not user_input.startswith('v'):
                with_v = f"v{user_input}"
                if with_v in versions:
                    self.print_info(f"Selected version: {with_v}")
                    return with_v
        
        self.print_warning("Invalid selection, skipping version configuration")
        return None
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration
        
        Returns:
            Configuration dictionary
        """
        return self.configuration.copy()
    
    def run(self, repo: Optional[str] = None,
            version: Optional[str] = None,
            skip: bool = False,
            interactive: bool = False,
            **kwargs) -> int:
        """Run configure command
        
        Args:
            repo: Repository name
            version: Binary SW version
            skip: Skip configuration
            interactive: Running in interactive mode
            **kwargs: Additional arguments
            
        Returns:
            Exit code (0 for success)
        """
        # Check if user is logged in
        session = self.get_session()
        if not session or not session.get('token'):
            self.print_error("Please login first (run 'tm-setter login')")
            return 1
        
        if skip:
            self.print_info("Skipping optional configuration")
            self.configuration = {}
            self.config['configuration'] = self.configuration
            self.save_config()
            return 0
        
        try:
            print("\n" + "=" * 50)
            print("Optional Configuration")
            print("=" * 50)
            print("You can skip any option by pressing Enter")
            
            # Repository selection
            selected_repo = self.prompt_repository(repo)
            if selected_repo:
                self.configuration['repo'] = selected_repo
            
            # Version selection
            selected_version = self.prompt_version(version)
            if selected_version:
                self.configuration['version'] = selected_version
            
            # Save configuration
            self.config['configuration'] = self.configuration
            self.save_config()
            
            # Display summary
            if self.configuration:
                self.print_success("Configuration saved!")
                print("\nConfiguration Summary:")
                print("-" * 30)
                if 'repo' in self.configuration:
                    print(f"Repository: {self.configuration['repo']}")
                if 'version' in self.configuration:
                    print(f"Version: {self.configuration['version']}")
            else:
                self.print_info("No optional configuration set")
            
            return 0
            
        except KeyboardInterrupt:
            print("\nConfiguration cancelled.")
            return 130
        except Exception as e:
            self.print_error(f"Error during configuration: {e}")
            return 1