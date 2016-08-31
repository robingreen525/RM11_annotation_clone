
#import libraries needed
import sys
import os
import argparse

#define parsing options
parser = argparse.ArgumentParser()
parser.add_argument('-gene_list',type=argparse.FileType('r'))
parser.add_argument('-liftover', type=argparse.FileType('r'))
parser.add_argument('-dir', dest='dir')

args = parser.parse_args()

path=args.dir
genefile=args.gene_list.read()

'''
build a dictionary of systematic names and CDS
'''

gene_info={}
genefile=genefile.split('>')
for line in genefile:
	linelist=line.split('\n')
	name=linelist[0]
	name=name.split('_')
	name= name[0]
	gene=''
	for i in range(1,len(linelist)):
		gene=gene+linelist[i]
	gene=gene.rstrip('\n')
	##print gene
	if name not in gene_info.keys():
		gene_info[name]=[gene] # make item a list, so i can append information later
	else:
		#print 'conflict'
		#print name
		#print gene
		continue # five or so issues with genes similar to other yeast species, ignore for now

args.gene_list.close()

'''
add gene start/stop information
'''

liftfile=args.liftover.readlines()

for line in liftfile:
	line=line.split('\t')
	if len(line)>1:
		if(line[2])=='CDS':
			print line
