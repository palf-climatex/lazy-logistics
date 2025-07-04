#!/usr/bin/env python3
"""
Analyze supplier lists from multiple supermarkets to identify candidates for the ignore list.
Usage: python analyze_suppliers.py
"""

import json
import os
from collections import defaultdict, Counter
from typing import Dict, List, Set

def load_supplier_files() -> Dict[str, List[str]]:
    """Load all supplier JSON files and extract supplier names."""
    supplier_data = {}
    
    # Find all supplier JSON files in the suppliers directory
    suppliers_dir = 'suppliers'
    if not os.path.exists(suppliers_dir):
        print(f"Suppliers directory '{suppliers_dir}' not found!")
        return supplier_data
    
    json_files = [f for f in os.listdir(suppliers_dir) if f.startswith('suppliers_') and f.endswith('.json')]
    
    for filename in json_files:
        try:
            filepath = os.path.join(suppliers_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                company_name = data.get('company_name', filename.replace('suppliers_', '').replace('.json', ''))
                suppliers = [s['name'] for s in data.get('suppliers', [])]
                supplier_data[company_name] = suppliers
                print(f"Loaded {len(suppliers)} suppliers from {company_name}")
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    
    return supplier_data

def find_common_suppliers(supplier_data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Find suppliers that appear in multiple supermarket lists."""
    # Count occurrences of each supplier
    supplier_counts = Counter()
    supplier_locations = defaultdict(list)
    
    for company, suppliers in supplier_data.items():
        for supplier in suppliers:
            supplier_counts[supplier] += 1
            supplier_locations[supplier].append(company)
    
    # Group by count
    common_suppliers = defaultdict(list)
    for supplier, count in supplier_counts.items():
        if count > 1:  # Appears in more than one list
            common_suppliers[count].append({
                'name': supplier,
                'locations': supplier_locations[supplier]
            })
    
    return common_suppliers

def categorize_suppliers(suppliers: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize suppliers into likely ignore candidates vs actual product suppliers."""
    ignore_candidates = []
    product_suppliers = []
    
    # Keywords that suggest the supplier is a platform, service, or aggregator
    ignore_keywords = [
        'commerce', 'logistics', 'supply', 'chain', 'edi', 'platform', 'solution',
        'partner', 'service', 'management', 'system', 'software', 'technology',
        'manufacture', 'network', 'group', 'company', 'limited', 'ltd', 'corp',
        'supplier', 'vendor', 'provider', 'consultancy', 'audit', 'finance',
        'warehouse', 'distribution', 'transport', 'retail', 'trading', 'business',
        'enterprise', 'digital', 'cloud', 'data', 'analytics', 'sustainability',
        'certification', 'compliance', 'regulatory', 'standard', 'framework'
    ]
    
    # Known product brands that should NOT be ignored
    product_brands = [
        'coca', 'cola', 'unilever', 'nestle', 'kraft', 'heinz', 'kellogg',
        'general mills', 'p&g', 'procter', 'gamble', 'mars', 'wrigley',
        'ferrero', 'mondelez', 'danone', 'pepsico', 'campbell', 'conagra',
        'hershey', 'j&j', 'johnson', 'kimberly', 'clark', 'colgate', 'palmolive',
        'reckitt', 'benckiser', 'henkel', 'loreal', 'estee', 'lauder',
        'avon', 'mary kay', 'amway', 'herbalife', 'nu skin', 'tupperware'
    ]
    
    for supplier in suppliers:
        name_lower = supplier['name'].lower()
        
        # Check if it's a known product brand
        is_product_brand = any(brand in name_lower for brand in product_brands)
        
        # Check if it contains ignore keywords
        has_ignore_keywords = any(keyword in name_lower for keyword in ignore_keywords)
        
        # Check if it's a generic term
        is_generic = any(generic in name_lower for generic in [
            'supplier', 'suppliers', 'vendor', 'vendors', 'partner', 'partners',
            'manufacturer', 'manufacturers', 'producer', 'producers', 'company',
            'companies', 'business', 'enterprise', 'group', 'limited', 'ltd',
            'corporation', 'corp', 'inc', 'llc', 'plc', 'co', 'company'
        ])
        
        if is_product_brand:
            product_suppliers.append(supplier)
        elif has_ignore_keywords or is_generic:
            ignore_candidates.append(supplier)
        else:
            # Default to product supplier if uncertain
            product_suppliers.append(supplier)
    
    return {
        'ignore_candidates': ignore_candidates,
        'product_suppliers': product_suppliers
    }

def generate_ignore_list(categories: Dict[str, List[Dict]]) -> List[str]:
    """Generate a formatted ignore list from candidates."""
    ignore_list = []
    
    for supplier in categories['ignore_candidates']:
        ignore_list.append(supplier['name'])
    
    return sorted(ignore_list)

def main():
    """Main analysis function."""
    print("Analyzing supplier lists from UK supermarkets...")
    print("=" * 60)
    
    # Load supplier data
    supplier_data = load_supplier_files()
    
    if not supplier_data:
        print("No supplier files found!")
        return
    
    print(f"\nAnalyzed {len(supplier_data)} supermarket supplier lists")
    print("-" * 60)
    
    # Find common suppliers
    common_suppliers = find_common_suppliers(supplier_data)
    
    if not common_suppliers:
        print("No suppliers found in multiple lists.")
        return
    
    # Display common suppliers by frequency
    print("\nSUPPLIERS APPEARING IN MULTIPLE LISTS:")
    print("=" * 60)
    
    for count in sorted(common_suppliers.keys(), reverse=True):
        suppliers = common_suppliers[count]
        print(f"\nSuppliers appearing in {count} lists ({len(suppliers)} total):")
        print("-" * 40)
        
        for supplier in sorted(suppliers, key=lambda x: x['name']):
            locations = ', '.join(supplier['locations'])
            print(f"  {supplier['name']}")
            print(f"    Found in: {locations}")
    
    # Categorize suppliers
    all_common_suppliers = []
    for suppliers in common_suppliers.values():
        all_common_suppliers.extend(suppliers)
    
    categories = categorize_suppliers(all_common_suppliers)
    
    # Generate ignore list
    ignore_list = generate_ignore_list(categories)
    
    # Display results
    print(f"\n\nCATEGORIZATION RESULTS:")
    print("=" * 60)
    print(f"Ignore candidates: {len(categories['ignore_candidates'])}")
    print(f"Product suppliers: {len(categories['product_suppliers'])}")
    
    print(f"\n\nIGNORE CANDIDATES (recommended for ignore list):")
    print("=" * 60)
    for supplier in sorted(categories['ignore_candidates'], key=lambda x: x['name']):
        locations = ', '.join(supplier['locations'])
        print(f"  {supplier['name']} (in {len(supplier['locations'])} lists: {locations})")
    
    print(f"\n\nPRODUCT SUPPLIERS (likely actual suppliers):")
    print("=" * 60)
    for supplier in sorted(categories['product_suppliers'], key=lambda x: x['name']):
        locations = ', '.join(supplier['locations'])
        print(f"  {supplier['name']} (in {len(supplier['locations'])} lists: {locations})")
    
    # Save ignore list
    ignore_filename = "suppliers/candidate_ignore_list.txt"
    with open(ignore_filename, 'w') as f:
        f.write("# Candidate ignore list generated from supermarket supplier analysis\n")
        f.write("# Review and manually edit before adding to supplier_ignore_list.txt\n\n")
        for supplier in ignore_list:
            f.write(f"{supplier}\n")
    
    print(f"\n\nCandidate ignore list saved to: {ignore_filename}")
    print("Review this file and manually add appropriate entries to suppliers/supplier_ignore_list.txt")
    
    # Save detailed analysis
    analysis_filename = "suppliers/supplier_analysis.json"
    analysis_data = {
        'summary': {
            'total_supermarkets': len(supplier_data),
            'total_common_suppliers': len(all_common_suppliers),
            'ignore_candidates': len(categories['ignore_candidates']),
            'product_suppliers': len(categories['product_suppliers'])
        },
        'common_suppliers_by_frequency': {
            str(count): suppliers for count, suppliers in common_suppliers.items()
        },
        'categorized_suppliers': categories
    }
    
    with open(analysis_filename, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    print(f"Detailed analysis saved to: {analysis_filename}")

if __name__ == "__main__":
    main() 