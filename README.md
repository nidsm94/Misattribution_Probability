# Misattribution_Probability

Normal adaptation AAMAS-19 – no misattribution (μ = 0).
Misattribution model – sweep μ from 0 to 1 and compared against the Normal Adaption.

The output contains four graphs:

Graph 1: Normal behaviour (doubt vs interactions)
Observations: With Succesful   interactions doubt decreases.
Graph 2: Misattribution behaviour for μ = 0, 0.2, 0.5, 0.8, 1.0
Observations: Misattribution Probability is included - m<0.5 - m=0.0, 0.2 - Agents learns mostly correctly, doubt decreases, confidence increases similar to AAMAS 19
m=0.5 - Agents is correct half the time and wrong half the time, doubt increases randomly
m >0.5 - m=0.8 - Agents is wrong more often than right, doubt increases even when the agent is successful.
Agents becomes less confident even after successful interactions/ repeated success.
m=1.0 - Every outcome is interpreted incorrectly, so the adaptation is completely inverted.
Graph 3: Average doubt after simulation vs μ
Graph 4: Difference between expected doubt (normal) and actual doubt (misattribution)

