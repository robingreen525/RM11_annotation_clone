
#import libraries needed
import sys
import os
import argparse

#define parsing options
parser = argparse.ArgumentParser()
parser.add_argument('-genefile',type=argparse.FileType('r'))
parser.add_argument('-clonevcf', type=argparse.FileType('r'))
parser.add_argument('-dir', dest='dir')
parser.add_argument('-strain',dest='strain')
parser.add_argument('-savedir',dest='savedir')

args = parser.parse_args()

path=args.dir
strain=args.strain


'''
first, ill build a dictionary of lists where each key is the supercontig. each
dictionary value will be a list with three elements: start of ORF, end of ORF, and gene name

'''

genefile=args.genefile.readlines()
supercontigs={}

for line in genefile:
	line=line.strip('\n')
	line=line.split('\t')
	#print line
	supercontig=line[2]
	start=line[4]
	end=line[5]
	gene=line[len(line)-1]
	#print start,end,gene
	if supercontig not in supercontigs.keys():
		supercontigs[supercontig]=[start,end,gene]
	else:
		supercontigs[supercontig].append([start,end,gene])
		

'''
ok, now do the same thing for the VCF calls for the strain
'''
clonefile=args.clonevcf.readlines()

muts=[]
for line in clonefile:
	#print line
		if line[0]!='#': # get past headers
			line=line.split('\t')
			#print line
			mutation=[]
			mutation.append(line[0]) #supercontig
			mutation.append(line[1]) # position
			mutation.append(line[3]) # ref allele
			mutation.append(line[4]) # alt allele
			mutation.append(line[5]) #quality score (higher = better)
			#print mutation
			muts.append(mutation)


'''
create the savefile with my snp information
'''

savefile=args.savedir
temp=strain+"_annotated_snps.csv"
savefile=savefile+temp

w=open(savefile,'w')

header='strain,supercontig,position,alt allele,ref allele,gene start, gene end, gene\n'
w.write(header)

#print supercontigs.keys()
for mu in muts:
	supercontig=mu[0]
	pos=mu[1]
	genes=supercontigs[supercontig]
	#print genes
	for gene in genes:
		#print gene
		if(len(gene)==3): # bug with some gene entries involving hypothetical proteins, fix sometime
			gene_start=gene[0]
			#print gene_start
			gene_end=gene[1]
			if int(pos) >= int(gene_start):
				if int(pos) <= int(gene_end):
					#print supercontig, pos, gene
					#print strain
					gene_start=gene[0]
					gene_end=gene[1]
					gene=gene[2]
					#print strain,',',pos,',',gene_start,',',gene_end,',',gene,',',supercontig
					save_line=strain+','+supercontig+','+pos+','+mu[3]+','+mu[2]+','+gene_start+','+gene_end+','+gene+'\n'
					print save_line
					print savefile
					w.write(save_line)
					
w.close()
					