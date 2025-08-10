# Mercor Challenge: Referral Network

This coding challenge implements the core logic for a referral network, progressing from data structure design to algorithmic analysis and simulation. The project is divided into five parts that build upon each other.

## Language & Setup

- **Language**: Python 3.8+
- **Dependencies**: No external dependencies required (uses only Python standard library)
- **Testing Framework**: pytest 8.4.1+

### Installation & Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd referral-network

# Create and activate virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install testing dependencies
pip install -r requirements.txt
```

**Note**: Python 3.8+ is required. The virtual environment ensures clean dependency management.

## Running Tests

```bash
# Run the entire test suite
python -m pytest tests/ -v

# Run specific test parts
python -m pytest tests/test_part1_core_structure.py -v
python -m pytest tests/test_part2_business_rules.py -v
python -m pytest tests/test_part3_influencer_identification.py -v
python -m pytest tests/test_part4_network_simulation.py -v
python -m pytest tests/test_part5_bonus_optimization.py -v
```

**Important**: Always ensure your virtual environment is activated before running tests or the demo.

## Running the Demo

```bash
# Run the comprehensive demonstration
python demo.py
```

## Time to Complete

**Total Time Spent**: Approximately **12-15 hours** over 3-4 days

**Breakdown by Part:**
- **Part 1 (Core Structure)**: ~3 hours - Data structure design, constraint implementation, basic testing
- **Part 2 (Network Reach)**: ~2 hours - BFS implementation, top referrers algorithm
- **Part 3 (Influencer Identification)**: ~4 hours - Unique reach expansion, flow centrality algorithms
- **Part 4 (Network Simulation)**: ~2 hours - Growth simulation, days calculation
- **Part 5 (Bonus Optimization)**: ~2 hours - Binary search implementation, optimization logic
- **Testing & Documentation**: ~2 hours - Comprehensive test suite, README documentation

**Development Approach**: Iterative development with continuous testing and refinement. Each part was implemented, tested, and documented before moving to the next, ensuring a solid foundation for subsequent features.

## Project Structure

```
referral-network/
├── README.md                    # This file - complete project documentation
├── .gitignore                   # Python gitignore patterns
├── requirements.txt             # Project dependencies
├── demo.py                      # Comprehensive functionality demonstration
├── source/                      # Core source code
│   ├── __init__.py             # Package initialization
│   ├── core/                   # Core business logic
│   │   ├── __init__.py         # Core package initialization
│   │   ├── referral_network.py # Parts 1-3: Core referral network and analysis
│   │   └── simulation.py       # Parts 4-5: Network growth simulation and bonus optimization
│   ├── models/                 # Data models
│   │   ├── __init__.py         # Models package initialization
│   │   └── user.py             # User model with referral tracking
│   ├── constraints/            # Business rule enforcement
│   │   ├── __init__.py         # Constraints package initialization
│   │   └── validator.py        # Referral validation and constraint checking
│   ├── algorithms/             # Advanced algorithms
│   │   ├── __init__.py         # Algorithms package initialization
│   │   ├── network_analysis.py # Network analysis algorithms
│   │   └── reach_expansion.py  # Unique reach expansion algorithms
│   └── examples/               # Example implementations
│       ├── __init__.py         # Examples package initialization
│       └── adoption_functions.py # Adoption probability functions
└── tests/                      # Comprehensive test suite
    ├── __init__.py             # Tests package initialization
    ├── test_part1_core_structure.py      # Tests for Parts 1-3
    ├── test_part2_business_rules.py      # Tests for business rule enforcement
    ├── test_part3_influencer_identification.py # Tests for influencer algorithms
    ├── test_part4_network_simulation.py  # Tests for simulation functionality
    └── test_part5_bonus_optimization.py  # Tests for bonus optimization
