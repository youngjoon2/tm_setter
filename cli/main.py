#!/usr/bin/env python3
"""TM Setter CLI - Main entry point"""

import argparse
import sys
from typing import Optional
from pathlib import Path

from cli.commands.interactive import InteractiveCommand
from cli.commands.login import LoginCommand
from cli.commands.select_db import SelectDBCommand
from cli.commands.select_issue import SelectIssueCommand
from cli.commands.configure import ConfigureCommand
from cli import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog='tm-setter',
        description='TM Setter CLI - Terminal-based tool for database code selection and Jira issue management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  tm-setter
  tm-setter interactive
  
  # Individual commands
  tm-setter login --id john.doe
  tm-setter select-db --db1 "Database A" --db2 "Schema X" --db3 "Table Alpha"
  tm-setter select-issue --issue PROJ-123
  tm-setter configure --repo my-repo --version v2.1.0
  
  # Help for specific commands
  tm-setter login --help
  tm-setter select-db --help
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file (default: ~/.tm-setter/config.json)',
        default=str(Path.home() / '.tm-setter' / 'config.json')
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )
    
    # Interactive mode (default)
    interactive_parser = subparsers.add_parser(
        'interactive',
        help='Run in interactive mode (default)'
    )
    interactive_parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from last saved state'
    )
    
    # Login command
    login_parser = subparsers.add_parser(
        'login',
        help='Authenticate user'
    )
    login_parser.add_argument(
        '--id',
        type=str,
        help='User ID (password will be prompted)'
    )
    login_parser.add_argument(
        '--save',
        action='store_true',
        help='Save credentials for future use'
    )
    
    # Select DB command
    db_parser = subparsers.add_parser(
        'select-db',
        help='Select database code'
    )
    db_parser.add_argument(
        '--db1',
        type=str,
        help='First database selection'
    )
    db_parser.add_argument(
        '--db2',
        type=str,
        help='Second database selection'
    )
    db_parser.add_argument(
        '--db3',
        type=str,
        help='Third database selection'
    )
    
    # Select issue command
    issue_parser = subparsers.add_parser(
        'select-issue',
        help='Select Jira issue'
    )
    issue_parser.add_argument(
        '--issue',
        type=str,
        help='Jira issue key (e.g., PROJ-123)'
    )
    issue_parser.add_argument(
        '--filter',
        type=str,
        help='Filter issues by status or keyword'
    )
    issue_parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Limit number of issues displayed (default: 10)'
    )
    
    # Configure command
    config_parser = subparsers.add_parser(
        'configure',
        help='Configure optional settings'
    )
    config_parser.add_argument(
        '--repo',
        type=str,
        help='Repository name'
    )
    config_parser.add_argument(
        '--version',
        type=str,
        help='Binary SW version'
    )
    config_parser.add_argument(
        '--skip',
        action='store_true',
        help='Skip configuration and use defaults'
    )
    
    return parser


def main(argv: Optional[list] = None) -> int:
    """Main entry point for CLI"""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Set up verbose logging if requested
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    
    # Default to interactive mode if no command specified
    if not args.command:
        args.command = 'interactive'
    
    try:
        # Route to appropriate command handler
        if args.command == 'interactive':
            cmd = InteractiveCommand(config_path=args.config)
            return cmd.run(resume=getattr(args, 'resume', False))
            
        elif args.command == 'login':
            cmd = LoginCommand(config_path=args.config)
            return cmd.run(
                user_id=args.id,
                save_credentials=args.save
            )
            
        elif args.command == 'select-db':
            cmd = SelectDBCommand(config_path=args.config)
            return cmd.run(
                db1=args.db1,
                db2=args.db2,
                db3=args.db3
            )
            
        elif args.command == 'select-issue':
            cmd = SelectIssueCommand(config_path=args.config)
            return cmd.run(
                issue_key=args.issue,
                filter_text=args.filter,
                limit=args.limit
            )
            
        elif args.command == 'configure':
            cmd = ConfigureCommand(config_path=args.config)
            return cmd.run(
                repo=args.repo,
                version=args.version,
                skip=args.skip
            )
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 130
    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())