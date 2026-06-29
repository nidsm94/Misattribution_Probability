import numpy as np
import matplotlib.pyplot as plt

num_interactions = 50
initial_doubt = 1.0
threshold = 0.6
step = 0.05

# probability that interaction succeeds
# p > 0.5 means agent succeeds more often
success_probability = 0.9

mis_values = [0.0,0.2,0.5,0.8,1.0]

def simulate_normal():

    doubt = initial_doubt

    history = [doubt]

    for t in range(num_interactions):

        success = np.random.rand() < success_probability

        if success:

            doubt = max(0,doubt-step)

        else:

            doubt += step

        history.append(doubt)

    return np.array(history)

def simulate_misattribution(mu):

    doubt = initial_doubt

    history = [doubt]

    for t in range(num_interactions):

        success = np.random.rand() < success_probability

        mis = np.random.rand() < mu

        if success:

            if mis:
                # success interpreted as failure
                doubt += step
            else:
                doubt = max(0,doubt-step)

        else:

            if mis:
                # failure interpreted as success
                doubt = max(0,doubt-step)
            else:
                doubt += step

        history.append(doubt)

    return np.array(history)

normal = simulate_normal()


results = {}

for mu in mis_values:

    results[mu] = simulate_misattribution(mu)

plt.figure(figsize=(8,5))

plt.plot(normal,
         linewidth=3,
         label="Normal Behaviour")

plt.title("Normal Doubt Adaptation")

plt.xlabel("Interactions")

plt.ylabel("Doubt")

plt.grid()

plt.legend()

plt.show()


plt.figure(figsize=(10,6))

plt.plot(normal,
         linewidth=3,
         color="black",
         label="Expected Behaviour")

for mu in mis_values:

    plt.plot(results[mu],
             label=f"μ={mu}")

plt.title("Effect of Misattribution on Doubt")

plt.xlabel("Interactions")

plt.ylabel("Doubt")

plt.legend()

plt.grid()

plt.show()


avg_doubt = []

for mu in mis_values:

    avg_doubt.append(np.mean(results[mu]))

plt.figure(figsize=(8,5))

plt.plot(mis_values,
         avg_doubt,
         'o-',
         linewidth=3)

plt.axvline(0.5,
            linestyle='--',
            color='red',
            label='Critical μ=0.5')

plt.xlabel("Misattribution Probability μ")

plt.ylabel("Average Doubt")

plt.title("Average Doubt vs Misattribution")

plt.grid()

plt.legend()

plt.show()

# -----------------------------
# GRAPH 4
# -----------------------------

expected = np.mean(normal)

difference = [np.mean(results[mu])-expected
              for mu in mis_values]

plt.figure(figsize=(8,5))

plt.bar([str(m) for m in mis_values],
        difference)

plt.axhline(0,color='black')

plt.xlabel("Misattribution Probability μ")

plt.ylabel("Deviation from Expected Doubt")

plt.title("Deviation from Normal Behaviour")

plt.grid()

plt.show()

# -----------------------------
# PRINT RESULTS
# -----------------------------

print("\nAverage Doubt\n")

for mu in mis_values:

    print(f"μ = {mu:.1f}  -->  {np.mean(results[mu]):.3f}")