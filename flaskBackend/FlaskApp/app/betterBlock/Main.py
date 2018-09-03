from app.document import Document
from app.blockChain import BlockChain


from flask import Flask, redirect, url_for, request, json

app = Flask(__name__)


def main():
    first_Doc = Document.Document('txtA.txt', 'Leo')


    block_Instance = BlockChain.BlockChain(BlockChain.BlockChain.block_hash)  # create an empty blockchain object

    block_Instance.create_genesis(first_Doc)  # first block

    second_doc = Document.Document('txtB.txt', 'Dani')

    block_Instance.make_block(block_Instance.chain, second_doc)  # create a block with our text b
    # print(block_Instance[1]['contents']['Filename'])

#    print(second_doc.print_doc(block_Instance['hash']['contents']['Filename']))  # see whats inside of text b


    second_doc.make_diff(first_Doc.name, second_doc.name)  # make our diffs
    print((block_Instance.chain[0]['hash']))


    #+print(block_Instance.chain[1][])  # print the whole chain
    print("yolo")


'''def flask_blackend():
    @app.route('/', methods=['POST'])
    def index():
        my_json = open('blockChain.json', 'r')
        return json.dumps(my_json)

    
    @app.route('/blockchain/<user_session>')
    def blockchain(user_session):
        first_Doc = Document.Document('txtA.txt', 'Leo')
        block_Instance = BlockChain.BlockChain(BlockChain.BlockChain.block_hash)  # create an empty blockchain object
        block_Instance.create_genesis(first_Doc)  # first block

        yolo = print(block_Instance.chain)

        return yolo
    
    app.run()

'''
if __name__ == '__main__':
    main()

