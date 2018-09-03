import os, fnmatch
import json
import html
import difflib

from flask import render_template, request, send_from_directory, flash, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.debug.repr import dump
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup

from app import ALLOWED_EXTENSIONS
from app.users import Groups
from app.auth import routes as auth_user
from app.models import User, Document

from app.document import bp,Document
from app.users.Groups import Users
from app.blockChain import BlockChain
from app.config import BLOCK_ROOT
APP_ROOT = os.path.dirname(os.path.relpath(__file__))
blockchain_root = os.path.join(BLOCK_ROOT,"blockChain1.json")


@bp.route('/documents', methods=['GET'])
def view_documents():
    
    #with open(blockchain_root, 'r+') as file:
    #   data = json.load(file)
    #   file.close()

    soup = BeautifulSoup(open("app/templates/history.html"),"html.parser")
 
    list = soup.ul
    
    with open(blockchain_root, 'r+') as file:
        data = json.load(file)
     
    data.reverse()
    
    i = 0
    
    h = len(data[i]["hash"])
    
    while i < len(data)-1:
        found_user = False
        got_filename = False
        
        new_li = soup.new_tag("li", **{'class': 'history_items' })
        current_file = data[i]["contents"]["Filename"]
        filename_only = ""
        user_id = ""
        
        path_split = current_file.split("/")
                
        filename_only = path_split[-1]
        user_id = path_split[-2]
        download_filename = "" + user_id + "/" + filename_only
        filename_split = filename_only.split(".")
        version = "";
        
        k = 0
        for letter in filename_split[0][::-1]:
            if letter == 'v':
                break
            else:
                version += letter
            k+=1        
        version = version[::-1]
        
        filename_only = "" + filename_split[0][0:len(filename_split[0])-(k+2)] + "." + filename_split[1]
        
        last_versions = data[i]["contents"]["versionedFiles"]
        current_version = 0
        file_to_compare_with = current_file
        
        if last_versions:
            file_to_compare_with = last_versions[-1]
            
        files = "" + current_file + ";" + file_to_compare_with

        view_link = soup.new_tag("a", href=url_for('document.send_iframe_doc', file=download_filename))
        compare_link = soup.new_tag("a", href= url_for('document.compare_doc',docs=files))
        download_link = soup.new_tag("a", href=url_for('document.download_file', filename=download_filename)) 
        
        hash_span = soup.new_tag("span", **{'class': 'history_hash' })
        name_span = soup.new_tag("span", **{'class': 'history_name' })
        download_span = soup.new_tag("span", **{'class': 'history_download' })
        compare_span = soup.new_tag("span", **{'class': 'history_compare' })
        version_span = soup.new_tag("span", **{'class': 'history_version' })
        time_span = soup.new_tag("span", **{'class': 'history_time' })
        
        new_p = soup.new_tag("p")
        
        list.append(new_li)
        name_span.append(view_link)
        download_span.append(download_link)
        compare_span.append(compare_link)
        
        new_li.insert(len(new_li.contents), hash_span)
        new_li.insert(len(new_li.contents), name_span)
        new_li.insert(len(new_li.contents), version_span)
        new_li.insert(len(new_li.contents), time_span)
        new_li.insert(len(new_li.contents), download_span)
        new_li.insert(len(new_li.contents), compare_span)
        new_li.insert(len(new_li.contents), new_p)
        
        time_span.string = "Upload time: " + data[i]["contents"]["timeStamp"] + " |"
        version_span.string = "Version: " + version + " |"
        download_link.string = "Download"
        hash_span.string = "Hash: .." + data[i]["hash"][h-4:h] + " |"
        compare_link.string = "Compare"
        view_link.string = filename_only + " |"
        new_p.string = "Author: " + data[i]["contents"]["Author"]
        i += 1
    
    content = soup.prettify(formatter="html")
    
    open("app/templates/history_result.html","w").close()
    html_result = open("app/templates/history_result.html","w")
    html_result.write(content)
    html_result.close()
    
    return render_template("history_result.html")


