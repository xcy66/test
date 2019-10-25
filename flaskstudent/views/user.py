from flask import Blueprint,render_template,request,redirect
from App.models import Grade,Student,Permission,User,Role
from App.models import db
from flask import session
from datetime import datetime

user = Blueprint('user',__name__,template_folder="../templates")

# ******************
# 登录
@user.route('/login',methods=['GET','POST'])
def Login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not all([username,password]):
            msg = '*请填写好完整信息'
            return render_template('login.html',msg=msg)
        user_obj = User.query.filter(User.username==username,User.password==password).first()
        if user_obj:
            session['user'] = username
            print('user:',session['user'])
            return redirect('/user/index')
        else:
            msg = '*用户名或者密码错误'
            return render_template('login.html',msg=msg)

@user.route('/register',methods=['GET','POST'])
def Register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        pwd1 = request.form['pwd1']
        user_obj = User.query.filter(User.username == username).first()
        if user_obj:
            return render_template('register.html')
        else:
            new_user = User(username=username,password=pwd1)
            db.session.add_all([new_user])
            db.session.commit()
            return redirect('/user/login')

@user.route('/index')
def Index():
    return render_template('index.html')

@user.route('/head/',methods=['GET','POST'])
def Head():
    if request.method == 'GET':
        user = session['user']
        return render_template('head.html',user=user)


@user.route('/left/',methods=['GET','POST'])
def Left():
    if  request.method == 'GET':
        # user = session.get('username')
        permissions = Permission.query.all()
        # permissions = User.query.filter_by(username=user).first().role().permission
        return render_template('left.html',permissions=permissions)

# 班级管理
# 班级列表
@user.route('/grade/',methods=['GET','POST'])
def grade_list():
    """
    显示班级列表
    """
    if request.method == 'GET':
        #查询第几页的数据
        page  = int(request.args.get('page',1))
        #每页的数据条数
        page_num = int(request.args.get('page_num',5))

        paginate = Grade.query.order_by('g_id').paginate(page,page_num)
        #获取每页的具体数据
        grades = paginate.items
        return render_template('grade.html',grades=grades,paginate=paginate)

# 编辑班级
import time
@user.route('/edit_grade/<g_id>',methods=['GET','POST'])
def edit_grades(g_id):
    edit_grade = Grade.query.filter_by(g_id=g_id).first()
    if request.method=='GET':
        return render_template('edit_grade.html',eg=edit_grade)
    else:
        g_name = request.form['g_name']
        eg_name_list = Grade.query.filter_by(g_name=g_name).first()
        now_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if eg_name_list:
            msg = '班级名称重复'
            return render_template('edit_grade.html',eg=edit_grade,msg=msg)
        else:
            edit_grade.g_name = g_name
            edit_grade.g_create_time = now_time
            db.session.commit()
            msg = '更改成功'
            return render_template('edit_grade.html',eg=edit_grade,msg=msg)

# 查看班级的学生
@user.route('/grade_student/<g_id>/',methods=['GET','POST'])
def grade_students(g_id):
    if request.method == 'GET':
        grade_students_list = Student.query.filter_by(grade_id=g_id).all()
        return render_template('grade_student.html',gs_list = grade_students_list)

# 删除班级列表中的班级
@user.route('/grade_delete/<g_id>/',methods=['GET','POST'])
def grade_delete(g_id):
    if request.method=='GET':
        grade_deletes = Grade.query.filter_by(g_id=g_id).delete()
        db.session.commit()
        return redirect('/user/grade/')
#添加班级
@user.route('/addgrade/',methods=['GET','POST'])
def grade_add():
    if request.method == 'GET':
        return render_template('addgrade.html')
    else:
        g_name = request.form['g_name']
        g_name_list = Grade.query.filter_by(g_name=g_name).first()
        if g_name_list:
            msg = '班级名称重复'
            return render_template('addgrade.html',msg=msg)
        else:
            grade_adds = Grade(g_name=g_name)
            db.session.add(grade_adds)
            db.session.commit()
            msg = '提交成功'
            return render_template('addgrade.html',g_name=g_name,msg=msg)



