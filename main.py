from runner import run_b92, run_bb84
from visualisation import (
    plot_bar_comparison,
    plot_cumulative_mean,
    plot_noisy_vs_noiseless,
    plot_noise_sweep
)
import matplotlib.pyplot as plt
import numpy as np

# -- Configuration -----
BIT_SIZE = 1000
ITERATIONS = 1000

THEORY = {
    'B92 without Eve': {'QBER': 0.0, 'Sifted Key Rate': 25.0},
    'B92 with Eve': {'QBER': 33.3, 'Sifted Key Rate': 37.5},
    'BB84 without Eve': {'QBER': 0.0, 'Sifted Key Rate': 50.0},
    'BB84 with Eve': {'QBER': 25.0, 'Sifted Key Rate': 50.0}
}

# -- Run Sims ---------
results = {
    'B92 without Eve': run_b92(BIT_SIZE, ITERATIONS, eve=False),
    'B92 with Eve': run_b92(BIT_SIZE, ITERATIONS, eve=True),
    'BB84 without Eve': run_bb84(BIT_SIZE, ITERATIONS, eve=False),
    'BB84 with Eve': run_bb84(BIT_SIZE, ITERATIONS, eve=True)
}

# -- Print Results -----
print(f"\n{'Scenario':20} {'QBER (%)':>10} {'Sifted Key Rate (%)':>15} {'Theory QBER':>12} {'Theory SKR':>12} {'QBER Dev':>10} {'SKR Dev':>10}")
print("-" * 95)

for scenario, (error_rates, sifted_key_rates, matching_bits_list) in results.items():

    avg_qber = np.mean(error_rates)
    avg_skr = np.mean(sifted_key_rates)

    theory_qber = THEORY[scenario]['QBER']
    theory_skr = THEORY[scenario]['Sifted Key Rate']

    qber_dev = avg_qber - theory_qber
    skr_dev = avg_skr - theory_skr

    print(f"{scenario:20} {avg_qber:10.2f} {avg_skr:15.2f} {theory_qber:12.2f} {theory_skr:12.2f} {qber_dev:10.2f} {skr_dev:10.2f}")

# -- Plotting ---------
print("\nGenerating plots...")

plot_bar_comparison(results, THEORY)
plot_cumulative_mean(results, THEORY)
#plot_noisy_vs_noiseless(results, results)  # Placeholder for noisy vs noiseless
#plot_noise_sweep(run_bb84, run_b92, BIT_SIZE, ITERATIONS)

#error_rates, sifted_key_rates, matching_bits_list = run_b92(bit_size=1000, iterations=100, eve=True)

#print(f"Average Error Rate: {np.mean(error_rates):.2f}%")
#print(f"Average Sifted Key Rate: {np.mean(sifted_key_rates):.2f}%")
#print(f"Average Matching Bits: {np.mean(matching_bits_list)}")

#error_rates, sifted_key_rates, matching_bits_list = run_bb84(bit_size=1000, iterations=100, eve=False)

#print(f"Average Error Rate: {np.mean(error_rates):.2f}%")
#print(f"Average Sifted Key Rate: {np.mean(sifted_key_rates):.2f}%")
#print(f"Average Matching Bits: {np.mean(matching_bits_list)}")