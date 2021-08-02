import re
from flask import Flask, render_template, request, flash, redirect, url_for, session

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# 비밀번호 암호화 관련
from werkzeug.security import generate_password_hash, check_password_hash

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    # ORM 관련
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    from .models import User, Board

    @app.route('/')
    def hello_pybo():
        content_list = Board.query.all()  # 모든 게시글 
        return render_template('index.html', content_list = content_list)

    # 회원가입
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET' :
            return render_template('signup.html')
        else :  
            n_id = request.form['new_id']
            n_pw = request.form['new_pw']
            n_pw2 = request.form['new_pw2']

            old_user = User.query.filter_by(user_id=n_id).first()
            # 1.비밀번호 != 비밀번호 확인
            if n_pw != n_pw2 : 
                flash("비밀번호 입력이 잘못되었습니다.")
                return render_template('signup.html')
            # 2.아이디 중복인 경우
            elif old_user :
                flash("이미 존재하는 사용자입니다.")
                return render_template('signup.html')
            # 중복되는 아이디 없고, 비밀번호와 비밀번호 확인이 일치할 경우, 회원정보 저장
            else :
                new_user = User(user_id = n_id, user_pw = generate_password_hash(n_pw))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('hello_pybo'))
            
            
    # 로그인
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET' :
            return render_template('login.html')
        else : 
            input_id = request.form['login_id']
            input_pw = request.form['login_pw']
            user = User.query.filter_by(user_id=input_id).first()
            if not user :
                flash("존재하지 않는 사용자입니다.")
                return redirect(url_for('login'))
            
            elif check_password_hash(input_pw, user.user_pw) :
                flash("비밀번호가 올바르지 않습니다.")
                return redirect(url_for('login'))
            else :
                session.clear()
                session['user_id'] = user.user_id
                return redirect(url_for('hello_pybo'))

    # 로그아웃
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('hello_pybo'))
    
    
    # 게시글 작성
    @app.route('/create', methods=['GET', 'POST'] )
    def create():
        if request.method =='GET' :
            return render_template('create.html')
        else :
            title = request.form['title']
            content = request.form['content']
            user_id = session['user_id'] 
            new_board = Board(title = title, content = content, user_id = user_id)
            db.session.add(new_board)
            db.session.commit()
            return redirect(url_for('hello_pybo'))
        
    # 게시글 보기
    @app.route('/detail/<int:content_id>')
    def detail(content_id):
        content = Board.query.get(content_id)
        return render_template('detail.html', content = content)
        
    return app
