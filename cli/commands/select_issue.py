"""Select Jira Issue command"""

from typing import Optional, List, Dict, Any
import math

from cli.commands.base import BaseCommand


class SelectIssueCommand(BaseCommand):
    """Handle Jira issue selection"""
    
    def __init__(self, config_path: str):
        """Initialize select issue command
        
        Args:
            config_path: Path to configuration file
        """
        super().__init__(config_path)
        self.selection: Dict[str, Any] = {}
        self.db_filter: Dict[str, str] = {}
        
    def set_db_filter(self, db_selection: Dict[str, str]) -> None:
        """Set DB filter for issue selection
        
        Args:
            db_selection: Database selection to filter issues
        """
        self.db_filter = db_selection
    
    def fetch_issues(self, filter_text: Optional[str] = None, 
                    page: int = 1, 
                    limit: int = 10) -> tuple[List[Dict[str, Any]], int]:
        """Fetch Jira issues based on filters
        
        Args:
            filter_text: Text to filter issues
            page: Page number for pagination
            limit: Number of issues per page
            
        Returns:
            Tuple of (issues list, total count)
        """
        # TODO: Replace with actual Jira API call
        # This is mock data
        
        all_issues = [
            {"key": "PROJ-101", "summary": "Implement user authentication", "status": "Open", "assignee": "John Doe"},
            {"key": "PROJ-102", "summary": "Fix database connection pool", "status": "In Progress", "assignee": "Jane Smith"},
            {"key": "PROJ-103", "summary": "Update API documentation", "status": "Todo", "assignee": "Unassigned"},
            {"key": "PROJ-104", "summary": "Optimize query performance", "status": "In Review", "assignee": "Bob Wilson"},
            {"key": "PROJ-105", "summary": "Add unit tests for service layer", "status": "Open", "assignee": "Alice Brown"},
            {"key": "PROJ-106", "summary": "Refactor legacy code", "status": "Todo", "assignee": "Unassigned"},
            {"key": "PROJ-107", "summary": "Implement caching mechanism", "status": "In Progress", "assignee": "Charlie Davis"},
            {"key": "PROJ-108", "summary": "Security audit findings", "status": "Open", "assignee": "David Lee"},
            {"key": "PROJ-109", "summary": "Migrate to new infrastructure", "status": "Planning", "assignee": "Eve Martinez"},
            {"key": "PROJ-110", "summary": "Performance monitoring setup", "status": "Done", "assignee": "Frank Garcia"},
            {"key": "PROJ-111", "summary": "Bug fix for login issue", "status": "In Progress", "assignee": "Grace Kim"},
            {"key": "PROJ-112", "summary": "Feature: Dark mode support", "status": "Open", "assignee": "Henry Chen"},
        ]
        
        # Apply filter if provided
        if filter_text:
            filter_lower = filter_text.lower()
            all_issues = [
                issue for issue in all_issues
                if filter_lower in issue['key'].lower() or 
                   filter_lower in issue['summary'].lower() or
                   filter_lower in issue['status'].lower()
            ]
        
        # Apply DB filter if set
        if self.db_filter:
            # In real implementation, this would filter based on DB selection
            pass
        
        # Calculate pagination
        total = len(all_issues)
        start = (page - 1) * limit
        end = min(start + limit, total)
        
        return all_issues[start:end], total
    
    def display_issues_table(self, issues: List[Dict[str, Any]], 
                            page: int = 1, 
                            total: int = 0,
                            limit: int = 10) -> None:
        """Display issues in a table format
        
        Args:
            issues: List of issues to display
            page: Current page number
            total: Total number of issues
            limit: Issues per page
        """
        if not issues:
            self.print_warning("No issues found")
            return
        
        total_pages = math.ceil(total / limit) if total > 0 else 1
        
        try:
            from rich.console import Console
            from rich.table import Table
            
            console = Console()
            
            # Create table
            table = Table(
                title=f"Jira Issues (Page {page}/{total_pages}, Total: {total})",
                show_header=True,
                header_style="bold cyan"
            )
            
            table.add_column("#", style="dim", width=4)
            table.add_column("Key", style="cyan", width=12)
            table.add_column("Summary", style="white")
            table.add_column("Status", style="yellow", width=15)
            table.add_column("Assignee", style="green", width=15)
            
            for i, issue in enumerate(issues, 1):
                table.add_row(
                    str(i),
                    issue['key'],
                    issue['summary'][:50] + "..." if len(issue['summary']) > 50 else issue['summary'],
                    issue['status'],
                    issue.get('assignee', 'Unassigned')
                )
            
            console.print(table)
            
        except ImportError:
            # Fallback to simple display
            print(f"\nJira Issues (Page {page}/{total_pages}, Total: {total})")
            print("=" * 80)
            print(f"{'#':>3} | {'Key':<12} | {'Summary':<35} | {'Status':<12} | {'Assignee':<15}")
            print("-" * 80)
            
            for i, issue in enumerate(issues, 1):
                summary = issue['summary'][:35] + "..." if len(issue['summary']) > 35 else issue['summary']
                print(f"{i:>3} | {issue['key']:<12} | {summary:<35} | {issue['status']:<12} | {issue.get('assignee', 'Unassigned'):<15}")
            
            print("=" * 80)
    
    def prompt_issue_selection(self, issues: List[Dict[str, Any]], 
                              pre_selected: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Prompt user to select an issue
        
        Args:
            issues: List of issues to choose from
            pre_selected: Pre-selected issue key
            
        Returns:
            Selected issue or None if cancelled
        """
        if pre_selected:
            # Find issue by key
            for issue in issues:
                if issue['key'] == pre_selected:
                    return issue
            self.print_warning(f"Issue '{pre_selected}' not found")
            # Fall through to interactive selection
        
        while True:
            prompt = "\nEnter issue number, issue key, or command (n=next, p=prev, s=search, q=quit): "
            user_input = input(prompt).strip()
            
            if user_input.lower() == 'q':
                return None
            elif user_input.lower() in ['n', 'p', 's']:
                return user_input.lower()  # Return command for pagination/search
            
            # Check if input is a number
            try:
                choice = int(user_input)
                if 1 <= choice <= len(issues):
                    return issues[choice - 1]
                else:
                    self.print_error(f"Please enter a number between 1 and {len(issues)}")
            except ValueError:
                # Check if it's an issue key
                user_input_upper = user_input.upper()
                for issue in issues:
                    if issue['key'] == user_input_upper:
                        return issue
                self.print_error(f"Issue key '{user_input}' not found in current page")
    
    def get_selection(self) -> Dict[str, Any]:
        """Get current selection
        
        Returns:
            Selected issue dictionary
        """
        return self.selection.copy()
    
    def run(self, issue_key: Optional[str] = None,
            filter_text: Optional[str] = None,
            limit: int = 10,
            interactive: bool = False,
            **kwargs) -> int:
        """Run select issue command
        
        Args:
            issue_key: Pre-selected issue key
            filter_text: Filter text for issues
            limit: Number of issues per page
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
        
        # Load DB selection if available
        if 'db_selection' in self.config:
            self.db_filter = self.config['db_selection']
            if self.db_filter:
                db_str = f"{self.db_filter.get('db1', 'N/A')} / {self.db_filter.get('db2', 'N/A')} / {self.db_filter.get('db3', 'N/A')}"
                self.print_info(f"Filtering issues for DB: {db_str}")
        
        try:
            page = 1
            search_filter = filter_text
            
            while True:
                # Fetch issues
                try:
                    from rich.progress import Progress, SpinnerColumn, TextColumn
                    
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        transient=True,
                    ) as progress:
                        task = progress.add_task("Fetching issues...", total=None)
                        issues, total = self.fetch_issues(search_filter, page, limit)
                except ImportError:
                    print("Fetching issues...")
                    issues, total = self.fetch_issues(search_filter, page, limit)
                
                if not issues and page == 1:
                    self.print_warning("No issues found")
                    return 1
                
                # Display issues
                self.display_issues_table(issues, page, total, limit)
                
                # Get selection
                result = self.prompt_issue_selection(issues, issue_key if page == 1 else None)
                
                if result is None:
                    self.print_warning("Selection cancelled")
                    return 1
                elif result == 'n':
                    # Next page
                    max_pages = math.ceil(total / limit)
                    if page < max_pages:
                        page += 1
                    else:
                        self.print_warning("Already on last page")
                elif result == 'p':
                    # Previous page
                    if page > 1:
                        page -= 1
                    else:
                        self.print_warning("Already on first page")
                elif result == 's':
                    # Search
                    search_term = input("Enter search term (or press Enter to clear filter): ").strip()
                    search_filter = search_term if search_term else None
                    page = 1  # Reset to first page
                elif isinstance(result, dict):
                    # Issue selected
                    self.selection = result
                    
                    # Save selection
                    self.config['issue_selection'] = self.selection
                    self.save_config()
                    
                    # Display selection
                    self.print_success(f"Selected issue: {result['key']}")
                    print(f"Summary: {result['summary']}")
                    print(f"Status: {result['status']}")
                    print(f"Assignee: {result.get('assignee', 'Unassigned')}")
                    
                    return 0
                
                # Clear issue_key after first iteration
                issue_key = None
                
        except KeyboardInterrupt:
            print("\nSelection cancelled.")
            return 130
        except Exception as e:
            self.print_error(f"Error during selection: {e}")
            return 1