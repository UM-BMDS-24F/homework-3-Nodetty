import subprocess
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast import NCBIXML

def initialize_blast_database(sequence_file, database_name, alias):
    #making a BLAST data base from fastafile
    subprocess.run([
        "/opt/homebrew/bin/makeblastdb",
        "-in", sequence_file,
        "-dbtype", "prot",
        "-out", database_name,
        "-title", alias,
        "-max_file_sz", "2GB"
    ], check=True)

def execute_blast(query_sequences, database, results_file, evalue_threshold=0.001):
    #BLAST search and save the output as XML
    blast_command = NcbiblastpCommandline(
        cmd="/opt/homebrew/bin/blastp",
        query=query_sequences,
        db=database,
        evalue=evalue_threshold,
        out=results_file,
        outfmt=5
    )
        blast_command()

def process_blast_results(xml_results, output_file):
    #Parse BLAST XML results and print out results in proper format
    with open(xml_results) as results, open(output_file, "w") as output:
        records = NCBIXML.parse(results)
        for record in records:
            output.write(f"Query Sequence ID: {record.query}\n")
            for match in record.alignments:
                output.write(f"Subject Sequence ID: {match.hit_def}\n")
                for segment in match.hsps:
                    output.write(f"Alignment E-value: {segment.expect}\n")
                    output.write(f"Score: {segment.score}\n")
                    output.write(f"Alignment Length: {segment.align_length}\n")
                    output.write(f"Query Alignment: {segment.query}\n")
                    output.write(f"Subject Alignment: {segment.sbjct}\n")
                    output.write("=" * 50 + "\n")

def run_analysis():
    # file paths and parameters
    source_sequences = "mouse.fa"
    blast_db = "protein_db"
    query_sequences = "human.fa"
    xml_results = "blast_output.xml"
    text_output = "formatted_blast_results.txt"

    #BLAST process
    initialize_blast_database(sequence_file=source_sequences, database_name=blast_db, alias="Mouse_Protein_DB")
    execute_blast(query_sequences=query_sequences, database=blast_db, results_file=xml_results)
    process_blast_results(xml_results=xml_results, output_file=text_output)

if __name__ == "__main__":
    run_analysis()

