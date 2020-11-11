#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2020 Dan Persons (dogoncouch@dogoncouch.net)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from argparse import ArgumentParser
from os.path import isfile
from yaml import full_load as yaml_full_load
from json import loads as json_loads

from sigmacheck import __version__

class SigmaCheckCore:

    def __init__(self):
        """Initialize the sigmacheck program"""

        self.args = None
        self.arg_parser = ArgumentParser()
        self.subparsers = self.arg_parser.add_subparsers(title='subcommands',
                dest = 'subcommand',
                help = 'sigmacheck [subcommand] -h for more information')
        self.parse_args()
        self.rules = []


    def parse_args(self):
        """Set argument options"""

        self.arg_parser.add_argument('--version', action = 'version',
                version = '%(prog)s ' + str(__version__))

        self.validateparser = self.subparsers.add_parser('validate',
                help = 'validate Sigma rules for sanity')
        self.validateparser.description = 'Validate Sigma rules for sanity'
        self.validateparser.add_argument('-j', '--json',
                action = 'store_true',
                help = 'load Sigma rules from JSON format')
        self.validateparser.add_argument('files',
                metavar = 'file', nargs = '+',
                help = 'input file containing Sigma rules')

        self.checkparser = self.subparsers.add_parser('check',
                help = 'check events against Sigma rule conditions')
        self.checkparser.description = 'Check events against Sigma rule ' + \
                'conditions'
        self.checkparser.add_argument('-j', '--json',
                action = 'store_true',
                help = 'load Sigma rules from JSON format')
        self.checkparser.add_argument('files',
                metavar = 'file', nargs = '+',
                help = 'input file containing Sigma rules')
        self.checkparser.add_argument('eventfiles',
                metavar = 'event_file', nargs = '+',
                help = 'input file containing events in JSON format')

        self.convertparser = self.subparsers.add_parser('convert',
                help = 'convert Sigma rules between formats')
        self.convertparser.description = 'Convert Sigma rules between formats'
        formatgroup = self.convertparser.add_mutually_exclusive_group()
        formatgroup.add_argument('-y', '--toyaml',
                action = 'store_true',
                help = 'output rules in YAML format')
        formatgroup.add_argument('-j', '--tojson',
                action = 'store_true',
                help = 'output rules in JSON format')
        self.checkparser.add_argument('files',
                metavar = 'file', nargs = '*',
                help = 'input file containing Sigma rules in YAML format')
        self.checkparser.add_argument('jsonfiles',
                metavar = 'json_file', nargs = '*',
                help = 'input file containing Sigma rules in JSON format')
        self.checkparser.add_argument('-o', '--output',
                required = True,
                help = 'output file for converted Sigma rules')

        self.args = self.arg_parser.parse_args()


    def validate(self):
        """Validate a Sigma rule file"""
        # To do: pretty much everything
        pass


    def check(self):
        """Test events agains Sigma rules to see if rule conditions are met"""
        # To do: pretty much everything
        pass


    def load_rules(self):
        """Load Sigma rules from files"""
        for f in self.args.files:
            if self.args.json:
                newrules = load_json(f)
                for rule in newrules:
                    validation = validate(rule)
                    if validation:
                        print(validation)
                    else:
                        self.rules.append(rule)
                #self.rules.append(load_json(f))
            else:
                newrules = load(f)
                for rule in newrules:
                    validation = validate(rule)
                    if validation:
                        print(validation)
                    else:
                        self.rules.append(rule)
                #self.rules.append(load(f))


    def run(self):
        """Run the program"""
        try:
            getattr(self, self.args.subcommand)()
        except KeyboardInterrupt:
            print('Exiting on KeyboardInterrupt')
            exit(1)



# Backend functions (should be easily used from Python shell/Jupyter/etc)

def check(rules, events):
    """Evaluate events against a Sigma rule"""
    # Dedup events and rules before starting to save CPU time?
    # Keep record of removed events so if one event matches, others will, too
    # No need to keep record of duplicate rules
    pass


def validate(rules):
    """Validate Sigma rules for sanity (assumes cleanly loaded rule)"""
    if isinstance(rules, list):
        for rule in rules:
            validaterule(rule)
            # Validate rule sanity
            # Return False if no problems, else string with error description
            # Errors should be useful in diagnosing rule format errors, etc
        pass
    else:
        validaterule(rule)
        # Validate single rule for sanity, same as above


def validaterule(rule):
    """Validate a Sigma rule for sanity (assumes cleanly loaded rule)"""
    for rule in rules:
        # Validate rule sanity
        # Return False if no problems, string with error description otherwise
        # Errors should be useful in diagnosing rule format errors, etc
        pass


def load(filename):
    """Load Sigma rules from a YAML file and return a list of dicts"""
    if isfile(filename):
        rules = yaml_full_load(filename)
        return rules


def load_json(filename):
    """Load Sigma rules from a JSON file and return a list of dicts"""
    if isfile(filename):
        rules = json_loads(filename)
        return rules


def main():
    sigmachecker = SigmaCheckCore()
    sigmachecker.run()


if __name__ == "__main__":
    main()
