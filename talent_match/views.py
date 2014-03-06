from talent_match import app, db, bcrypt
from flask import render_template, request, redirect, url_for, flash, g
from flask.ext.login import login_user, login_required, logout_user
from models import User, Category, Skill
from forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm
from sqlalchemy.sql import func

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Validate the submitted data
    if form.validate_on_submit():
        # Get the user by email address
        user = User.query.filter_by(email=form.email.data).limit(1).first()
        # Check that the user exists, and that the password is correct
        if user and bcrypt.check_password_hash(user.pwd_hash, form.password.data):
            # Log the user in
            login_user(user, remember=True)
            next = request.args.get('next')
            if next:
                return redirect(next)
            # Redirect to the URL for the profile page
            return redirect(url_for('profile'))
        else:
            flash('Invalid Username/Password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.firstName.data, form.lastName.data, form.username.data, form.email.data, bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html") 

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def editProfile():
    form = EditProfileForm()
    if form.validate_on_submit():
        g.user.firstName = form.firstName.data
        g.user.lastName = form.lastName.data
        g.user.quickIntro = form.quickIntro.data
        g.user.background = form.background.data
        g.user.email = form.email.data
        g.user.phoneNumber = form.phoneNumber.data
        g.user.website = form.website.data
        db.session.commit()
        return redirect(url_for('profile'))
    form.quickIntro.data = g.user.quickIntro # or "Default Quick Intro"
    form.background.data = g.user.background 
    return render_template('/edit.html', form=form) 


@app.route('/skills', methods=['GET', 'POST'])
@login_required
def listSkills():
    # original test stuff
    # user = dict(isAdmin = True, name='Steve', email='test-only-a-test')
    # talents = [ dict(name='Harp', category='Music'), dict(name='Flute', category='Music')]
    # form = PickCategoriesForm()

    categoryID = request.values.get('categoryID')
    skillList = []
    category = None
    categoryName = None
    categoryFirst = True  # display category first or skill first in the table
    if categoryID:
        print("Looking up skills by categoryID=" + categoryID)
        category = Category.query.get(categoryID)
    if category:
        # show skills for a specific category
        categoryFirst = False   # since the category is fixes, list the skill column first
        myCategoryID = categoryID
        for cat,skill in db.session.query(Category, Skill).\
            filter(Category.id == Skill.categoryID).\
            filter(Skill.categoryID == myCategoryID).all():
                print(cat)
                print(skill)
                newSkill=dict(name=skill.name, categoryName=cat.name, description=skill.description, count='Not available yet')
                skillList.append(newSkill)

    else:
        # show all skills for all categories
        categoryFirst = True    # for better viewing all skills, put the category column first, then the skill.
        for cat,skill in db.session.query(Category, Skill).\
            filter(Category.id == Skill.categoryID).all():
                newSkill=dict(name=skill.name, categoryName=cat.name, description=skill.description, count='Not available yet')
                skillList.append(newSkill)

    if (skillList != None):
        skillList.sort(key=lambda test: (test['categoryName'], test['name']))

    form = None
    return render_template("skills.html", form=form, skillList=skillList, user=g.user, categoryName=categoryName, categoryFirst=categoryFirst)

@app.route('/categories', methods=['GET', 'POST'])
@login_required
def listCategories():
    #user = dict(isAdmin = True, name='Steve', email='test-only-a-test')
    #form = PickCategoriesForm()
    form = None

    # original category query
    #categories =  Category.query.all()
    #categories.sort(key= lambda category: category.name)

    # new category query - replacement that includes the count:
    # reminder: may be able to use "from_statement" to utilize 'raw' sql statements
    #
    # This still seems to have a bug with the EmptyCategoryTest (category with no skills).
    # There is something here that will need to be addressed long-term.
    categories = []
    for cat, myCount in db.session.query(Category, func.count('Skill.*')).\
        outerjoin(Skill).\
        group_by(Category).all():
            newCat=dict(id=cat.id, name=cat.name, description=cat.description, count=myCount)
            categories.append(newCat)
    categories.sort(key= lambda category: category['name'])

    return render_template("categories.html", form=form, categories=categories, user=g.user)

@app.route('/categories/edit', methods=['GET', 'POST'])
@login_required
def editCategory():
    isAddTalent = True # assume add to start
    form = EditCategoryForm()
    # Validate the submitted data
    if form.validate_on_submit():
        print(form.data)
        print(form.name.data)
        print(form.description.data)
        isCreate = False
        if (form.id.data == ''):
            isCreate = True
        if (isCreate):
            category = Category.query.filter_by(name=form.name.data).limit(1).first()
            if (category != None):
                print('existing category error')
                flash('Category already exists', 'error')
                return render_template("edit_category.html", editCategory=None, form=form, isAddTalent=True)
            else:
                category = Category(form.name.data, form.description.data)
                db.session.add(category)
                db.session.commit()
        else:
            category = Category.query.get(form.id.data)
            category.description = form.description.data
            category.name = form.name.data

        db.session.commit()
        return redirect('/categories')
    else:
        categoryID = request.values.get('id')
        category = None
        if categoryID != None:
            isAddTalent = False
            category = Category.query.get(categoryID)
            #print(category.name)
            #print(category.description)
            form.description.data = category.description
            form.id.data = categoryID
        else:
            isAddTalent = True
            form.id.data = None

        return render_template("edit_category.html", editCategory=category, form=form, isAddTalent=isAddTalent)

@app.route('/skills/edit', methods=['GET', 'POST'])
@login_required
def editSkill():
    print(request)
    dir(request)
    isAddSkill = True # assume add to start
    form = EditSkillForm()

    # There is a better way to do this, but this will work for today.
    if (form.category.choices == None):
        categoryChoices = []
        categoryList = Category.query.all()
        categoryList.sort(key= lambda category: category.name)
        for category in categoryList:
            #print category.name
            # categoryChoices.append( (category.name, category.id) )
            # categoryChoices.append( (category.id, category.name) )
            categoryChoices.append( (category.name, category.name) )
        form.category.choices = categoryChoices

    """
    if (form.category.choices == None):
        print("Maybe this needs to be reset?")
        categoryChoices = []
        categoryList = Category.query.all()
        categoryList.sort(key= lambda category: category.name)
        first = None
        for category in categoryList:
            if (first == None):
                #first = (category.id, category.name)
                first = category.name
            #categoryChoices.append( (category.id, category.name) )
            categoryChoices.append( category.name )
        form.category.choices = categoryChoices
        form.default = first

    # Validate the submitted data
    print(dir(form))
    if (form.errors):
        print(form.errors)
    if form.category.errors:
        print(form.category.errors)
    if form.description.errors:
        print(form.description.errors)
    if form.id.errors:
        print(form.id.errors)
    if form.name.errors:
        print(form.name.errors)
    """

    print('About to check the validation status of the form ...')

    if form.validate_on_submit():
        print('here!')
        print(dir(form))
        #print(form.name.data)
        #print(form.description.data)

        isCreate = False

        if (form.id.data == ''):
            isCreate = True
        if (isCreate):
            print(form.category.data)
            category = Category.query.filter_by(name=form.category.data).limit(1).first()
            print(category)
            testSkillName = form.name.data
            print(testSkillName)
            skill = Skill.query.\
                filter_by(categoryID=category.id).\
                filter_by(name=testSkillName).\
                first()
            if (skill != None):
                print('existing skill error')
                flash('Skill already exists', 'error')
                return render_template("edit_skill.html", editSkill=None, form=form, isAddSkill=True)
            else:
                print('trying to add the skill ... ')
                skill = Skill(category.id,testSkillName, form.description.data)
                skill.categoryID = category.id
                db.session.add(skill)
                db.session.commit()
        else:
            category = Category.query.get(form.id.data)
            category.description = form.description.data
            category.name = form.name.data

        db.session.commit()
        return redirect('/skills')

    else:
        print('here - in the regular render')

        if (form.errors):
            print(form.errors)
        if form.category.errors:
            print(form.category.errors)
        if form.description.errors:
            print(form.description.errors)
        if form.id.errors:
            print(form.id.errors)
        if form.name.errors:
            print(form.name.errors)

        skillID = request.values.get('id')
        skill = None
        print(request.values)
        if skillID:
            print('Checking the skill ... skip this for now' )
            isAddSkill = False
            skill = Skill.query.get(skillID)

            if (skill):
                form.description.data = skill.description
                form.id.data = skill.id

                form.category.choices = Category.query.all()
                # this is not right:
                form.category.default = Category.query.get(skill.categoryID)

            else:
                print('GAAAAAHH!!!!!!! This is an error.')
        else:
            print('Add skill?')
            isAddSkill = True
            form.id.data = None



        # <!-- {{ form.category(class="form-control", required=true, autofocus=true) }} -->


        return render_template("edit_skill.html", editSkill=skill, form=form, isAddSkill=isAddSkill)