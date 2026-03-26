Finding orthologs of Aminoacyl tRNA synthetases in parasitic plants.

Here is the relevant output from Orthofinder run on parasitic and autotrophic plants. Additionally there are some scripts used in the analysis downstream, including finding all orthogroups with aminoacyl tRNA synthetases, running reciprocal best hit (RBH) searches in BLAST, and sorting and plotting orthologs based on length of sequence relative to Arabidopsis thaliana reference.

Description of the data and file structure

This submission has the initial output from Orthofinder: Orthogroups.tsv
This submission also has downstream code for analysis (see code section for more details)
Required metadata files to run code:

aaRS_tRNAprocessing.txt - metadata about genes of interest, including Arabidopsis thaliana ortholog TAIR identifiers, and description of sub-cellular targeting and target amino acid.

psuedogenes.txt - A list of known amino-acyl tRNA psuedogenes in Arabidopsis thaliana, based on Duchenne et. al., 2005.

aaRS_tRNAprocessing_Athal_query.txt - Just the TAIR identifiers for genes of interest, for use in Reciprocal Best Hit via BLAST+.

orthogroups_geneID.txt - metadata about genes of interest, including subcellular targeting, description, and orthogroup identifier from Orthofinder analysis.

orthogroup_sequences.zip - contains amino acid sequences for each orthogroup with target genes.

Sharing/Access information

Data was derived from many publicly available datasets. See publication for details.

Orthofinder was used to find orthologous protein sequences across all species.

References:

Emms DM, Kelly S, 2015. OrthoFinder: solving fundamental biases in whole genome comparisons dramatically improves orthogroup inference accuracy. Genome Biology 16.

Emms DM, Kelly S, 2019. OrthoFinder: Phylogenetic orthology inference for comparative genomics. Genome Biology 20.

Blast+ was used for Reciprocal Best Hit analysis:

Camacho C, Coulouris G, Avagyan V et al., 2009. BLAST+: Architecture and applications. BMC Bioinformatics 10.

Code/Software

Includes python scripts and a bash script used for downstream analysis and data visualization.

Extract orthogroups of interest based on list:

python3 individualfind_orthogroups.py  aaRS_tRNAprocessing_Athal_query.txt Orthogroups.tsv orthogroups_ind.xlsx

Obtain Reciprocal Best Hit (RBH) using blast against A. thaliana. Requires BLAST+ installed locally, and databases generated from protein annotations for each species including Arabidopsis.

for fa in ~/blastdb/_prot.fa; do blast_RBH_noE.sh aaRS_tRNAprocessing_Athal_query.txt blastdb/A_thaliana_prot.fa $fa ${fa#////} A_thaliana_prot.fa; done

Merge Orthogroups and RBH hits:

for f in $(ls blast_RBH*); do merge_orthofinder_blastRBH.py orthogroups_ind.xlsx $f; done

Extract sequences for each gene in each orthogroup and generate new fasta file. Use command line to remove psuedogenes in psuedogenes.txt Then generate multiple sequence alignments for each orthogroup in via MAFFT and put into folder alignments/

Use script to parse output- determine ortholog length relative to A. thaliana model

parse_absencepresence.py orthogroup_sequences/ presence_absence_seperateoldnewmodels.xlsx

Plot using jupyter notebook plot_presenceabsence.ipynb

python packages required include:
pandas
numpy
seaborn
scipy.stats
matplotlib
re
os
datetime
math

Version changes

20240528: Re-did analysis but added two new sets of gene models (old models run in parallel), resulting in an entirely new Orthogroups.tsv file. Metadata file with list of aaRS/tRNA modifying enzymes is included as an example of format. For lists of other proteins from the study (i.e. riboproteins, targeting controls, organelle import machinery), please see linked publication.

Balanophora fungosa: Genome-based models from China National GeneBank (CNGB) Sequence Archive (CNSA) accession number CNP0003054

Sapria himalayana: Protein models directly from author of DOI: 10.1186/s12915-023-01620-3.

20240811: Altered tablemash_blast_RBH.py so species name is added to name of output excel file

20240820: Altered scripts for parsing sequences by length and plotting

Removed MAFFT alignment step (parse_after_mafft.py), replaced with new script parse_absencepresence.py which just assesses length of putative ortholog relative to A. thaliana model without multiple sequence alignment.

Removed analysis/ plotting of of tetrapyrole pathway, added analysis/ plotting of organelle protein import machinery to plot_presenceabsence.ipynb