```

## Design Choices

### Data Structure Design (Part 1)

I chose to implement the referral network using an **adjacency list representation** with the following design decisions:

1. **Graph Representation**: Used an adjacency list (`dict[int, set[int]]`) where keys are user IDs and values are sets of direct referral IDs. This provides O(1) lookup for direct referrals and efficient iteration.

2. **User Management**: Maintained a separate set of all users for O(1) existence checks and efficient user enumeration.

3. **Constraint Enforcement**: 
   - **No Self-Referrals**: Checked in `add_referral()` method using user ID comparison
   - **Unique Referrer**: Used a reverse mapping (`referrer_map`) to track who referred each user, ensuring O(1) constraint validation
   - **Acyclic Graph**: Implemented cycle detection using DFS with path tracking, preventing any circular referral chains

4. **API Design**: Chose method names that clearly express intent (`add_referral`, `get_direct_referrals`, `get_total_referrals`) and return types that are intuitive (sets for referrals, integers for counts).

### Algorithm Choices

1. **BFS for Reach Calculation (Part 2)**: Chose BFS over DFS for calculating total referrals as it naturally processes nodes level by level, making it easier to understand and debug. Time complexity: O(V + E).

2. **Greedy Algorithm for Unique Reach (Part 3)**: Implemented the greedy approach as specified, which provides a good approximation for the NP-hard set cover problem. Time complexity: O(V²).

3. **All-Pairs Shortest Path for Flow Centrality (Part 3)**: Used BFS from each node to compute shortest distances, then applied the mathematical property that a node v lies on a shortest path between s and t if `dist(s, v) + dist(v, t) == dist(s, t)`. Time complexity: O(V³).

4. **Binary Search for Bonus Optimization (Part 5)**: Used binary search over the bonus space to efficiently find the minimum required bonus, leveraging the monotonic nature of the adoption probability function. Time complexity: O(log B) where B is the bonus range.

## Implementation Details by Part

**Part 1: Core Referral Network**
- **Graph Representation**: Adjacency list with O(1) direct referral lookup
- **Constraint Enforcement**: Self-referral prevention, unique referrer validation, acyclic graph maintenance
- **API Design**: Intuitive method names and return types

**Part 2: Full Network Reach**
- **Top Referrers Selection**: The `get_top_referrers(k)` method returns the top k referrers based on total referral count. **How to pick appropriate k**: 
  - For **small networks** (< 100 users): Use k = 5-10 to identify key influencers
  - For **medium networks** (100-1000 users): Use k = 10-20 for broader coverage
  - For **large networks** (> 1000 users): Use k = 20-50 to capture significant referrers
  - **Business rule**: k should be proportional to network size, typically 5-10% of total users

**Part 3: Identify Influencers**
- **Unique Reach Expansion**: Greedy algorithm for minimizing audience overlap
- **Flow Centrality Implementation**: The flow centrality algorithm follows the assignment specification exactly:
  1. Pre-compute shortest distances between all pairs using BFS from every node
  2. For each combination of source s, target t, and potential broker v:
  3. Check if `dist(s, v) + dist(v, t) == dist(s, t)` 
  4. If true, increment v's centrality score
  5. This identifies users who lie on the most shortest paths between other users

**Part 4: Network Growth Simulation**
- **Simulation Parameters**: The simulation uses fixed parameters as specified in the assignment:
  - **Initial Referrers**: 100 active referrers at start
  - **Referral Capacity**: Each referrer can make up to 10 successful referrals before becoming inactive
  - **Time Unit**: Discrete steps called "days"
  - **Probability Model**: Each active referrer has probability p of making a successful referral each day

**Part 5: Referral Bonus Optimization**
- **Binary Search Approach**: Efficiently finds minimum bonus using monotonic property of adoption probability function
- **Key Constraint**: Bonus must be in $10 increments as specified in assignment

## Required Functions Implementation

**Part 4: Network Growth Simulation**
- **`simulate(p: float, days: int) -> List[int]`**: Returns cumulative expected referrals for each day
  - Input: probability p of successful referral per day, number of days to simulate
  - Output: List where index i contains total referrals by end of day i
  - Implementation: Tracks active referrers and their remaining capacity, simulates daily referral attempts

- **`days_to_target(p: float, target_total: int) -> int`**: Calculates minimum days to reach target
  - Input: probability p, target total referrals
  - Output: Minimum days required to meet or exceed target
  - Implementation: Uses binary search over days to efficiently find the minimum required

**Part 5: Referral Bonus Optimization**
- **`min_bonus_for_target(days: int, target_hires: int, adoption_prob: Callable, eps: float = 1e-3) -> Optional[int]`**: Finds minimum bonus for target
  - Input: days available, target hires, adoption probability function, precision epsilon
  - Output: Minimum bonus (rounded up to nearest $10) or None if unachievable
  - Implementation: Binary search over bonus space (0 to max_bonus) using simulation results
  - **Key Constraint**: Bonus must be in $10 increments as specified in assignment

## Influence Metrics Comparison (Part 3)

The implementation provides three different metrics for identifying important users in the network, each suited for different business scenarios:

1. **Reach (Total Referral Count)**: 
   - **What it measures**: The total number of users in a referrer's downstream network
   - **Business scenario**: Best for **volume-based campaigns** where you want to maximize the number of people reached. For example, when launching a new product and you need to spread awareness to as many potential customers as possible.
   - **Limitation**: May overvalue users who have many referrals but low-quality connections

2. **Unique Reach Expansion**:
   - **What it measures**: The number of unique users covered by a set of referrers, minimizing overlap
   - **Business scenario**: Ideal for **budget optimization** when you have limited resources and want to maximize coverage without redundancy. For example, when selecting a group of influencers for a marketing campaign where you want to reach the maximum number of unique people.
   - **Limitation**: Greedy approach may not always find the globally optimal solution

3. **Flow Centrality**:
   - **What it measures**: How critical a user is as a "broker" connecting different parts of the network
   - **Business scenario**: Perfect for **network resilience planning** and identifying key personnel whose departure could fragment the organization. For example, when planning succession or identifying employees who should receive additional training to maintain network connectivity.
   - **Limitation**: Computationally expensive for large networks

## Time Complexity Analysis for Bonus Optimization (Part 5)

The `min_bonus_for_target` function uses a **binary search approach** over the bonus space:

- **Time Complexity**: O(log B × D × V) where:
  - B = bonus range (typically 0 to some maximum bonus amount)
  - D = number of days for simulation
  - V = number of users in the network

- **Space Complexity**: O(V) for storing the network state during simulation

- **Why Binary Search**: Since the adoption probability function is monotonically increasing, we can use binary search to efficiently find the minimum bonus that achieves the target. This is much more efficient than linear search, especially when the bonus range is large.

- **Optimization**: The function pre-computes the network structure once and reuses it for each simulation, avoiding redundant graph construction.

## AI Usage Acknowledgment

This project was developed with assistance from some AI tools like ChatGPT for:
- Debugging assistance during implementation
- Code review and optimization suggestions
- Test case generation and validation
- Documentation improvements

**All core algorithms, data structure decisions, and business logic were designed and implemented by me.** The AI served as a collaborative coding partner to help refine the implementation, catch potential issues, and ensure comprehensive test coverage. I own the complete solution and can explain every design choice and implementation detail.