# *******************
# 学生管理
@user.route('/student/',methods=['GET','POST'])
def student_list():
    """
    显示学生列表
    """
    if request.method == 'GET':
        #查询第几页的数据
        page  = int(request.args.get('page',1))
        #每页的数据条数
        page_num = int(request.args.get('page_num',5))

        paginate = Student.query.order_by('s_id').paginate(page,page_num)
        #获取每页的具体数据
        stus = paginate.items
        return render_template('student.html',stus=stus,paginate=paginate)
# 删除学生列表学生
@user.route('/student_list/<s_id>',methods=['GET','POST'])
def student_delete(s_id):
    if request.method=='GET':
        student_deletes = Student.query.filter_by(s_id=s_id).delete()
        db.session.commit()
        return redirect('/user/student/')

#添加学生
@user.route('/addstu/',methods=['GET','POST'])
def student_add():
    grades = Grade.query.all()
    if request.method == 'GET':
        return render_template('addstu.html',grades=grades)
    else:
        s_name = request.form['s_name']
        s_sex = request.form['s_sex']
        g_name = request.form['g_name']
        s_names = Student.query.filter_by(s_name=s_name).first()
        if s_names:
            msg = '该名字已存在'
            return render_template('addstu.html', s_name=s_name, msg=msg, grades=grades)
        else:
            student_adds = Student(s_name=s_name,s_sex=s_sex,grade_id=g_name)
            db.session.add(student_adds)
            db.session.commit()
            msg = '添加成功'
            return render_template('addstu.html',s_name=s_name,msg=msg,grades=grades)





#*****************************
# 角色管理
# 角色列表
@user.route('/roles/',methods=['GET','POST'])
def roles_list():
    if request.method == "GET":
        roles = Role.query.order_by('r_id')
        return render_template('roles.html',roles=roles)

# 查看权限
@user.route('/userperlist/<r_id>',methods=["GET","POST"])
def Userper_list(r_id):
    if request.method == 'GET':
        r_name = Role.query.filter_by(r_id=r_id).first()
        userper_lists = r_name.permission
        return render_template('userperlist.html',rm=r_name,s=userper_lists)

# 添加权限
@user.route('/adduserper/<r_id>',methods=["GET","POST"])
def Adduserper(r_id):
    userper_lists = Permission.query.all()
    if request.method == 'GET':
        return render_template('adduserper.html',s=userper_lists)
    else:
        r = Role.query.get(r_id)
        userpers = request.form['p_name']
        users =  Permission.query.filter_by(p_name=userpers).first()
        if users in r.permission:
            msg = "权限已存在"
            return render_template('adduserper.html', msg=msg, s=userper_lists)
        else:
            msg = '添加成功'
            r.permission.append(users)
            db.session.commit()
            print(users)
            return render_template('adduserper.html',msg = msg,s=userper_lists)

# 删除权限
@user.route('/subuserper/<r_id>',methods=['GET','POST'])
def Subuserper(r_id):
    if request.method == 'GET':
        r_name = Role.query.filter_by(r_id=r_id).first()
        userper_lists = r_name.permission
        session['a'] = r_id
        return render_template('subuserper.html',rm=r_name,s=userper_lists)

@user.route('/sdelete/<p_id>',methods=['GET','POST'])
def Sdeletes(p_id):
    b = session.get('a')
    if request.method == 'GET':
        a = Role.query.filter_by(r_id = b).first()
        s = Permission.query.filter_by(p_id=p_id).first()
        a.permission.remove(s)
        db.session.commit()
        return redirect('/user/roles/')







# 添加角色
@user.route('/addroles/',methods=['GET',"POST"])
def roles_add():
    if request.method == "GET":
        return render_template('addroles.html')
    else:
        r_name = request.form['r_name']
        rname = Role.query.filter_by(r_name=r_name).first()
        if rname:
            msg='角色名称已存在'
            return render_template('addroles.html', msg=msg)
        else:
            r_names = Role(r_name=r_name)
            db.session.add(r_names)
            db.session.commit()
            msg='添加成功'
            return render_template('addroles.html',msg=msg)

# 权限列表
@user.route('/permissions/',methods=['GET','POST'])
def permissions_list():
    if request.method == 'GET':
        permissions = Permission.query.all()
        return render_template('permissions.html',permissions=permissions)
