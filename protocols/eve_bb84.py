from numpy import random
import utils.utils as utils

def intercept(alice_bits, alice_bases, eve_bases, p_alice_prep=0.0, p_eve_prep=0.0, p_eve_meas=0.0):
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

        prepared_bit = utils.apply_noise(int(alice_bits[i]), p_alice_prep)

        # If Alice/Eve send/measure in same basis, Eve will measure Alice's bit
        # Bits measured on a matching basis added to the sifted key
        if alice_bases[i] == eve_bases[i]:
            measured_bit = utils.apply_noise(prepared_bit, p_eve_meas)

        # If bases don't match, measurement outcome is random
        # Eve doesn't know, she will still send this bit
        else:
            measured_bit = random.randint(2)

        resend_bit = utils.apply_noise(measured_bit, p_eve_prep)
        eve_resend.append(resend_bit)

    return eve_resend