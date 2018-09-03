import hashlib, json, sys
import os
import datetime
from string import digits

from flask_login import current_user

from app.document import Document
from app.config import APP_ROOT

# import unicode from datashape
from app.users.Groups import Users

APP_ROOTs = os.path.dirname(os.path.relpath(__file__))
json_block_path = "app/document/blockChain1.json"


class BlockChain:

    def __init__(self, chain):
        self.chain = chain

    def hashMe(self, msg):
        if type(msg) != str:
            msg = json.dumps(msg, sort_keys=True)

        # if sys.version_info.major == 2:
        # return unicode(hashlib.sha256(msg).hexdigest(), 'utf-8')
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

    def create_genesis(self, chain, doc: Document):
        genesisBlockContents = {u'blockNumber': 0, u'parentHash': 0, u'Filename': None, u'Diffs': False,
                                u'Author': None}

        self.block_hash = self.hashMe(genesisBlockContents)
        self.block = {u'hash': self.block_hash, u'contents': genesisBlockContents}
        chain = []
        chain.append(self.block)
        doc.write_json(chain)
        return self.chain

    def make_version_index(self, chain, doc: Document):
        filenames_list = []
        count = 0
        versioned = ""

        for i in range(len(chain)):
            filename = chain[i]['contents']['Filename']
            filename = str(filename)
            finalized = ""
            num_to_dot = filename.find('.')

            if(num_to_dot > 0):
                striped_filename = filename[0:num_to_dot]
                from_slash = striped_filename.rfind("/")
                striped_filename = striped_filename[from_slash:len(striped_filename)]
                striped_filename = ''.join([i for i in striped_filename if not i.isdigit()])
                finalized = filename[0:from_slash] + striped_filename

            if bool(chain[i]['contents']['Author'] == doc.autor) & bool(finalized in doc.name):

                count = 1 + count
                versioned = finalized + str(count) + ".txt"
                if count == 0 :
                    filenames_list.append(doc.name)
                    continue

                elif count == len(filenames_list):
                    filenames_list.append(doc.name )
                filenames_list.append(versioned)
        return filenames_list

    def make_block(self, chain, doc: Document):

        self.doc = doc
        self.chain = [chain][0]

        parentBlock = self.chain[-1]
        parentHash = parentBlock[u'hash']
        time_stamp = str(datetime.datetime.now())

        # diffs = doc.make_diff()
        #diffs = self.doc.make_diff(parentBlock['contents']['Filename'], self.doc.name)  # make our diffs
        versioned_files = self.make_version_index(self.chain, doc)
        blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
        blockContents = {u'blockNumber': blockNumber, u'parentHash': parentHash, u'Filename': self.doc.name,
                         u'Diffs': 'diffs', u'Author': self.doc.autor, u'versionedFiles': versioned_files, u'timeStamp': time_stamp}
        blockHash = self.hashMe(blockContents)
        self.block = {u'hash': blockHash, u'contents': blockContents}
        self.chain.append(self.block)
        doc.write_json(self.chain)

        return self.block

    def get_block_hash(self):
        return self.block_hash

    def __getitem__(self, index):
        return self.chain[index]

    def __setitem__(self, index, value):
        self.chain[index] = value
