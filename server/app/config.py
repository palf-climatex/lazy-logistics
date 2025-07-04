import os
from typing import List, Set
from pathlib import Path

# Constants
MAX_SEARCH_RESULTS = 20

class Config:
    """Configuration management for the supplier extraction service."""
    
    def __init__(self):
        self.ignore_list_file = os.getenv("SUPPLIER_IGNORE_LIST_FILE", "suppliers/supplier_ignore_list.txt")
        self._ignored_suppliers: Set[str] = set()
        self._load_ignore_list()
    
    def _load_ignore_list(self):
        """Load the supplier ignore list from file."""
        try:
            ignore_file_path = Path(self.ignore_list_file)
            if ignore_file_path.exists():
                with open(ignore_file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        supplier_name = line.strip()
                        if supplier_name and not supplier_name.startswith('#'):
                            self._ignored_suppliers.add(supplier_name.lower())
                print(f"Loaded {len(self._ignored_suppliers)} suppliers to ignore")
            else:
                print(f"Ignore list file not found: {ignore_file_path}")
        except Exception as e:
            print(f"Error loading ignore list: {e}")
    
    def reload_ignore_list(self):
        """Reload the ignore list from file."""
        self._ignored_suppliers.clear()
        self._load_ignore_list()
    
    def is_supplier_ignored(self, supplier_name: str) -> bool:
        """Check if a supplier should be ignored."""
        return supplier_name.lower() in self._ignored_suppliers
    
    def add_to_ignore_list(self, supplier_name: str) -> bool:
        """Add a supplier to the ignore list."""
        try:
            ignore_file_path = Path(self.ignore_list_file)
            with open(ignore_file_path, 'a', encoding='utf-8') as f:
                f.write(f"{supplier_name}\n")
            self._ignored_suppliers.add(supplier_name.lower())
            return True
        except Exception as e:
            print(f"Error adding to ignore list: {e}")
            return False
    
    def remove_from_ignore_list(self, supplier_name: str) -> bool:
        """Remove a supplier from the ignore list."""
        try:
            ignore_file_path = Path(self.ignore_list_file)
            if not ignore_file_path.exists():
                return False
            
            # Read all lines except the one to remove
            with open(ignore_file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Write back all lines except the one to remove
            with open(ignore_file_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.strip() != supplier_name:
                        f.write(line)
            
            self._ignored_suppliers.discard(supplier_name.lower())
            return True
        except Exception as e:
            print(f"Error removing from ignore list: {e}")
            return False
    
    def get_ignore_list(self) -> List[str]:
        """Get the current ignore list."""
        try:
            ignore_file_path = Path(self.ignore_list_file)
            if not ignore_file_path.exists():
                return []
            
            with open(ignore_file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        except Exception as e:
            print(f"Error reading ignore list: {e}")
            return []

# Global configuration instance
config = Config() 