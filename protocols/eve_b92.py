from numpy import random
import utils.utils as utils

def intercept(alice_bases, eve_bases, p_alice_prep=0.0, p_eve_prep=0.0, p_eve_meas=0.0):
    """
    Simulates Eve intercepting Alice's qubits
    Measures them in her own random bases
    Eve then resends the qubits to Bob based on her measurement outcomes

    Alice sends |0> (bit 0):
        - Eve measures in Z basis -> measures |0> -> resends |0>
        - Eve measures in X basis -> random |+> or |-> -> resends that state
    Alice sends |+> (bit 1):
        - Eve measures in X basis -> measures |+> -> resends |+>
        - Eve measures in Z basis -> random |0> or |1> -> resends that state

    Parameters
    ----------
    alice_bases : list
        List of bases Alice sends in (0 for Z, 1 for X)
    eve_bases : list
        List of bases Eve measures in (0 for Z, 1 for X)

    Returns
    -------
    eve_resend : list
        List of states Eve resends to Bob based on her measurements
    """

    eve_resend = []

    for i in range(len(alice_bases)):

        prepared_state = utils.apply_noise(alice_bases[i], p_alice_prep)

        # Alice sends |0> (bit 0)
        if prepared_state == 0:
            if eve_bases[i] == 0:
                # Eve measures in Z basis (matching Alice) -> measures |0>
                measured_state = utils.apply_noise(0, p_eve_meas)
            else:
                # Eve measures in X basis (orthogonal to Alice) -> random |+> or |->
                measurement = random.randint(2)
                if measurement == 0:
                    measured_state = '+'
                else:
                    measured_state = '-'

        # Alice sends |+> (bit 1)
        elif prepared_state == 1:
            if eve_bases[i] == 1:
                # Eve measures in X basis (matching Alice) -> measures |+>
                measured_state = utils.apply_noise('+', p_eve_meas)
            else:
                # Eve measures in Z basis (orthogonal to Alice) -> random |0> or |1>
                measurement = random.randint(2)
                if measurement == 0:
                    measured_state = 0
                else:
                    measured_state = 1

        resend_state = utils.apply_noise(measured_state, p_eve_prep)
        eve_resend.append(resend_state)

    return eve_resend