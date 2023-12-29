#!/bin/python

import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ifo", default=None, help="The name of the detector.")
parser.add_argument("-c", "--channels", default=None, help="The text file that records the channels to be fetched.")
parser.add_argument("-s", "--start", default=None, type=float, help="The start GPS time.")
parser.add_argument("-e", "--end", default=None, type=float, help="The end GPS time.")
parser.add_argument("-l", "--length", default=None, type=float, help="The length of each output gwf files from the start time to the end time.")
parser.add_argument("-d", "--destination", default=None, help="The directory to output the gwf files of the fetched data.")
parser.add_argument("-o", "--output", default=None, help="The directory to output the sub files.")
args = parser.parse_args()

def main():
    ifo = args.ifo
    channels = args.channels
    start = int(args.start)
    end = int(args.end)
    length = int(args.length)
    destination = args.destination
    output = args.output

    if os.path.exists(output):
        print(f"Error: The output directory {output} already exits. Please use another name of the output directory.")
        sys.exit()
    else:
        os.mkdir(output)
        os.system(f'cp get_data.py get_data.sub {output}')
        os.chdir(output)

    f_starts = [st for st in range(start, end, length)]
    f_ends = [st + length for st in f_starts[:-1]]
    f_ends.append(int(end))
    
    for st, ed in zip(f_starts, f_ends):
        job_name = f'{ifo}_{st}-{ed-st}'
        os.mkdir(job_name)

        with open('get_data.sub', 'r') as rf:
            subtext = rf.read()

        subtext = subtext.replace(r'./get_data.py', '../get_data.py')
        subtext = subtext.replace(r'$(ifo)', ifo)
        subtext = subtext.replace(r'$(channels)', channels)
        subtext = subtext.replace(r'$(start)', str(st))
        subtext = subtext.replace(r'$(end)', str(ed))
        subtext = subtext.replace(r'$(destination)', destination)

        with open(f'{job_name}/{job_name}.sub', 'w') as wf:
            wf.write(subtext)

        os.chdir(job_name)
        os.system(f'condor_submit {job_name}.sub')
        os.chdir('..')

if __name__ == "__main__":
    main()
