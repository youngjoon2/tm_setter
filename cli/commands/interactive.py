"""Interactive mode command for step-by-step configuration"""

import sys
from typing import Any, Dict, Optional

from cli.commands.base import BaseCommand
from cli.commands.login import LoginCommand
from cli.commands.select_db import SelectDBCommand
from cli.commands.select_issue import SelectIssueCommand
from cli.commands.configure import ConfigureCommand
from cli import __version__


class InteractiveCommand(BaseCommand):
    """Interactive mode command handler"""
    
    def __init__(self, config_path: str):
        """Initialize interactive command
        
        Args:
            config_path: Path to configuration file
        """
        super().__init__(config_path)
        self.current_step: int = 1
        self.total_steps: int = 4
        self.state: Dict[str, Any] = {}
        
    def print_header(self) -> None:
        """Print welcome header"""
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.text import Text
            
            console = Console()
            title = Text(f"TM Setter CLI v{__version__}", style="bold cyan")
            subtitle = Text("Terminal-based tool for database code selection and Jira issue management", style="dim")
            
            panel = Panel.fit(
                Text.from_markup(f"{title}\n{subtitle}"),
                border_style="cyan"
            )
            console.print(panel)
        except ImportError:
            print("=" * 60)
            print(f"TM Setter CLI v{__version__}")
            print("Terminal-based tool for database code selection and Jira issue management")
            print("=" * 60)
    
    def print_step(self, step: int, title: str) -> None:
        """Print current step information
        
        Args:
            step: Current step number
            title: Step title
        """
        try:
            from rich.console import Console
            console = Console()
            console.print(f"\n[bold cyan][Step {step}/{self.total_steps}][/bold cyan] {title}")
        except ImportError:
            print(f"\n[Step {step}/{self.total_steps}] {title}")
    
    def prompt_continue(self, message: str = "Press Enter to continue, or 'q' to quit: ") -> bool:
        """Prompt user to continue
        
        Args:
            message: Prompt message
            
        Returns:
            True to continue, False to quit
        """
        response = input(message).strip().lower()
        return response != 'q'
    
    def prompt_go_back(self) -> bool:
        """Ask if user wants to go back to previous step
        
        Returns:
            True to go back, False to continue
        """
        response = input("\nDo you want to go back to the previous step? (y/N): ").strip().lower()
        return response == 'y'
    
    def run_step_login(self) -> bool:
        """Run login step
        
        Returns:
            True if successful, False otherwise
        """
        self.print_step(1, "User Authentication")
        
        # Check if already logged in
        session = self.get_session()
        if session and session.get('token'):
            self.print_info(f"Already logged in as {session.get('username', 'user')}")
            response = input("Do you want to re-login? (y/N): ").strip().lower()
            if response != 'y':
                return True
        
        # Run login command
        login_cmd = LoginCommand(str(self.config_path))
        result = login_cmd.run(interactive=True)
        
        if result == 0:
            self.state['logged_in'] = True
            self.state['session'] = self.get_session()
            return True
        
        return False
    
    def run_step_select_db(self) -> bool:
        """Run DB selection step
        
        Returns:
            True if successful, False otherwise
        """
        self.print_step(2, "Select DB Code")
        
        # Check if already selected
        if 'db_selection' in self.state:
            self.print_info(f"Already selected: {self.state['db_selection']}")
            response = input("Do you want to re-select? (y/N): ").strip().lower()
            if response != 'y':
                return True
        
        # Run select-db command
        db_cmd = SelectDBCommand(str(self.config_path))
        result = db_cmd.run(interactive=True)
        
        if result == 0:
            # Store selection in state
            self.state['db_selection'] = db_cmd.get_selection()
            return True
        
        return False
    
    def run_step_select_issue(self) -> bool:
        """Run issue selection step
        
        Returns:
            True if successful, False otherwise
        """
        self.print_step(3, "Select Jira Issue")
        
        # Check if already selected
        if 'issue_selection' in self.state:
            self.print_info(f"Already selected: {self.state['issue_selection']}")
            response = input("Do you want to re-select? (y/N): ").strip().lower()
            if response != 'y':
                return True
        
        # Pass DB selection to issue command
        issue_cmd = SelectIssueCommand(str(self.config_path))
        issue_cmd.set_db_filter(self.state.get('db_selection', {}))
        result = issue_cmd.run(interactive=True)
        
        if result == 0:
            self.state['issue_selection'] = issue_cmd.get_selection()
            return True
        
        return False
    
    def run_step_configure(self) -> bool:
        """Run configuration step
        
        Returns:
            True if successful, False otherwise
        """
        self.print_step(4, "Configuration (Optional)")
        
        # Check if already configured
        if 'configuration' in self.state:
            self.print_info("Already configured")
            response = input("Do you want to re-configure? (y/N): ").strip().lower()
            if response != 'y':
                return True
        
        # Run configure command
        config_cmd = ConfigureCommand(str(self.config_path))
        result = config_cmd.run(interactive=True)
        
        if result == 0:
            self.state['configuration'] = config_cmd.get_configuration()
            return True
        
        return False
    
    def process_final(self) -> int:
        """Process final action with collected data
        
        Returns:
            Exit code
        """
        self.print_info("\nProcessing with collected information...")
        
        try:
            from rich.progress import Progress, SpinnerColumn, TextColumn
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                task = progress.add_task("Processing...", total=None)
                
                # Simulate processing (replace with actual implementation)
                import time
                time.sleep(2)
                
                progress.update(task, description="Finalizing...")
                time.sleep(1)
        except ImportError:
            print("Processing...")
            import time
            time.sleep(2)
        
        # Save state for resume functionality
        self.config['last_state'] = self.state
        self.save_config()
        
        self.print_success("Task completed successfully!")
        
        # Display summary
        self.print_summary()
        
        return 0
    
    def print_summary(self) -> None:
        """Print summary of selections"""
        print("\n" + "=" * 40)
        print("Summary:")
        print("-" * 40)
        
        if 'session' in self.state:
            print(f"User: {self.state['session'].get('username', 'N/A')}")
        
        if 'db_selection' in self.state:
            db = self.state['db_selection']
            print(f"DB Code: {db.get('db1', 'N/A')} / {db.get('db2', 'N/A')} / {db.get('db3', 'N/A')}")
        
        if 'issue_selection' in self.state:
            issue = self.state['issue_selection']
            print(f"Issue: {issue.get('key', 'N/A')} - {issue.get('summary', 'N/A')}")
        
        if 'configuration' in self.state:
            config = self.state['configuration']
            if config.get('repo'):
                print(f"Repository: {config['repo']}")
            if config.get('version'):
                print(f"Version: {config['version']}")
        
        print("=" * 40)
    
    def run(self, resume: bool = False, **kwargs) -> int:
        """Run interactive mode
        
        Args:
            resume: Resume from last saved state
            **kwargs: Additional arguments
            
        Returns:
            Exit code
        """
        self.print_header()
        
        # Load previous state if resuming
        if resume and 'last_state' in self.config:
            self.state = self.config['last_state']
            self.print_info("Resuming from previous session...")
            self.print_summary()
        
        # Track current step for navigation
        steps = [
            self.run_step_login,
            self.run_step_select_db,
            self.run_step_select_issue,
            self.run_step_configure
        ]
        
        current = 0
        while current < len(steps):
            try:
                # Run current step
                success = steps[current]()
                
                if not success:
                    # Step failed, ask to retry or go back
                    response = input("\nRetry (r), go back (b), or quit (q)? ").strip().lower()
                    if response == 'q':
                        print("\nOperation cancelled.")
                        return 1
                    elif response == 'b' and current > 0:
                        current -= 1
                        continue
                    else:
                        continue  # Retry current step
                
                # Step succeeded, check if user wants to go back
                if current < len(steps) - 1:  # Not on last step
                    if self.prompt_go_back():
                        if current > 0:
                            current -= 1
                            continue
                
                # Move to next step
                current += 1
                
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                return 130
            except Exception as e:
                self.print_error(f"Error in step: {e}")
                response = input("\nRetry (r), go back (b), or quit (q)? ").strip().lower()
                if response == 'q':
                    return 1
                elif response == 'b' and current > 0:
                    current -= 1
                # Otherwise retry current step
        
        # All steps completed, process final action
        return self.process_final()