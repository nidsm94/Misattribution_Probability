import random
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class Agent:
    def __init__(self, agent_id: int, true_cooperation: float, misattribution_prob: float):
        self.id = agent_id
        self.true_cooperation = true_cooperation
        self.p = misattribution_prob
        
        # Hardcoded hyper-parameters grouped or defaulted cleanly
        self.doubt = 5.0
        self.egocentricity = 2.0
        self.doubt_step = 0.2
        self.payoff = 0

    @property
    def effective_spread(self) -> float:
        """Returns the perception noise scaling factor."""
        return self.doubt / self.egocentricity

    def perceive_cooperation(self, target_cooperation: float) -> bool:
        """Estimates if another agent will cooperate based on current doubt."""
        sigma = self.effective_spread
        noise = np.random.normal(0, sigma / 10)
        estimated_val = np.clip(target_cooperation + noise, 0, 1)
        return estimated_val > 0.5

    def update_doubt(self, success: bool):
        """Updates internal doubt model, factoring in misattribution bias."""
        misattribute = random.random() < self.p
        # If misattributed, invert the success signal
        effective_success = not success if misattribute else success
        
        self.doubt += -self.doubt_step if effective_success else self.doubt_step
        self.doubt = np.clip(self.doubt, 0.1, 20.0)


def execute_interaction(agent_a: Agent, agent_b: Agent):
    """Executes a symmetric interaction where both agents learn from each other."""
    # Intentions
    a_expects_cooperation = agent_a.perceive_cooperation(agent_b.true_cooperation)
    b_expects_cooperation = agent_b.perceive_cooperation(agent_a.true_cooperation)
    
    # Ground truth actual actions
    a_actually_cooperates = agent_a.true_cooperation > 0.5
    b_actually_cooperates = agent_b.true_cooperation > 0.5
    
    # Success definition: did reality match my expectation?
    a_success = a_expects_cooperation == b_actually_cooperates
    b_success = b_expects_cooperation == a_actually_cooperates
    
    if a_success: agent_a.payoff += 1
    if b_success: agent_b.payoff += 1
        
    agent_a.update_doubt(a_success)
    agent_b.update_doubt(b_success)


def run_simulation(p: float, n_agents: int = 50, steps: int = 2000) -> Tuple[float, float]:
    """Runs the agent network simulation for a given misattribution probability."""
    agents = [Agent(i, random.uniform(0, 1), p) for i in range(n_agents)]
    
    for _ in range(steps):
        a, b = random.sample(agents, 2)
        execute_interaction(a, b)
        
    avg_payoff = np.mean([ag.payoff for ag in agents])
    avg_doubt = np.mean([ag.doubt for ag in agents])
    return float(avg_payoff), float(avg_doubt)


# ==========================================
# SIMULATION EXECUTION & PLOTTING
# ==========================================
if __name__ == "__main__":
    # Ensure reproducible results
    random.seed(42)
    np.random.seed(42)

    # Generate misattribution probabilities from 0.0 to 1.0
    p_values = np.arange(0, 1.01, 0.1)
    payoffs = []
    doubts = []

    # Run simulations
    print("Running simulations across misattribution spectrum...")
    for p in p_values:
        payoff, doubt = run_simulation(p)
        payoffs.append(payoff)
        doubts.append(doubt)
        print(f"p={p:.1f} | Payoff={payoff:.2f} | Doubt={doubt:.2f}")

    # Create layout with two distinct subplots side-by-side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Left Graph: Performance (Payoffs)
    ax1.plot(p_values, payoffs, marker='o', color='#1f77b4', linewidth=2)
    ax1.set_xlabel("Misattribution Probability (p)", fontsize=11)
    ax1.set_ylabel("Average Systemic Payoff", fontsize=11)
    ax1.set_title("System Performance vs. Misattribution", fontsize=12, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Right Graph: Cognitive Model (Doubt)
    ax2.plot(p_values, doubts, marker='s', color='#d62728', linewidth=2)
    ax2.set_xlabel("Misattribution Probability (p)", fontsize=11)
    ax2.set_ylabel("Average Agent Doubt", fontsize=11)
    ax2.set_title("Systemic Doubt vs. Misattribution", fontsize=12, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()