from numpy import random
import numpy as np

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils.utils as utils

def no_eve(alice_bases, bob_bases):
    """
    Simulates the B92 protocol without an eavesdropper

    Alice sends |0> (bit 0) or |+> (bit 1) with equal probability
    Bob measures in Z or X basis with equal probability

    If Bob measures in the same basis as Alice sends, he will measure her bit
    If Bob measures in the opposite basis, he will get a random result
    Only conclusive measurements are kept for the sifted key:
    - Alice sends |0> (bit 0), Bob measures in X
        - Measurement outcome: |+> (bit 0) -> inconclusive -> discard
        - Measurement outcome: |-> (bit 1) -> conclusive -> Alice did not send |-> could only have sent |0> -> 0
    - Alice sends |+> (bit 1), Bob measures in Z
        - Measurement outcome: |0> (bit 0) -> inconclusive -> discard
        - Measurement outcome: |1> (bit 1) -> conclusive -> Alice did not send |1> could only have sent |+> -> 1
    - When both bases match Bob will measure either |0> or |+>
        - These measurements are inconclusive -> discard

    Parameters
    ----------
    alice_bases : list
        List of bases Alice sends in (0 for Z, 1 for X)
    bob_bases : list
        List of bases Bob measures in (0 for Z, 1 for X)

    Returns
    -------
    alice_sifted : list
        List of bits Alice sent that Bob kept for the sifted key
    bob_sifted : list
        List of bits Bob measured that he kept for the sifted key
    """

    bob_sifted = []
    alice_sifted = []

    alice_bases = utils.convert_bits_to_bases(alice_bases)
    bob_bases = utils.convert_bits_to_bases(bob_bases)

    for i in range(len(alice_bases)):

    # Alice sends |0> (bit 0), Bob measures in X -> keep if outcome is |->
        if alice_bases[i] == 'z' and bob_bases[i] == 'x':
            measurement = random.randint(2)
            if measurement == 1:
                bob_sifted.append(0)
                alice_sifted.append(0)

    # Alice sends |+> (bit 1), Bob measures in Z -> keep if outcome is |1>
        if alice_bases[i] == 'x' and bob_bases[i] == 'z':
            measurement = random.randint(2)
            if measurement == 1:
                bob_sifted.append(1)
                alice_sifted.append(1)

    return alice_sifted, bob_sifted

def eve(alice_bases, bob_bases, eve_resend):
    """
    Simulates the B92 protocol with an eavesdropper

    Alice sends |0> (bit 0) or |+> (bit 1) with equal probability
    Eve intercepts Alice's qubits and measures in a random basis
    Eve resends a new qubit to Bob based on her measurement outcome (|0>, |1>, |+>, |->)
    Bob measures in a random basis (Z or X)
    There are more possible outcomes for Bob's measurements when Eve is present
    But only the same conclusive measurements are kept for the sifted key:

    Parameters
    ----------
    alice_bases : list
        List of bases Alice sends in (0 for Z, 1 for X)
    bob_bases : list
        List of bases Bob measures in (0 for Z, 1 for X)
    eve_resend : list
        List of states Eve resends to Bob based on her measurements (|0>, |1>, |+>, |->)

    Returns
    -------
    alice_sifted : list
        List of bits Alice sent that Bob kept for the sifted key
    bob_sifted : list
        List of bits Bob measured that he kept for the sifted key
    """

    # Bits Bob will keep and their index
    bob_sifted = []
    kept_bits = []

    for i in range(len(eve_resend)):

        # Bob measures in X basis
        if bob_bases[i] == 1:
            if eve_resend[i] == 0:
                # Eve sends |0> (orthogonal to Bob) -> random |+> or |->
                measurement = random.randint(2)
                if measurement == 1:
                    # Bob measures |-> -> concludes Alice sent |0>
                    bob_sifted.append(0)
                    kept_bits.append(i)
            elif eve_resend[i] == '-':
                # Eve sends |-> (matching Bob) -> measures |-> -> concludes |0>
                bob_sifted.append(0)
                kept_bits.append(i)
            elif eve_resend[i] == 1:
                # Eve sends |1> (orthogonal to Bob) -> random |+> or |->
                measurement = random.randint(2)
                if measurement == 1:
                    # Bob measures |-> -> concludes Alice sent |0>
                    bob_sifted.append(0)
                    kept_bits.append(i)
            # Eve sends |+> -> Bob measures |+> -> always discarded

        # Bob measures in Z basis
        elif bob_bases[i] == 0:
            if eve_resend[i] == '+':
                # Eve sends |+> (orthogonal to Bob) -> random |0> or |1>
                measurement = random.randint(2)
                if measurement == 1:
                    # Bob measures |1> -> concludes Alice sent |+>
                    bob_sifted.append(1)
                    kept_bits.append(i)
            elif eve_resend[i] == 1:
                # Eve sends |1> (matching Bob) -> measures |1> -> concludes |+>
                bob_sifted.append(1)
                kept_bits.append(i)
            elif eve_resend[i] == '-':
                # Eve sends |-> (orthogonal to Bob) -> random |0> or |1>
                measurement = random.randint(2)
                if measurement == 1:
                    # Bob measures |1> -> concludes Alice sent |+>
                    bob_sifted.append(1)
                    kept_bits.append(i)
            # Eve sends |0> -> Bob measures |0> -> always discarded

    # Get Alice's sifted key
    alice_sifted = []

    for i in range(len(bob_sifted)):
        alice_sifted.append(alice_bases[kept_bits[i]])

    return alice_sifted, bob_sifted