#!/usr/bin/env python3
"""
Generate 92,332 random smart contract transaction dataset
for comprehensive benchmark testing.
"""

import json
import csv
import random
import time
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class RandomDatasetGenerator:
    """Generate realistic random transaction data for benchmarking."""
    
    def __init__(self, seed=42):
        random.seed(seed)
        self.dataset_size = 92332
        self.transactions = []
        self.attack_scenarios = []
        
    def generate_random_address(self) -> str:
        """Generate random Ethereum-style address."""
        return '0x' + ''.join(random.choices('0123456789abcdef', k=40))
    
    def generate_random_hash(self) -> str:
        """Generate random transaction hash."""
        return '0x' + ''.join(random.choices('0123456789abcdef', k=64))
    
    def generate_transaction(self, tx_id: int) -> Dict:
        """Generate a single random transaction."""
        base_time = datetime(2026, 7, 1)
        tx_time = base_time + timedelta(seconds=random.randint(0, 864000))  # 10 days
        
        return {
            'tx_id': tx_id,
            'timestamp': tx_time.isoformat(),
            'from_address': self.generate_random_address(),
            'to_address': self.generate_random_address(),
            'value_wei': random.randint(100, 10000000000000000),  # Random wei amount
            'gas_limit': random.choice([21000, 50000, 100000, 200000, 500000, 1000000]),
            'gas_price_gwei': round(random.uniform(20, 200), 2),
            'data': '0x' + ''.join(random.choices('0123456789abcdef', k=random.randint(0, 256))),
            'nonce': random.randint(0, 10000),
            'tx_hash': self.generate_random_hash(),
            'status': random.choice(['success', 'failed', 'pending']),
            'block_number': random.randint(10000000, 20000000),
            'function_selector': random.choice(['transfer', 'approve', 'mint', 'burn', 'swap', 'stake']),
            'contract_type': random.choice(['ERC20', 'ERC721', 'ERC1155', 'Custom']),
        }
    
    def generate_transactions(self) -> List[Dict]:
        """Generate all 92,332 transactions."""
        print(f"Generating {self.dataset_size:,} random transactions...")
        start_time = time.time()
        
        for i in range(self.dataset_size):
            self.transactions.append(self.generate_transaction(i))
            if (i + 1) % 10000 == 0:
                elapsed = time.time() - start_time
                print(f"  Generated {i + 1:,} transactions ({elapsed:.2f}s)")
        
        print(f"✓ Completed in {time.time() - start_time:.2f}s\n")
        return self.transactions
    
    def generate_attack_scenarios(self) -> List[Dict]:
        """Generate attack scenario configurations."""
        print("Generating attack scenarios...")
        
        scenarios = [
            {
                'attack_id': 'reentrancy_001',
                'attack_type': 'Reentrancy',
                'description': 'Classic reentrancy attack on withdrawal pattern',
                'target_contracts': random.sample(range(100), 10),
                'expected_damage': random.randint(1000000, 100000000),
                'complexity': 'high',
                'mitigation': 'checks-effects-interactions',
                'exploit_rate': round(random.uniform(0.1, 0.9), 3),
            },
            {
                'attack_id': 'replay_001',
                'attack_type': 'Replay Attack',
                'description': 'Cross-chain replay attack simulation',
                'target_contracts': random.sample(range(100), 5),
                'expected_damage': random.randint(500000, 50000000),
                'complexity': 'medium',
                'mitigation': 'chain-id-validation',
                'exploit_rate': round(random.uniform(0.05, 0.5), 3),
            },
            {
                'attack_id': 'oracle_001',
                'attack_type': 'Oracle Manipulation',
                'description': 'Flash loan oracle price manipulation',
                'target_contracts': random.sample(range(100), 8),
                'expected_damage': random.randint(5000000, 500000000),
                'complexity': 'high',
                'mitigation': 'multi-source-oracle',
                'exploit_rate': round(random.uniform(0.2, 0.8), 3),
            },
            {
                'attack_id': 'gas_griefing_001',
                'attack_type': 'Gas Griefing',
                'description': 'Excessive gas consumption attack',
                'target_contracts': random.sample(range(100), 15),
                'expected_damage': random.randint(100000, 10000000),
                'complexity': 'low',
                'mitigation': 'gas-optimization',
                'exploit_rate': round(random.uniform(0.1, 0.6), 3),
            },
            {
                'attack_id': 'access_control_001',
                'attack_type': 'Unauthorized Access',
                'description': 'Missing access control checks',
                'target_contracts': random.sample(range(100), 12),
                'expected_damage': random.randint(2000000, 200000000),
                'complexity': 'medium',
                'mitigation': 'role-based-access',
                'exploit_rate': round(random.uniform(0.15, 0.7), 3),
            },
        ]
        
        # Add more random attack scenarios
        for i in range(5, 50):
            scenarios.append({
                'attack_id': f'attack_{i:03d}',
                'attack_type': random.choice(['Reentrancy', 'Replay', 'Oracle', 'Gas Griefing', 'Access Control']),
                'description': f'Attack scenario {i}',
                'target_contracts': random.sample(range(100), random.randint(1, 20)),
                'expected_damage': random.randint(100000, 1000000000),
                'complexity': random.choice(['low', 'medium', 'high']),
                'mitigation': random.choice(['pattern-based', 'validation-based', 'oracle-based']),
                'exploit_rate': round(random.uniform(0.01, 0.95), 3),
            })
        
        self.attack_scenarios = scenarios
        print(f"✓ Generated {len(scenarios)} attack scenarios\n")
        return scenarios
    
    def save_transaction_csv(self, filename='dataset/RandomTransactions_92332.csv'):
        """Save transactions to CSV file."""
        print(f"Saving transactions to {filename}...")
        with open(filename, 'w', newline='') as f:
            if not self.transactions:
                return
            writer = csv.DictWriter(f, fieldnames=self.transactions[0].keys())
            writer.writeheader()
            writer.writerows(self.transactions)
        print(f"✓ Saved {len(self.transactions):,} transactions\n")
    
    def save_attack_scenarios_json(self, filename='dataset/attackScenarios_92332.json'):
        """Save attack scenarios to JSON file."""
        print(f"Saving attack scenarios to {filename}...")
        with open(filename, 'w') as f:
            json.dump(self.attack_scenarios, f, indent=2)
        print(f"✓ Saved {len(self.attack_scenarios)} scenarios\n")
    
    def generate_benchmark_config(self, filename='dataset/benchmarkConfig_92332.json'):
        """Generate benchmark configuration."""
        print(f"Generating benchmark configuration...")
        config = {
            'experiment_name': 'Random Dataset Benchmark - 92,332 Transactions',
            'dataset_size': self.dataset_size,
            'timestamp': datetime.now().isoformat(),
            'configuration': {
                'transaction_count': self.dataset_size,
                'attack_scenarios': len(self.attack_scenarios),
                'time_range': '10 days (2026-07-01 to 2026-07-11)',
                'seed': 42,
                'gas_limits': [21000, 50000, 100000, 200000, 500000, 1000000],
                'contract_types': ['ERC20', 'ERC721', 'ERC1155', 'Custom'],
                'function_selectors': ['transfer', 'approve', 'mint', 'burn', 'swap', 'stake'],
            },
            'metrics_to_collect': [
                'gas_consumption',
                'transaction_latency',
                'attack_success_rate',
                'throughput_tps',
                'security_vulnerabilities',
                'contract_optimization_score',
            ],
            'test_suites': [
                'benchmark.test.js',
                'security.test.js',
                'oracle.test.js',
                'performance.test.js',
                'scalability.test.js',
                'attacks.test.js',
            ],
            'expected_outputs': [
                'results/gas_results_92332.csv',
                'results/latency_results_92332.csv',
                'results/attack_results_92332.csv',
                'results/scalability_results_92332.csv',
                'results/statistical_summary_92332.csv',
            ],
        }
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ Saved benchmark configuration\n")
        return config

if __name__ == '__main__':
    print("\n" + "="*70)
    print("Random Dataset Generator for Smart Contract Benchmark")
    print("="*70 + "\n")
    
    generator = RandomDatasetGenerator(seed=42)
    
    # Generate transactions
    transactions = generator.generate_transactions()
    
    # Generate attack scenarios
    attacks = generator.generate_attack_scenarios()
    
    # Save files
    generator.save_transaction_csv()
    generator.save_attack_scenarios_json()
    generator.generate_benchmark_config()
    
    # Print summary
    print("\n" + "="*70)
    print("Dataset Generation Summary")
    print("="*70)
    print(f"Total Transactions: {len(transactions):,}")
    print(f"Attack Scenarios: {len(attacks)}")
    print(f"Files Generated:")
    print(f"  - RandomTransactions_92332.csv")
    print(f"  - attackScenarios_92332.json")
    print(f"  - benchmarkConfig_92332.json")
    print(f"\nDataset is ready for benchmarking!")
    print("="*70 + "\n")
