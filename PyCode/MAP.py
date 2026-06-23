import random
import numpy as np
import matplotlib.pyplot as plt


class Agent:

    def __init__(self,
                 agent_id,
                 true_cooperation,
                 initial_doubt=5.0,
                 egocentricity=2.0,
                 misattribution_prob=0.0,
                 doubt_step=0.2):

        self.id = agent_id

        # Ground-truth behavior
        self.true_cooperation = true_cooperation

        self.doubt = initial_doubt
        self.E0 = egocentricity

        self.p = misattribution_prob
        self.c = doubt_step

        self.payoff = 0

    def effective_spread(self):

        return self.doubt / self.E0

    def update_doubt(self, success):

        misattribute = random.random() < self.p

        if not misattribute:

            # Normal learning
            if success:
                self.doubt -= self.c
            else:
                self.doubt += self.c

        else:

            # Wrong attribution
            if success:
                self.doubt += self.c
            else:
                self.doubt -= self.c

        self.doubt = max(0.1, min(20, self.doubt))


def interaction(agentA, agentB):

    # Cooperation probability depends on spread
    sigma = agentA.effective_spread()

    estimated_cooperation = (
        agentB.true_cooperation
        + np.random.normal(0, sigma / 10)
    )

    estimated_cooperation = np.clip(
        estimated_cooperation,
        0,
        1
    )

    cooperate = estimated_cooperation > 0.5

    # Ground truth success
    success = cooperate == (
        agentB.true_cooperation > 0.5
    )

    if success:
        agentA.payoff += 1

    agentA.update_doubt(success)


def run_simulation(
        p,
        n_agents=50,
        interactions=1000):

    agents = []

    for i in range(n_agents):

        agents.append(
            Agent(
                i,
                true_cooperation=random.uniform(0, 1),
                initial_doubt=5,
                egocentricity=2,
                misattribution_prob=p
            )
        )

    mean_doubt_history = []

    for t in range(interactions):

        a, b = random.sample(agents, 2)

        interaction(a, b)

        mean_doubt_history.append(
            np.mean(
                [ag.doubt for ag in agents]
            )
        )

    avg_payoff = np.mean(
        [ag.payoff for ag in agents]
    )

    avg_doubt = np.mean(
        [ag.doubt for ag in agents]
    )

    return avg_payoff, avg_doubt, mean_doubt_history


p_values = np.arange(0, 1.01, 0.1)

payoffs = []
doubts = []

for p in p_values:

    payoff, doubt, _ = run_simulation(p)

    payoffs.append(payoff)
    doubts.append(doubt)

    print(
        f"p={p:.1f} | "
        f"Payoff={payoff:.2f} | "
        f"Doubt={doubt:.2f}"
    )


plt.figure(figsize=(8,5))
plt.plot(
    p_values,
    payoffs,
    marker='o'
)

plt.xlabel("Misattribution Probability (p)")
plt.ylabel("Average Payoff")
plt.title("Performance vs Misattribution")
plt.grid(True)
plt.show()


plt.figure(figsize=(8,5))
plt.plot(
    p_values,
    doubts,
    marker='s'
)

plt.xlabel("Misattribution Probability (p)")
plt.ylabel("Average Doubt")
plt.title("Doubt vs Misattribution")
plt.grid(True)
plt.show()