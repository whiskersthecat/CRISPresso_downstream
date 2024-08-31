#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int argc, char* argv[]) {
	if(argc < 3) {
		cout << "Usage: ./summarizer samples.tsv guides.tsv num_reads=2 mode" << endl;
		cout << " ***** Summarizer operates downstream of CRISPRESSO to summarize the most common reads for each sample *****" << endl;
		cout << " >samples.tsv file includes each sample name seperated by a tab, space, or new line." << endl;
		cout << " >guides.tsv each line includes site name followed by sgRNA sequence seperated by a tab, space or new line." << endl;
		cout << " >By default, the top two reads will be taken, unless another number is put as the last argument." << endl;
		cout << " >By default, assumes directories are from paired end, using f or r for mode if doing split end." << endl;
		exit(0);
	}

	char mode = ' ';
	string insert = "";
	if(argc > 4) mode = argv[4][0];

	vector<string> ids;
	ifstream samples(argv[1]);
	if(!samples) {
		cout << "ERROR: Bad samples file" << endl;
		exit(0);
	}
	string sample;
	while(samples >> sample) {
		if(mode == 'f') {
			ids.push_back(sample);
			insert = ".f";
		}
		else if(mode == 'r') {
			ids.push_back(sample);
			insert = ".r";
		}
		else {
			ids.push_back(sample);
		}

	}

	vector<string> sites;
	vector<string> seq;
	ifstream sequences(argv[2]);
	if(!sequences) {
		cout << "ERROR: Bad sequences file" << endl;
		exit(0);
	}
	string sequence, siteName;
	while(sequences >> siteName) {
		sequences >> sequence;
		sites.push_back(siteName);
		seq.push_back(sequence);
	}

	int num_reads = 2;
	if(argc > 3) num_reads = atoi(argv[3]);

	


	ofstream output("summary.tsv");
	output << "Site\tSample\tAligned Sequence\tReference Sequence\tUnedited\tn_deleted\tn_inserted\tn_mutated\t#Reads\t%Reads" << endl;
	cout << "Writing to file: summary.tsv" << endl;
	for(int i = 0; i < (int) seq.size(); i++) {
		cout << seq[i - 1] << endl;

		for(auto plant : ids) {
			cout << ">>" << plant << endl;

			string directory = "./";
			//directory += "Site" + to_string(i) + "/";

			//if(i == 4) directory += "Single-end/CRISPResso.S" + to_string(i) + "." + plant + ".f.3/";
			directory += "CRISPResso." + sites[i]  + "." + plant + insert + ".3/";
			//if(i ==4) directory += "CRISPResso_on_S" + to_string(i) + "." + plant + ".clean.f.fq/";
			if(mode == ' ')
				directory += "CRISPResso_on_" + sites[i] + "." + plant + ".clean_R1.fq_" + sites[i] + "." + plant + ".clean_R2.fq/";
			else if(mode == 'f')
				directory += "CRISPResso_on_" + sites[i] + "." + plant + ".clean.f.fq/";
			else if(mode == 'r')
				directory += "CRISPResso_on_" + sites[i] + "." + plant + ".clean.r.fq/";
			
			for(int j = 0; j < (int)plant.length(); j++) {
				if(plant[j] == '.')
					plant[j] = '_';
			}
			//if(i==4) directory += "S" + to_string(i) + "_" + plant + "_f_3.Alleles_frequency_table_around_sgRNA_" + seq[i-1] + ".txt";
			if(insert == "")
				directory += sites[i] + "_" + plant + "_3.Alleles_frequency_table_around_sgRNA_" + seq[i] + ".txt";
			else if (insert == ".f")
				directory += sites[i] + "_" + plant + "_f" + "_3.Alleles_frequency_table_around_sgRNA_" + seq[i] + ".txt";
			else if (insert == ".r")
				directory += sites[i] + "_" + plant + "_r" + "_3.Alleles_frequency_table_around_sgRNA_" + seq[i] + ".txt";
			/*if(i == 4 && plant.compare("water") == 0) {
				directory = "./Site4/Paired-End/CRISPResso.S4.water.3/CRISPResso_on_S4.water.clean_R1.fq_S4.water.clean_R2.fq/S4_water_3.Alleles_frequency_table_around_sgRNA_TATCAGGTTCCATAGAACCA.txt";
			}*/
			//S1_22G1T_uc_3.Alleles_frequency_table_around_sgRNA_CGGAAATGATAGTCTGGCGG.txt

			ifstream tablefile(directory);
			if(!tablefile) {
				cout << "ERR: Failed opening file in directory: " << directory << endl;
				cout << " -There are likely no aligned reads for this sample" << endl;
				output << i << "\t" << plant << "\t" << "No_Reads" << '\t' << "No_Reads\t" << "TRUE\t" << 0 << "\t" << 0 << "\t" << -1 << "\t" << 1 << "\t" << 100.0 << endl;
				output << i << "\t" << plant << "\t" << "No_Reads" << '\t' << "No_Reads\t" << "TRUE\t" << 0 << "\t" << 0 << "\t" << 0 << "\t" << 0 << "\t" << 0.0 << endl;

			} else {
				string sequence;
				getline(tablefile, sequence);
				for(int j = 0; j < num_reads; j++) {
					getline(tablefile, sequence);
					output << i << "\t" << plant << "\t";
					output << sequence << endl;
				}
			}
			
			/*getline(tablefile, sequence);
			output << i << "\t" << plant << "\t";
			output << sequence << endl;*/
		}
	}
	output.close();
	return 0;
}