# 编辑权限
@user.route('/eidtorpermission/<p_id>',methods=['GET','POST'])
def Eeidtorpermission(p_id):
    per = Permission.query.filter_by(p_id=p_id).first()
    if request.method == 'GET':
        return render_template('eidtorpermission.html',per=per)
    else:
        p_name = request.form['p_name']
        p_er = request.form['p_er']
        p_names = Permission.query.filter_by(p_name=p_name).first()
        if p_names:
            msg = '名字重复'
            return render_template('eidtorpermission.html',per=per,msg=msg)
        else:
            per.p_name = p_name
            per.p_er = p_er
            db.session.commit()
            msg = '更改成功'
            return render_template('eidtorpermission.html',per=per,msg=msg)




# 删除权限
@user.route('/perdelete/<p_id>/',methods=['POST','GET'])
def per_delete(p_id):
    if request.method=='GET':
        per_deletes = Permission.query.filter_by(p_id=p_id).delete()
        db.session.commit()
        return redirect('/user/permissions/')

# 添加权限
@user.route('/addpermission/',methods=['GET',"POST"])
def addpermission():
    if request.method == "GET":
        return render_template('addpermission.html')
    else:
        p_name = request.form['p_name']
        p_er = request.form['p_er']
        pname = Permission.query.filter_by(p_name=p_name).first()
        if pname:
            msg='权限已存在'
            return render_template('addpermission.html', msg=msg)
        else:
            p_names = Permission(p_name=p_name,p_er=p_er)
            db.session.add(p_names)
            db.session.commit()
            msg='添加成功'
            return render_template('addpermission.html',msg=msg,p_name=p_name,p_er=p_er)


# 用户管理
# 用户列表
@user.route('/userlist/',methods=['GET','POST'])
def user_list():
    if request.method == 'GET':
        # 查询第几页的数据
        page = int(request.args.get('page', 1))
        # 每页的数据条数
        page_num = int(request.args.get('page_num', 5))
        paginate = User.query.order_by('u_id').paginate(page, page_num)
        # 获取每页的具体数据
        users = paginate.items
        return render_template('users.html', users=users, paginate=paginate)
# 分配角色
@user.route('/assignrole/<u_id>',methods=['GET','POST'])
def Aassignrole(u_id):
    roles = Role.query.all()
    if request.method == 'GET':
        return render_template('assign_user_role.html',roles=roles)
    else:
        s = request.form['r_id']
        ss = User.query.filter_by(u_id=u_id).first()
        if  s == str(ss.role_id):
            msg = '权限已存在'
            return render_template('assign_user_role.html', roles=roles, msg=msg)
        else:
            msg = '更改成功'
            ss.role_id = s
            db.session.commit()
            return render_template('assign_user_role.html', roles=roles, msg=msg)





# 删除用户
@user.route('/userdelete/<u_id>',methods=['POST','GET'])
def user_delete(u_id):
    if request.method=='GET':
        user_deletes = User.query.filter_by(u_id=u_id).delete()
        db.session.commit()
        return redirect('/user/userlist/')



# 添加用户
@user.route('/adduser/',methods=['GET',"POST"])
def adduser():
    if request.method == "GET":
        return render_template('adduser.html')
    else:
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        usernames = User.query.filter_by(username=username).first()
        if usernames or password1 != password2:
            msg='添加失败'
            return render_template('adduser.html', msg=msg)
        else:
            usersnames = User(username=username,password=password1)
            db.session.add(usersnames)
            db.session.commit()
            msg='添加成功'
            return render_template('adduser.html',msg=msg)


# 系统管理
# 修改密码
@user.route('/changepwd/',methods=['GET',"POST"])
def Cchangepwd():
    users = session.get('user')

    user = User.query.filter_by(username=users).first()
    if request.method == "GET":
        return render_template('changepwd.html',user=user)
    else:
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']
        pwd3 = request.form['pwd3']
        if pwd1 != user.password:
            msg = '密码错误'
            return render_template('changepwd.html', user=user,msg=msg)
        elif pwd2 != pwd3:
            msg = '两次密码不一致'
            return render_template('changepwd.html', user=user, msg=msg)
        else:
            user.password = pwd2
            db.session.commit()
            return render_template('changepwdsu.html')



# 退出
@user.route('/logout/',methods=['GET',"POST"])
def Llogout():
    return redirect('/user/login')









