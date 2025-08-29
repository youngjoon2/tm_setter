"""Select DB Code command"""

from typing import Optional, List, Dict, Any

from cli.commands.base import BaseCommand


class SelectDBCommand(BaseCommand):
    """Handle database code selection"""
    
    def __init__(self, config_path: str):
        """Initialize select DB command
        
        Args:
            config_path: Path to configuration file
        """
        super().__init__(config_path)
        self.selection: Dict[str, str] = {}
        
    def get_db_options(self, level: int, previous_selection: Optional[Dict[str, str]] = None) -> List[str]:
        """Get available database options for a given level
        
        Args:
            level: Selection level (1, 2, or 3)
            previous_selection: Previous selections to filter options
            
        Returns:
            List of available options
        """
        # TODO: Replace with actual API call to get options
        # This is mock data
        
        if level == 1:
            return [
                "Production Database",
                "Development Database", 
                "Test Database",
                "Staging Database",
                "Analytics Database"
            ]
        elif level == 2:
            # Options could depend on level 1 selection
            if previous_selection and previous_selection.get('db1') == "Production Database":
                return ["Main Schema", "Backup Schema", "Archive Schema"]
            return ["Schema A", "Schema B", "Schema C", "Schema D"]
        elif level == 3:
            # Options could depend on level 1 and 2 selections
            return [
                "Users Table",
                "Products Table", 
                "Orders Table",
                "Transactions Table",
                "Logs Table",
                "Configuration Table"
            ]
        
        return []
    
    def search_options(self, options: List[str], search_term: str) -> List[tuple[int, str]]:
        """Search and filter options
        
        Args:
            options: List of options to search
            search_term: Search term
            
        Returns:
            List of (index, option) tuples matching search
        """
        search_lower = search_term.lower()
        results = []
        
        for i, option in enumerate(options):
            if search_lower in option.lower():
                results.append((i, option))
        
        return results
    
    def display_options(self, options: List[str], title: str) -> None:
        """Display options in a formatted way
        
        Args:
            options: List of options to display
            title: Title for the selection
        """
        try:
            from rich.console import Console
            from rich.table import Table
            
            console = Console()
            table = Table(title=title, show_header=True, header_style="bold cyan")
            table.add_column("#", style="dim", width=4)
            table.add_column("Option", style="white")
            
            for i, option in enumerate(options, 1):
                table.add_row(str(i), option)
            
            console.print(table)
        except ImportError:
            print(f"\n{title}")
            print("-" * 40)
            for i, option in enumerate(options, 1):
                print(f"{i:2}. {option}")
            print("-" * 40)
    
    def prompt_selection(self, level: int, options: List[str], 
                        pre_selected: Optional[str] = None) -> Optional[str]:
        """Prompt user to select an option
        
        Args:
            level: Selection level (1, 2, or 3)
            options: Available options
            pre_selected: Pre-selected value (for command-line mode)
            
        Returns:
            Selected option or None if cancelled
        """
        if pre_selected:
            # Validate pre-selected value
            if pre_selected in options:
                return pre_selected
            else:
                self.print_warning(f"'{pre_selected}' not found in available options")
                # Fall through to interactive selection
        
        level_names = {
            1: "first database item",
            2: "second database item",
            3: "third database item"
        }
        
        self.display_options(options, f"Select {level_names[level]}")
        
        while True:
            prompt = f"Enter number (1-{len(options)}) or search term (or 'q' to quit): "
            user_input = input(prompt).strip()
            
            if user_input.lower() == 'q':
                return None
            
            # Check if input is a number
            try:
                choice = int(user_input)
                if 1 <= choice <= len(options):
                    selected = options[choice - 1]
                    self.print_info(f"Selected: {selected}")
                    return selected
                else:
                    self.print_error(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                # Treat as search term
                matches = self.search_options(options, user_input)
                
                if not matches:
                    self.print_warning("No matches found. Try again.")
                elif len(matches) == 1:
                    _, selected = matches[0]
                    self.print_info(f"Selected: {selected}")
                    return selected
                else:
                    # Multiple matches, show them
                    print("\nSearch results:")
                    for idx, (_, option) in enumerate(matches, 1):
                        print(f"  {idx}. {option}")
                    
                    sub_choice = input(f"Select from results (1-{len(matches)}): ").strip()
                    try:
                        sub_idx = int(sub_choice) - 1
                        if 0 <= sub_idx < len(matches):
                            _, selected = matches[sub_idx]
                            self.print_info(f"Selected: {selected}")
                            return selected
                    except (ValueError, IndexError):
                        self.print_error("Invalid selection")
    
    def get_selection(self) -> Dict[str, str]:
        """Get current selection
        
        Returns:
            Dictionary with db1, db2, db3 selections
        """
        return self.selection.copy()
    
    def run(self, db1: Optional[str] = None,
            db2: Optional[str] = None, 
            db3: Optional[str] = None,
            interactive: bool = False,
            **kwargs) -> int:
        """Run select DB command
        
        Args:
            db1: First database selection
            db2: Second database selection
            db3: Third database selection
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
        
        try:
            # Level 1 selection
            options1 = self.get_db_options(1)
            selected1 = self.prompt_selection(1, options1, db1)
            if not selected1:
                self.print_warning("Selection cancelled")
                return 1
            self.selection['db1'] = selected1
            
            # Level 2 selection
            options2 = self.get_db_options(2, self.selection)
            selected2 = self.prompt_selection(2, options2, db2)
            if not selected2:
                self.print_warning("Selection cancelled")
                return 1
            self.selection['db2'] = selected2
            
            # Level 3 selection
            options3 = self.get_db_options(3, self.selection)
            selected3 = self.prompt_selection(3, options3, db3)
            if not selected3:
                self.print_warning("Selection cancelled")
                return 1
            self.selection['db3'] = selected3
            
            # Save selection to config
            self.config['db_selection'] = self.selection
            self.save_config()
            
            # Display summary
            self.print_success("Database code selection complete!")
            print(f"\nSelected: {selected1} / {selected2} / {selected3}")
            
            return 0
            
        except KeyboardInterrupt:
            print("\nSelection cancelled.")
            return 130
        except Exception as e:
            self.print_error(f"Error during selection: {e}")
            return 1