# allows multiple file uploads
@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_doc():

    with open(blockchain_root ,"r") as block_init:
        parsed_json = json.load(block_init)
        chain = BlockChain.BlockChain(parsed_json)
        block_init.close()

    if request.method == 'POST':
        # check if the post request has the file part
        users = Users(current_user.id, current_user.username)

        # join/add to this
        target = os.path.join(APP_ROOT, 'Effichaincy/documents/' + str(users.id) + "")
        all_userdirs = os.path.join(APP_ROOT, 'Effichaincy/documents/')
        # create folder if nonexistent
        if not os.path.isdir(target):
            os.makedirs(target)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        #if 'file' in request.files:
        #    return render_template('e_file_already_exists.html', title='Oops')
        if file:
            doc = Document.Document(target + "/" + file.filename,users.name)
            filename = file.filename
            file_loc = target + "/" + filename
            count = 1
            to_dot = filename.find('.')
            strip_file = filename[0:to_dot]
            sec_filename_num = strip_file + '_v' + str(count) + '.txt'
            for dirs in os.listdir(all_userdirs):
                current_dir = os.path.join(all_userdirs,dirs)
                if os.path.isfile(current_dir + "/" + sec_filename_num):
                    print("True for: " + current_dir)
                    for files in os.listdir(current_dir):
                        file = request.files['file']
                        file_name = file.filename
                        num_to_dot = file_name.find('.')
                        striped_file = file_name[0:num_to_dot]
                        if striped_file in files:
                            count = count + 1
                            sec_filename_num = striped_file + '_v' +  str(count) + '.txt'
                            #sec_filename_num = secure_filename(file_with_num)
            file.save(target + "/" + sec_filename_num)
            doc.name = target + "/" + sec_filename_num
            chain.make_block(chain.chain, doc)
            return render_template('upload_completion.html', title='Success', file=sec_filename_num)


# issue here is that the method does not find the desired file yet --> should get file out of blockchain/db
# index.html still needs filename
# filename needs to be saved to db to be downloadable
@bp.route('/uploads/<path:filename>', methods=['GET', 'POST'])
@login_required
def download_file(filename):
    return send_from_directory('../app/document/Effichaincy/documents', filename, as_attachment=True)


@bp.route('/document/<id>')
@login_required
def document(id):
    document = Document.query.filter_by(id=id).first_or_404()
    return render_template('index.html', document=document)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@bp.route('/content/<f>')
def show_doc(f):
    users = Users(current_user.id,current_user.username)
    target = os.path.join(APP_ROOT, 'Effichaincy/documents/' + str(users.id) + "")
    text = open(os.path.join(target, f), 'r+')
    content = text.read()
    text.close()
    return render_template('doc_content.html', doc = content)

@bp.route('/historycontent/<path:file>')
def send_iframe_doc(file):
    return render_template('view_document.html',file = file)
    
@bp.route('/iframe/<path:file>')
def show_doc_content(file):
    target = os.path.join(APP_ROOT, 'Effichaincy/documents/') 
    text = open(os.path.join(target,file),'r')
    content = text.read()
    text.close()
    return render_template('doc_content.html', doc=content)

@bp.route('/compare/<path:docs>')
def compare_doc(docs):
    
    target = os.path.join(APP_ROOT, 'Effichaincy/documents/') 
    files=[]
    d = difflib.Differ()
    
    docs = docs.split(";")
    for path in docs:
        singles = path.split("/")
        files.append(singles[-2] + "/" + singles[-1])
        
    fileA = open(os.path.join(target,files[1]),'r').read().splitlines(1)
    fileB = open(os.path.join(target,files[0]),'r').read().splitlines(1)
  
    diffs = list(d.compare(fileA,fileB))
    
    soup = BeautifulSoup("<pre></pre>","html.parser")
    
    pre = soup.pre
    br = soup.new_tag('br')
    
    for s in diffs:
        kind = s[0]
        
        colortype = ''
        
        if kind == '+':
            colortype = 'plus'
            span = soup.new_tag('span',**{'class': colortype })
            span.string = s
            pre.append(br)
            pre.append(span)
        elif kind == '-':
            colortype = 'minus'
            span = soup.new_tag('span',**{'class': colortype })
            span.string = s
            pre.append(br)
            pre.append(span)
        elif kind == ' ':
            span = soup.new_tag('span',**{'class': colortype })
            span.string = s
            pre.append(br)
            pre.append(span)
   
    span.append(soup.new_tag('style', type='text/css'))
    span.style.append('.minus {background-color:rgba(238,163,128,0.7);}')
    span.style.append('.plus {background-color:rgba(0,155,119,0.45);}')
    span.style.append('span {width:100%}')
    
        
    content = soup.prettify(formatter="html")
    
    diff_result = open("app/templates/diffs.html","w")
    diff_result.write(content)
    diff_result.close()

    return render_template('compare.html',file1=files[0],file2=files[1])

@bp.route('/comparison_result')
@login_required
def show_comparison_result():
    return render_template('comparison_result.html')

@bp.route('/show_diffs')
@login_required
def show_diffs():
    return render_template('diffs.html')

@bp.route('/merge')
@login_required
def merge():
    return render_template('merge.html')

@bp.route('/merge_result')
@login_required
def merge_result():
    return render_template('merge_result.html')