# SecureSmartContractBenchmark
DigitalTwinand Security 
SecureSmartContractBenchmark/
│
├── README.md
├── LICENSE
├── CITATION.cff
├── .gitignore
├── package.json
├── hardhat.config.js
├── requirements.txt
├── .env.example
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
│
├── contracts/
│   ├── ProposedFramework.sol
│   ├── BaselineContract.sol
│   ├── OracleManager.sol
│   ├── AccessManager.sol
│   ├── RuntimeMonitor.sol
│   │
│   ├── interfaces/
│   │      IOracle.sol
│   │      IRuntime.sol
│   │
│   ├── libraries/
│   │      SecurityLibrary.sol
│   │      OptimizationLibrary.sol
│   │
│   └── attacks/
│          ReentrancyAttack.sol
│          ReplayAttack.sol
│          UnauthorizedAttack.sol
│          OracleAttack.sol
│          GasGriefingAttack.sol
│
├── scripts/
│   ├── deploy.js
│   ├── benchmark.js
│   ├── replayDataset.js
│   ├── exportMetrics.js
│   └── verify.js
│
├── test/
│   ├── benchmark.test.js
│   ├── security.test.js
│   ├── oracle.test.js
│   ├── performance.test.js
│   ├── scalability.test.js
│   └── attacks.test.js
│
├── dataset/
│   ├── SmartGridTransactions.csv
│   ├── attackScenarios.json
│   ├── benchmarkConfig.json
│   └── README.md
│
├── analysis/
│   ├── statistics.py
│   ├── gas_analysis.py
│   ├── latency_analysis.py
│   ├── scalability_analysis.py
│   ├── security_analysis.py
│   ├── visualization.py
│   └── generate_figures.py
│
├── results/
│   ├── gas_results.csv
│   ├── latency_results.csv
│   ├── attack_results.csv
│   ├── scalability_results.csv
│   ├── statistical_summary.csv
│   │
│   └── figures/
│         Figure1_Gas.png
│         Figure2_Latency.png
│         Figure3_AttackRate.png
│         Figure4_TPS.png
│
├── docs/
│   ├── methodology.md
│   ├── benchmark_design.md
│   ├── experiment_protocol.md
│   ├── architecture.md
│   └── reviewer_validation_checklist.md
│
├── paper/
│   ├── supplementary_material.pdf
│   ├── reproducibility_checklist.md
│   └── response_mapping.md
│
└── .github/
    └── workflows/
           ci.yml
