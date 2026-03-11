import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# -- Create results directory if it doesn't exist -----
RESULTS_DIR = 'results'
os.makedirs(RESULTS_DIR, exist_ok=True)

def save_plot(filename):
    """
    Saves the current plot to the results directory with the given filename.

    Parameters
    ----------
    filename : str
        The name of the file to save the plot as (e.g., 'plot.png').

    Returns
    -------
    None
    """
    plt.savefig(os.path.join(RESULTS_DIR, filename), dpi=150, bbox_inches='tight')
    plt.show()

def plot_bar_comparison(results, theory):
    """
    Plots a bar comparison of simulated and theoretical values for QBER and SKR.

    Parameters
    ----------
    results : dict
        A dictionary containing the simulation results for each protocol and scenario.
    theory : dict
        A dictionary containing the theoretical values for each protocol and scenario.

    Returns
    -------
    None
    """

    scenarios = list(results.keys())
    qbers = [np.mean(r[0]) for r in results.values()]
    skrs = [np.mean(r[1]) for r in results.values()]
    t_qbers = [theory[s]['QBER'] for s in scenarios]
    t_skrs = [theory[s]['Sifted Key Rate'] for s in scenarios]

    x = np.arange(len(scenarios))
    width = 0.35

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.bar(x - width/2, qbers, width, label='Simulated', color='steelblue')
    ax1.bar(x + width/2, t_qbers, width, label='Theory', color='orange', alpha=0.7)
    ax1.set_title('QBER Comparison')
    ax1.set_ylabel('QBER (%)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios, rotation=15, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)

    ax2.bar(x - width/2, skrs, width, label='Simulated', color='steelblue')
    ax2.bar(x + width/2, t_skrs, width, label='Theory', color='orange')
    ax2.set_title('SKR Comparison')
    ax2.set_ylabel('SKR (%)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenarios, rotation=15, ha='right')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    save_plot('bar_comparison.png')

def plot_cumulative_mean(results, theory):
    """
    Separate plots for each protocol and each case (no Eve / with Eve)

    Parameters
    ----------
    results : dict
        A dictionary containing the simulation results for each protocol and scenario.
    theory : dict
        A dictionary containing the theoretical values for each protocol and scenario.

    Returns
    -------
    None
    """

    # Group scenarios by protocol
    groups = {
        'BB84': ['BB84 without Eve', 'BB84 with Eve'],
        'B92':  ['B92 without Eve',  'B92 with Eve']
    }

    for protocol, scenarios in groups.items():
        for scenario in scenarios:

            if scenario not in results:
                continue

            error_rates, sifted_key_rates, _ = results[scenario]

            cumulative_qber      = pd.Series(error_rates).expanding().mean()
            cumulative_retention = pd.Series(sifted_key_rates).expanding().mean()

            t_qber     = theory[scenario]['QBER']
            t_retention = theory[scenario]['Sifted Key Rate']

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle(f'{scenario} — Cumulative Mean Convergence')

            # QBER convergence
            ax1.plot(cumulative_qber, color='steelblue', label='Simulated')
            ax1.axhline(y=t_qber, color='orange', linestyle='--', label=f'Theory ({t_qber}%)')
            ax1.set_title('QBER')
            ax1.set_xlabel('Iteration')
            ax1.set_ylabel('QBER (%)')
            ax1.legend()
            ax1.grid(alpha=0.3)

            # Sifted Key Rate convergence
            ax2.plot(cumulative_retention, color='steelblue', label='Simulated')
            ax2.axhline(y=t_retention, color='orange', linestyle='--', label=f'Theory ({t_retention}%)')
            ax2.set_title('Sifted Key Retention Rate')
            ax2.set_xlabel('Iteration')
            ax2.set_ylabel('Retention Rate (%)')
            ax2.legend()
            ax2.grid(alpha=0.3)

            plt.tight_layout()

            # Save with scenario name as filename
            filename = f"cumulative_mean_{scenario.lower().replace(' ', '_')}.png"
            save_plot(filename)

def plot_noisy_vs_noiseless(results_clean, results_noisy):

    """
    Plots a side-by-side bar comparison of QBER and SKR for noisy vs noiseless simulations.

    Parameters
    ----------
    results_clean : dict
        A dictionary containing the simulation results for the noiseless scenarios.
    results_noisy : dict
        A dictionary containing the simulation results for the noisy scenarios.

    Returns
    -------
    None
    """

    scenarios = list(results_clean.keys())
    x = np.arange(len(scenarios))
    width = 0.35

    qbers_clean = [np.mean(r[0]) for r in results_clean.values()]
    qbers_noisy = [np.mean(r[0]) for r in results_noisy.values()]
    skrs_clean = [np.mean(r[1]) for r in results_clean.values()]
    skrs_noisy = [np.mean(r[1]) for r in results_noisy.values()]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.bar(x - width/2, qbers_clean, width, label='No Noise', color='steelblue')
    ax1.bar(x + width/2, qbers_noisy, width, label='With Noise', color='orange', alpha=0.7)
    ax1.set_title('QBER: No Noise vs With Noise')
    ax1.set_ylabel('QBER (%)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(scenarios, rotation=15, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)

    ax2.bar(x - width/2, skrs_clean, width, label='No Noise', color='steelblue')
    ax2.bar(x + width/2, skrs_noisy, width, label='With Noise', color='orange')
    ax2.set_title('SKR: No Noise vs With Noise')
    ax2.set_ylabel('SKR (%)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenarios, rotation=15, ha='right')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    save_plot('noisy_vs_noiseless.png')

def plot_noise_sweep(run_bb84, run_b92, bit_size, iterations):

    """
    Plots the convergence of QBER and SKR for different noise levels.

    Parameters
    ----------
    run_bb84 : function
        The function to run the BB84 simulation.
    run_b92 : function
        The function to run the B92 simulation.
    bit_size : int
        The number of bits to simulate for each noise level.
    iterations : int
        The number of iterations to run for each noise level.

    Returns
    -------
    None
    """

    p_errors = np.linspace(0, 0.15, 20)

    bb84_no_eve, bb84_eve = [], []
    b92_no_eve, b92_eve = [], []

    for p in p_errors:

        noise = {'p_prep': p, 'p_meas': p, 'p_eve_prep': 0, 'p_eve_meas': 0}

        bb84_no_eve.append(np.mean(run_bb84(bit_size, iterations, eve=False, noise=noise)[0]))
        bb84_eve.append(np.mean(run_bb84(bit_size, iterations, eve=True, noise=noise)[0]))
        b92_no_eve.append(np.mean(run_b92(bit_size, iterations, eve=False, noise=noise)[0]))
        b92_eve.append(np.mean(run_b92(bit_size, iterations, eve=True, noise=noise)[0]))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for ax, no_eve, eve, title in [
        (ax1, bb84_no_eve, bb84_eve, 'BB84'),
        (ax2, b92_no_eve, b92_eve, 'B92')
    ]:

        ax.plot(p_errors * 100, no_eve, label='No Eve', color='steelblue')
        ax.plot(p_errors * 100, eve, label='With Eve', color='orange')
        ax.axhline(y=11, colour='green', linestyle='--', label='Detection Threshold (11%)')
        ax.fill_between(p_errors * 100, no_eve, 11, where=[q < 11 for q in no_eve], alpha=0.2, color='red', label='Eve undetectable')
        ax.set_title(f'{title}: QBER vs Noise Level')
        ax.set_xlabel('Noise Level (%)')
        ax.set_ylabel('QBER (%)')
        ax.legend()
        ax.grid(alpha=0.3)

    plt.tight_layout()
    save_plot('noise_sweep.png')