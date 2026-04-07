# Quantum Cryptography Simulations

Simulation of the **BB84** and **B92** quantum key distribution (QKD) protocols, 
developed as an extension to a third-year optics laboratory on quantum cryptography. 
Implements both protocols with and without an eavesdropper (Eve), and models the 
effect of optical noise on key distribution security.

---

## Protocols

### BB84
Proposed by Bennett and Brassard in 1984, BB84 uses four polarisation states across 
two bases (rectilinear and diagonal) to distribute a secret key. Alice and Bob retain 
only bits where they used the same basis, giving a theoretical sifted key rate of 50%. 
Eve's presence introduces a 25% QBER, well above the 11% detection threshold.

### B92
Proposed by Bennett in 1992, B92 simplifies BB84 by using only two non-orthogonal 
states. Only conclusive measurements are kept, giving a theoretical sifted key rate 
of 25%. Eve's intercept-resend attack introduces a ~33% QBER and anomalously raises 
the sifted key rate to ~37.5%, both of which signal her presence.

---

## Results

| Scenario | QBER (%) | Sifted Key Rate (%) | Theory QBER (%) | Theory SKR (%) | QBER Deviation | SKR Deviation |
|---|---|---|---|---|---|---|
| B92 without Eve  | 0.00  | 24.99 | 0.00  | 25.00 | 0.00 | 0.01 |
| B92 with Eve     | 33.30 | 37.47 | 33.00 | 37.50 | 0.30 | 0.03 |
| BB84 without Eve | 0.00  | 50.00 | 0.00  | 50.00 | 0.00 | 0.00 |
| BB84 with Eve    | 25.02 | 49.95 | 25.00 | 50.00 | 0.02 | 0.05 |

### Cumulative Mean Convergence

<p align="center">
  <img src="https://github.com/user-attachments/assets/e7d5942a-d25c-44cf-b6df-78c30ec90a82" width="48%"/>
  <img src="https://github.com/user-attachments/assets/324413e4-a328-477f-8674-0219af305476" width="48%"/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/59b62561-3b78-41c5-9b48-d3ee401488f5" width="48%"/>
  <img src="https://github.com/user-attachments/assets/0ae4bc3e-e2e5-4dcc-8614-11fb87f26b50" width="48%"/>
</p>

### Protocol Comparison

<p align="center">
  <img src="https://github.com/user-attachments/assets/446d67a9-2085-4493-992f-741012c72ce3" width="80%"/>
</p>

---

## Project Structure
```
quantum-cryptography-sims/
├── protocols/
│   ├── bb84.py          # BB84 protocol — no Eve and with Eve
│   ├── b92.py           # B92 protocol — no Eve and with Eve
│   ├── eve_bb84.py      # Eve's intercept-resend attack on BB84
│   └── eve_b92.py       # Eve's intercept-resend attack on B92
├── utils/
│   └── utils.py         # Shared helper functions
├── visualisation/
│   └── plots.py         # All plotting functions
├── runner.py            # Orchestrates simulations
├── main.py              # Entry point — configure and run
└── requirements.txt
```

---

## Usage

Clone the repository and install dependencies:
```bash
git clone https://github.com/yourusername/quantum-cryptography-sims.git
cd quantum-cryptography-sims
pip install -r requirements.txt
```

Run the simulation:
```bash
python main.py
```

Simulation parameters can be configured at the top of `main.py`:
```python
BIT_SIZE   = 10000    # number of qubits per simulation
ITERATIONS = 100      # number of iterations to average over
NOISE = {
    'p_prep':     0.03,   # state preparation error
    'p_meas':     0.03,   # measurement error
    'p_eve_meas': 0.03,   # Eve's measurement error
    'p_eve_prep': 0.03    # Eve's state preparation error
}
```

---

## References

- Bennett, C. H. (1992). *Quantum cryptography using any two nonorthogonal states*. Physical Review Letters.
- Bennett, C. H., & Brassard, G. (1984). *Quantum cryptography: Public key distribution and coin tossing*.
- Fox, M. (2006). *Quantum Optics: An Introduction*. Oxford University Press.
