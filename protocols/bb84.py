from numpy import random
import numpy as np

def no_eve(alice_bits, alice_bases, bob_bases):
    """
    Simulates the BB84 protocol without Eve's interference
    Alice prepares random bits and bases, Bob measures in random bases
    When bases match, Bob will measure Alice's bit correctly
    They keep bits where their bases match for the sifted key

    Parameters
    ----------
    alice_bits : list
        List of bits Alice sends (0 or 1)
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

    alice_sifted = []
    bob_sifted = []

    for i in range(len(alice_bits)):

        # If Alice/Bob send/measure in same basis, Bob will measure Alice's bit
        # Bits measured on a matching basis added to the sifted key
        if alice_bases[i] == bob_bases[i]:
            alice_sifted.append(int(alice_bits[i]))
            bob_sifted.append(int(alice_bits[i]))

        # If bases don't match, measurement outcome is random
        # These bits are discarded

    return alice_sifted, bob_sifted

def eve(alice_bits, alice_bases, eve_resend, eve_bases, bob_bases):
    """
    Simulates the BB84 protocol with Eve's interference
    Alice prepares random bits and bases
    Eve intercepts and measures in random bases, resends her measurements to Bob
    Bob measures in random bases
    Alice and Bob again keep the bits where their bases matched
    Randomness introduced by Eve, Bob may not measure Alice's bit correctly

    Parameters
    ----------
    alice_bits : list
        List of bits Alice sends (0 or 1)
    alice_bases : list
        List of bases Alice sends in (0 for Z, 1 for X)
    eve_resend : list
        list of bits Eve measured from Eve to resend to Bob (0 for Z, 1 for X)
    eve_bases : list
        list of bases Eve resends her measured bit to Bob in (0 for Z, 1 for X)
    bob_bases : list
        List of bases Bob measures in (0 for Z, 1 for X)

    Returns
    -------
    alice_sifted : list
        List of bits Alice sent that Bob kept for the sifted key
    bob_sifted : list
        List of bits Bob measured that he kept for the sifted key
    """

    alice_sifted = []
    bob_sifted = []
    bob_bits = []

    for i in range(len(eve_resend)):

        # If sends her bit in same basis as Bob measures, Bob will measure her bit
        if eve_bases[i] == bob_bases[i]:
            bob_bits.append(int(eve_resend[i]))

        # If bases don't match, measurement outcome is random
        else:
            bob_bits.append(random.randint(2))

    for i in range(len(alice_bits)):

        # Bits sent/measured on matching bases are added to the sifted key
        if alice_bases[i] == bob_bases[i]:

            alice_sifted.append(alice_bits[i])
            bob_sifted.append(bob_bits[i])

    return alice_sifted, bob_sifted