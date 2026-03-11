from numpy import random
import numpy as np
import protocols.b92 as b92
import protocols.eve_b92 as eve_b92
import protocols.bb84 as bb84
import protocols.eve_bb84 as eve_bb84
import utils.utils as utils

def _run_simulation(bit_size, iterations, eve, no_eve_fn, eve_fn, intercept_fn=None):
    """
    Runs the specified quantum key distribution simulation for a given number of iterations and bit size

    Parameters
    ----------
    bit_size : int
        The number of bits to simulate in each iteration
    iterations : int
        The number of iterations to run the simulation for
    eve : bool
        Whether to include Eve in the simulation
    no_eve_fn : function
        The function to run when Eve is not included
    eve_fn : function
        The function to run when Eve is included
    intercept_fn : function, optional
        The function to simulate Eve's interception

    Returns
    -------
    error_rates : list of float
        The list of error rates for each iteration
    sifted_key_rates : list of float
        The list of sifted key rates for each iteration
    matching_bits_list : list of int
        The list of matching bits for each iteration
    """

    error_rates = []
    sifted_key_rates = []
    matching_bits_list = []

    for _ in range(iterations):

        if eve:
            alice_bits, alice_bases, bob_bases, eve_bases = utils.prepare_bits_and_bases(bit_size, eve)
            eve_resend = intercept_fn(alice_bits, alice_bases, eve_bases)
            alice_sifted, bob_sifted = eve_fn(alice_bits, alice_bases, eve_resend, eve_bases, bob_bases)

        else:
            alice_bits, alice_bases, bob_bases = utils.prepare_bits_and_bases(bit_size)
            alice_sifted, bob_sifted = no_eve_fn(alice_bits, alice_bases, bob_bases)

        error_rates.append(utils.calculate_error_rate(alice_sifted, bob_sifted))
        sifted_key_rates.append(utils.calculate_sifted_key_rate(bob_sifted, bit_size))
        matching_bits_list.append(np.sum(np.array(alice_sifted) == np.array(bob_sifted)))

    return error_rates, sifted_key_rates, matching_bits_list

def run_b92(bit_size, iterations, eve=False):
    """
    Runs the B92 quantum key distribution simulation for a given number of iterations and bit size

    Parameters
    ----------
    bit_size : int
        The number of bits to simulate in each iteration
    iterations : int
        The number of iterations to run the simulation for
    eve : bool
        Whether to include Eve in the simulation

    Returns
    -------
    error_rates : list of float
        The list of error rates for each iteration
    sifted_key_rates : list of float
        The list of sifted key rates for each iteration
    matching_bits_list : list of int
        The list of matching bits for each iteration
    """

    return _run_simulation(
        bit_size,
        iterations,
        eve,
        no_eve_fn=lambda alice_bits, alice_bases, bob_bases: b92.no_eve(alice_bases, bob_bases),
        eve_fn=lambda alice_bits, alice_bases, eve_resend, eve_bases, bob_bases: b92.eve(alice_bases, bob_bases, eve_resend),
        intercept_fn=lambda alice_bits, alice_bases, eve_bases: eve_b92.intercept(alice_bases, eve_bases)
    )

def run_bb84(bit_size, iterations, eve=False):
    """
    Runs the BB84 quantum key distribution simulation for a given number of iterations and bit size

    Parameters
    ----------
    bit_size : int
        The number of bits to simulate in each iteration
    iterations : int
        The number of iterations to run the simulation for
    eve : bool
        Whether to include Eve in the simulation

    Returns
    -------
    error_rates : list of float
        The list of error rates for each iteration
    sifted_key_rates : list of float
        The list of sifted key rates for each iteration
    matching_bits_list : list of int
        The list of matching bits for each iteration
    """


    return _run_simulation(
        bit_size,
        iterations,
        eve,
        no_eve_fn=bb84.no_eve,
        eve_fn=bb84.eve,
        intercept_fn=eve_bb84.intercept
    )









