Organellar tRNAs in Parasitic Plant Species

Here are input genebank (.gbk) files for various mitochondrial and plastid genomes, and accompanying scripts for generating figures plotting presence/absence analysis of tRNAs in relation to aminoacy tRNA-synthetases.
Description of the data and file structure

    Zipped data directory gbk/ contains genebank annotation files which are input for plotting absence/presence of organellar tRNAs, aminoacyl tRNA-synthetases (fig. 4)

    trna_parse2.pl is a perl script used for extracting tRNAs from gbk files, originally written by Dan Sloan.

    jupyter notebook 20240820_parsetRNA.ipynb was used to generate plot (Fig. 4)

    20240820_absencepresence_retarget.csv is a metadata file containing a data matrix detailing for each aaRS whether the organellar enzyme is absent/present, and whether the cytosolic enzyme is retargeted/not retargeted/unknown. This data was used by 20240820_parsetRNA.ipynb to overlay tRNA data. More information about ortholog presence/absence data from https://doi.org/10.5061/dryad.0cfxpnw7p, targeting from https://doi.org/10.5061/dryad.6hdr7sr5x. Also see manuscript for more details.

    AA_codes.txt is a metadatafile containing the 1 letter and 3 letter codes for each amino acid, used by 20240820_parsetRNA.ipynb for axis labels.

Sharing/Access information

.gbk files were downloaded from NCBI. See manuscript for more details.
Code/Software

Requires Bioperl, python3, Jupyter notebooks

extract tRNAs from Genebank files (.gbk):

for file in *.gbk; do trna_parse2.pl $file > ${file%.gbk}_tRNA.tab; done

Then open 20240820_absencepresence_retarget.ipynb to plot. Ensure output .csv file from targeting analysis (i.e.20240820_absencepresence_retarget_both.csv) is included with info

python packages required include:
pandas
numpy
seaborn
matplotlib
string
re
os
Version Changes

20240820: Use of updated metadata file (20240820_absencepresence_retarget.csv) reflecting reanalysis with updated gene models, see publication and associated datasets. Update to 20240820_parsetRNA.ipynb- plot plastid targeting predictions for Rafflesiaceae species.

