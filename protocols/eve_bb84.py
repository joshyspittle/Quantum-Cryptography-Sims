from numpy import random

def intercept(alice_bits, alice_bases, eve_bases):
    """
    Simulates Eve intercepting Alice's bits
    Measures in her own random bases
        Base matches Alice -> perfectly measures Alice's bit
        Bases don't match -> measures random bit
    Whatever she measures, she resends to Bob

    Parameters
    ----------
    alice_bits : list
        list of bits Alice sends to Bob (0 or 1)
    alice_bases : list
        list of bases Alice uses to encode her bits (0 for Z basis, 1 for X basis)
    eve_bases : list
        list of bases Eve uses to measure the bits (0 for Z basis, 1 for X basis)

    Returns
    -------
    eve_resend : list
        list of bits Eve resends to Bob (0 or 1)
    """

    eve_resend = []

    for i in range(len(alice_bits)):

        # If Alice/Eve send/measure in same basis, Eve will measure Alice's bit
        # Bits measured on a matching basis added to the sifted key
        if alice_bases[i] == eve_bases[i]:
            eve_resend.append(int(alice_bits[i]))

        # If bases don't match, measurement outcome is random
        # Eve doesn't know, she will still send this bit
        else:
            eve_resend.append(random.randint(2))

    return eve_resend