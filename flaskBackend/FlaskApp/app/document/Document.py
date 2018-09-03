import csv,json, difflib
import os

from app.config import BLOCK_ROOT
from app.blockChain import BlockChain


class Document:

    doc_block = ''

    def __init__(self, name, autor):
        self.name = name
        self.autor = autor

    def set_hash(self, block : BlockChain):
        self.doc_hash = block
        return self.doc_hash

    def load_doc(self, file):
         open(file, 'r')

    def write_csv(self,chain : BlockChain):

        with open('blockChain.csv', 'w') as blockchain_csv:
            wr = csv.writer(blockchain_csv, quoting = csv.QUOTE_ALL)
            wr.writerow(chain)


    def print_doc(self,chain : BlockChain):

        with open(chain) as readDoc:
            content = readDoc.readlines()
        readDoc.close()
        return content

    def write_lines_from_doc(self,file):
        with open(file) as readDoc:
            content = readDoc.read()
        readDoc.close()
        return content


    def write_json(self, chain : BlockChain):

        with open(os.path.join(BLOCK_ROOT,"blockChain1.json"),'w') as blockchain_json:
            json.dump(chain, blockchain_json,indent=3,sort_keys=True)
            json_out = json.dumps(chain,indent=3,sort_keys=True)
            blockchain_json.close()
        return json_out



    def make_diff(self, fileA, fileB):
        d = difflib.Differ()

        fileA = self.write_lines_from_doc(fileA).splitlines(1)
        fileB = self.write_lines_from_doc(fileB).splitlines(1)

        diff = list(d.compare(fileA,fileB))

        return diff
