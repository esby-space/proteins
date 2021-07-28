#!/usr/bin/env python

"""
Renumbers residues in a PDB file starting from a given number.
usage: python pdb_reres.py -<resi> <pdb file>
example: python pdb_reres.py -1 1CTF.pdb
Author: {0} ({1})
This program is part of the PDB tools distributed with HADDOCK
or with the HADDOCK tutorial. The utilities in this package
can be used to quickly manipulate PDB files, with the benefit
of 'piping' several different commands. This is a rewrite of old
FORTRAN77 code that was taking too much effort to compile. RIP.
"""

import os
import re
import sys

__author__ = "Joao Rodrigues"
__email__ = "j.p.g.l.m.rodrigues@gmail.com"

USAGE = __doc__.format(__author__, __email__)


def check_input(args):
    """
    Checks whether to read from stdin/file and validates user input/options.
    """

    if not len(args): # how many arguments are given
        # if the input is empty
        # No reres, from pipe
        if not sys.stdin.isatty():
            # use given file and set reres to 1
            pdbfh = sys.stdin
            reres = 1
        else:
            # nothing was given, display help screen
            sys.stderr.write(USAGE)
            sys.exit(1)
    elif len(args) == 1:
        # if the input is missing an argument
        # Resi & Pipe _or_ file & no reres
        if re.match('\-[\-0-9]+', args[0]):
            reres = int(args[0][1:])
            if not sys.stdin.isatty():
                pdbfh = sys.stdin
            else:
                sys.stderr.write(USAGE)
                sys.exit(1)
        else:
            if not os.path.isfile(args[0]):
                sys.stderr.write('File not found: ' + args[0] + '\n')
                sys.stderr.write(USAGE)
                sys.exit(1)
            pdbfh = open(args[0], 'r')
            reres = 1
    elif len(args) == 2:
        # all inputs are correct
        # Chain & File
        if not re.match('\-[\-0-9]+', args[0]):
            # if the input doesn't soley contain numbers
            sys.stderr.write('Invalid residue number: ' + args[0] + '\n')
            sys.stderr.write(USAGE)
            sys.exit(1)
        if not os.path.isfile(args[1]):
            # if the file is not found in the os path
            sys.stderr.write('File not found: ' + args[1] + '\n')
            sys.stderr.write(USAGE)
            sys.exit(1)
        reres = int(args[0][1:]) # reres = reres number to start reading
        pdbfh = open(args[1], 'r') # pdbfh = pdb file --> open the file for reading
    else:
        # an incorrect nunber of arguments were used
        sys.stderr.write(USAGE)
        sys.exit(1)

    return (reres, pdbfh)
    # returning the residue start and the file


def _renumber_pdb_residue(fhandle, sresid):
    # generator for the next line in the sequence
    # fhandle = file being used
    # sresid = starting residue
    """Enclosing logic in a function to speed up a bit"""

    resi = sresid - 1
    # computers count from 0, so the starting residue is sresid - 1
    prev_resi = None
    # initialize
    for line in fhandle:
        if line.startswith(('ATOM', 'HETATM', 'TER')): # it the atom is ATOM, HETATM, or TER
            if line[22:26] != prev_resi: # if the chain and number is different from the previous residue
                prev_resi = line[22:26] # the new previous residue is this residue
                resi += 1 # increase the count of the residue

            yield line[:22] + str(resi).rjust(4) + line[26:] # return the line with the altered residue
        else: # if the chain and number is the same
            yield line # don't change anything


if __name__ == '__main__':

    # Check Input
    reres, pdbfh = check_input(sys.argv[1:]) # check if the input actually works

    # Do the job
    new_pdb = _renumber_pdb_residue(pdbfh, reres) # renumber the file

    try:
        sys.stdout.write(''.join(new_pdb)) # joins the lines together
        sys.stdout.flush() # print them out
    except IOError:
        # This is here to catch Broken Pipes
        # for example to use 'head' or 'tail' without
        # the error message showing up
        pass

    # last line of the script
    # We can close it even if it is sys.stdin
    pdbfh.close() # stop reading the file
    sys.exit(0)
