from numpy import random

def intercept(alice_bases, eve_bases):
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

        # Alice sends |0> (bit 0)
        if alice_bases[i] == 0:
            if eve_bases[i] == 0:
                # Eve measures in Z basis (matching Alice) -> measures |0>
                eve_resend.append(0)
            else:
                # Eve measures in X basis (orthogonal to Alice) -> random |+> or |->
                measurement = random.randint(2)
                if measurement == 0:
                    eve_resend.append('+')
                else:
                    eve_resend.append('-')

        # Alice sends |+> (bit 1)
        elif alice_bases[i] == 1:
            if eve_bases[i] == 1:
                # Eve measures in X basis (matching Alice) -> measures |+>
                eve_resend.append('+')
            else:
                # Eve measures in Z basis (orthogonal to Alice) -> random |0> or |1>
                measurement = random.randint(2)
                if measurement == 0:
                    eve_resend.append(0)
                else:
                    eve_resend.append(1)

    return eve_resend