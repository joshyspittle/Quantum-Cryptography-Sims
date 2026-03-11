from numpy import random

def prepare_bits_and_bases(bit_size, eve=False):
    """
    Generates random bits and bases for Alice, Bob, and optionally Eve.

    Parameters
    ----------
    bit_size : int
        The number of bits to generate for the simulation
    eve : bool, optional
        Whether to prepare bases for Eve (default is False)

    Returns
    -------
    If eve is False:
        alice_bits : numpy.ndarray
        alice_bases : numpy.ndarray
        bob_bases : numpy.ndarray
    If eve is True:
        alice_bits : numpy.ndarray
        alice_bases : numpy.ndarray
        bob_bases : numpy.ndarray
        eve_bases : numpy.ndarray
    """

    # Alice prepares random bits and bases
    alice_bits = random.randint(2, size=bit_size)
    alice_bases = random.randint(2, size=bit_size)

    # Bob prepares random bases
    bob_bases = random.randint(2, size=bit_size)

    if eve:
        # Eve prepares random bases
        eve_bases = random.randint(2, size=bit_size)
        return alice_bits, alice_bases, bob_bases, eve_bases

    return alice_bits, alice_bases, bob_bases

def convert_bits_to_bases(bits):
    """
    Converts an array of bits (0s and 1s) to corresponding bases
    'z': 0
    'x': 1

    Parameters    
    ----------
    bits : numpy.ndarray
        An array of bits (0s and 1s)

    Returns
    -------
    bases : list of str
        A list of bases corresponding to the input bits
    """

    bases = []
    for i in range(len(bits)):
        if bits[i] == 0:
            bases.append('z')
        else:
            bases.append('x')

    return bases

def calculate_error_rate(alice_bits, bob_bits):
    """
    Calculates the Quantum Bit Error Rate (QBER) between Alice's and Bob's sifted keys
    Number of mismatches divided by total sifted bits, expressed as a percentage

    Parameters
    ----------
    alice_bits : list or numpy.ndarray
        The sifted bits that Alice has after the protocol execution
    bob_bits : list or numpy.ndarray
        The sifted bits that Bob has after the protocol execution

    Returns
    -------
    error_rate : float
        The Quantum Bit Error Rate (QBER) as a percentage
    """

    if len(alice_bits) == 0:
        return 0

    errors = 0
    for i in range(len(alice_bits)):
        if alice_bits[i] != bob_bits[i]:
            errors += 1

    error_rate = errors / len(alice_bits) * 100

    return error_rate

def calculate_sifted_key_rate(bob_bits, bit_size):
    """
    Calculates the Sifted Key Rate as the percentage of bits that Bob has 
    after sifting compared to the original number of bits sent by Alice

    Parameters
    ----------
    bob_bits : list or numpy.ndarray
        The sifted bits that Bob has after the protocol execution
    bit_size : int
        The original number of bits sent by Alice

    Returns
    -------
    sifted_key_rate : float
        The Sifted Key Rate as a percentage
    """

    if bit_size == 0:
        return 0

    sifted_key_rate = len(bob_bits) / bit_size * 100

    return sifted_key_rate