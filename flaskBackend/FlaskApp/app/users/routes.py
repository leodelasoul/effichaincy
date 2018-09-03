import os

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from app.config import basedir
from app.users.forms import EditProfileForm
from app.main import bp as bpmain
from app.models import User, Group
from app.users import bp
from app.users.forms import GroupForm,MemberForm
from sqlalchemy.sql import select,update
from sqlalchemy import *

engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'))

@bpmain.route('/index/user<userid>', methods=['GET', 'POST'])
@login_required
def user_index(userid):
    return render_template('index.html', title='Dashboard')



@bpmain.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.surname = form.surname.data
        current_user.about_me = form.about_me.data
        current_user.status = form.status.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('users.edit_profile'))
    elif request.method == 'GET':
        current_user.firstname = form.firstname.data
        current_user.surname = form.surname.data
        current_user.about_me = form.about_me.data
        current_user.status = form.status.data
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/groups', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm()
    my_groups = []
    if form.validate_on_submit():
        group = Group(name=form.name.data)
        #role = 'admin'
        #db.session.add(role)
        group.users.append(current_user)
        db.session.add(group)
        db.session.commit()
        my_groups = make_group_list()
        return render_template('groups.html', title='Groups', form=form, groups=my_groups)
    my_groups = make_group_list()
    return render_template('groups.html', title='Groups', form=form, groups=my_groups)


def make_group_list():
    my_groups = []
    
    metadata = MetaData()
    metadata.reflect(bind=engine)
    groups = metadata.tables['groups']
    group = metadata.tables['group']
        
    q = db.session.query(group,groups).filter(group.c.id == groups.c.group_id)
        
    for item in q:
        if item[2] == current_user.id:
            my_groups.append(item[1])
    
    return my_groups

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_page():
    memberform = MemberForm()
    if memberform.validate_on_submit():
        username = memberform.username.data
        groupname = memberform.groupname.data
        
        metadata = MetaData()
        metadata.reflect(bind=engine)
        group = metadata.tables['group']
        users = metadata.tables['user']
        groups = metadata.tables['groups']
        
        #group.users.append(user)
        db.session.commit()
        return render_template('add_page.html',form=memberform)
    return render_template('add_page.html', form=memberform)


# add users via username to the group
#@admin_permission.require()
@login_required
def add_members():
    return None