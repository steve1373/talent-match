
from talent_match.models import User,Skill,Category,Seeker,Provider,ProviderSkill,Invitation,Activity,ActivitySkill
from talent_match import db

__author__ = 'Steve'

def addTestData() :
    userList = None
    userList = User.query.filter_by(is_admin=True)

    categoryList = Category.query.order_by(Category.name)
    skillList = Skill.query.order_by(Skill.name)

    if (userList == None) or (userList.count() < 1):
        print("Adding default user(s)")

        print("Adding user='admin'")
        admin = User()
        admin.is_admin = True; admin.username = 'admin'; admin.email = 'admin@talent-match.us'
        admin.pwd_hash ='$2a$12$5XpK1rXasJv1Zdz7ABxMN.EyHERZ7WqMUjmRQeFALP7LEbrNB8tb2' # admin!
        db.session.add(admin)
        db.session.commit()
        seeker = Seeker(admin.id)
        provider = Provider(admin.id)
        db.session.add(seeker)
        db.session.add(provider)
        db.session.commit()

        print("Adding user='sally'")
        sally = User()
        sally.is_admin = True; sally.username = 'sally'; sally.email = 'sally@talent-match.us'
        sally.pwd_hash ='$2a$12$onbU2C6cjWs16m1RLDOjrObCpP8tLb28RAQeiYAbqE/JjPsGJiDOa' # sally!
        sally.firstName = 'Sally'
        sally.lastName = 'Struthers'
        sally.phoneNumber = '806-555-1212'
        sally.website = 'sallystruthers.com'
        db.session.add(sally)
        db.session.commit()
        sallySeeker = Seeker(sally.id)
        sallyProvider = Provider(sally.id)
        db.session.add(sallySeeker)
        db.session.add(sallyProvider)
        db.session.commit()

        print("Adding user='sally.smith'")
        sally = User()
        sally.is_admin = False; sally.username = 'sally.smith'; sally.email = 'sally.smith@talent-match.us'
        sally.pwd_hash ='$2a$12$onbU2C6cjWs16m1RLDOjrObCpP8tLb28RAQeiYAbqE/JjPsGJiDOa' # sally!
        sally.firstName = 'Sally'
        sally.lastName = 'Smith'
        sally.phoneNumber = '806-555-1212'
        sally.website = 'sally-smith-realty.com'
        db.session.add(sally)
        db.session.commit()

        sallySeeker = Seeker(sally.id)
        sallyProvider = Provider(sally.id)
        db.session.add(sallySeeker)
        db.session.add(sallyProvider)
        db.session.commit()

        print("Adding user='steve'")
        steve = User()
        steve.is_admin = True
        steve.username = 'steve'
        steve.email = 'steve@talent-match.us'
        steve.pwd_hash ='$2a$12$5XpK1rXasJv1Zdz7ABxMN.EyHERZ7WqMUjmRQeFALP7LEbrNB8tb2'  # admin!
        steve.firstName = 'Steve'
        steve.lastName = 'Smith'
        steve.phoneNumber = '806-555-1212'
        steve.website = 'steves-world.com'
        db.session.add(steve)
        db.session.commit()
        steveSeeker = Seeker(steve.id)
        steveProvider = Provider(steve.id)
        db.session.add(steveSeeker)
        db.session.add(steveProvider)
        db.session.commit()

    else:
        pass

    if (categoryList == None) or (categoryList.count() < 1):
        categoryList = \
            {
              'Music' :
                  ['Harp', 'Flute', 'Violin', 'Viola', 'Cello', 'Bass', 'Conductor', 'Arranger', 'Composer'],
              'Software' :
                  ['C#', 'F#', 'C++', 'Java', 'User Interface', 'HTML5', 'CSS3', 'Node.js', 'Python', 'Django',
                   'JavaScript', 'ASP.NET', 'SQL'],
              'Graphic Design' :
                  ['Drawing', 'Painting', 'Mixed Media', 'Illustration', 'Adobe Illustrator', 'Typography', 'Adobe Photoshop'],
              'Planning' : # need more details here
                  ['PMP'],
              # partially per wikipedia: http://en.wikipedia.org/wiki/List_of_engineering_branches#Mechanical_engineering
              'Mechanical Engineering' :
                  ['Acoustical', 'Manufacturing', 'Thermal', 'Vehicle', 'Oil/Petroleum', 'Fluid dynamics'],
              'EmptyCategoryTest' : [],
            }
        print("Adding default categories")
        for categoryName in categoryList:
            skillList = categoryList[categoryName]
            category = Category(categoryName, 'no description available')
            db.session.add(category)
            db.session.commit()
            for skillName in skillList:
                skill = Skill(category.id, skillName, 'no skill description available')
                db.session.add(skill)
            # at the end of the skills ... one last commit
            db.session.commit()

        print("Adding a couple of existing skills to our sample users ... ")

        mechEngrCategory = None
        mechSkill = None
        mechEngrCategory = Category.query.filter_by(name = 'Mechanical Engineering').first()
        if (mechEngrCategory != None):
            mechSkill = Skill.query.filter_by(name = 'Thermal').first()

        softwareCategory = None
        softwareSkillHtml5 = None
        softwareSkillCSharp = None
        softwareSkillJava = None
        softwareCategory = Category.query.filter_by(name = 'Software').first()
        if (softwareCategory != None):
            softwareSkillHtml5 = Skill.query.filter_by(name = 'HTML5').first()
            softwareSkillCSharp = Skill.query.filter_by(name = 'C#').first()
            softwareSkillJava = Skill.query.filter_by(name = 'Java').first()

        print("Checking the new category -> skill relationship ... ")
        if (softwareCategory != None):
            mySkillList = softwareCategory.skillList
            for skill in mySkillList:
                print( skill )
        print("Checking the new skill -> category relationship ... ")
        if (softwareSkillCSharp != None):
            myCategory = softwareSkillCSharp.category
            print myCategory

        print("Checking out the sally user ... ")
        user = User.query.filter_by(username='sally.smith').first()
        if (user != None):
            print(user)
            if (user.seekerProfile):
                print(user.seekerProfile)
            else:
                print("No seeker profile found.")
            if (user.providerProfile):
                print(user.providerProfile)
            else:
                print("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)
            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)

        print("Checking out the steve user ... ")
        user = User.query.filter_by(username='steve').first()
        if (user != None):
            print(user)
            if (user.seekerProfile):
                print(user.seekerProfile)
            else:
                print("No seeker profile found.")
            if (user.providerProfile):
                print(user.providerProfile)
            else:
                print("No provider profile found.")
            if (softwareSkillCSharp != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)
            if (softwareSkillJava != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)











