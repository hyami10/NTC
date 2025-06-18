from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from src.models.course import Course, Lesson, Quiz, Question
from src.models.progress import UserProgress, UserQuizResult
from src.main import db

learning_bp = Blueprint('learning', __name__, url_prefix='/learning')

@learning_bp.route('/')
def index():
    """Halaman utama learning path"""
    courses = Course.query.order_by(Course.order).all()
    
    # Jika user sudah login, ambil progress mereka
    completed_lessons = []
    if current_user.is_authenticated:
        completed_lessons = current_user.get_completed_lessons()
    
    return render_template('learning/index.html', 
                          courses=courses,
                          completed_lessons=completed_lessons)

@learning_bp.route('/course/<int:course_id>')
def course(course_id):
    """Halaman detail course"""
    course = Course.query.get_or_404(course_id)
    lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()
    
    # Jika user sudah login, ambil progress mereka
    completed_lessons = []
    if current_user.is_authenticated:
        completed_lessons = current_user.get_completed_lessons()
    
    return render_template('learning/course.html', 
                          course=course,
                          lessons=lessons,
                          completed_lessons=completed_lessons)

@learning_bp.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    """Halaman detail lesson"""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = Course.query.get(lesson.course_id)
    
    # Jika user sudah login, catat progress
    if current_user.is_authenticated:
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            lesson_id=lesson_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                lesson_id=lesson_id,
                course_id=lesson.course_id
            )
            db.session.add(progress)
        
        progress.last_accessed = db.func.now()
        db.session.commit()
    
    # Ambil quiz jika ada
    quiz = Quiz.query.filter_by(lesson_id=lesson_id).first()
    
    return render_template('learning/lesson.html', 
                          lesson=lesson,
                          course=course,
                          quiz=quiz)

@learning_bp.route('/complete_lesson/<int:lesson_id>')
@login_required
def complete_lesson(lesson_id):
    """Menandai lesson sebagai selesai"""
    lesson = Lesson.query.get_or_404(lesson_id)
    
    progress = UserProgress.query.filter_by(
        user_id=current_user.id,
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            course_id=lesson.course_id
        )
        db.session.add(progress)
    
    progress.completed = True
    db.session.commit()
    
    flash('Lesson berhasil ditandai selesai!', 'success')
    return redirect(url_for('learning.lesson', lesson_id=lesson_id))

@learning_bp.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    """Halaman quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    if request.method == 'POST':
        score = 0
        max_score = len(questions)
        
        for question in questions:
            selected_option = request.form.get(f'question_{question.id}')
            if selected_option:
                for option in question.options:
                    if str(option.id) == selected_option and option.is_correct:
                        score += 1
        
        # Simpan hasil quiz
        result = UserQuizResult(
            user_id=current_user.id,
            quiz_id=quiz_id,
            score=score,
            max_score=max_score
        )
        db.session.add(result)
        
        # Update total score user
        current_user.update_score(score)
        
        # Tandai lesson sebagai selesai
        lesson = Lesson.query.get(quiz.lesson_id)
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            lesson_id=lesson.id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                lesson_id=lesson.id,
                course_id=lesson.course_id
            )
            db.session.add(progress)
        
        progress.completed = True
        db.session.commit()
        
        flash(f'Quiz selesai! Skor Anda: {score}/{max_score}', 'success')
        return redirect(url_for('learning.quiz_result', result_id=result.id))
    
    return render_template('learning/quiz.html', 
                          quiz=quiz,
                          questions=questions)

@learning_bp.route('/quiz_result/<int:result_id>')
@login_required
def quiz_result(result_id):
    """Halaman hasil quiz"""
    result = UserQuizResult.query.get_or_404(result_id)
    
    # Pastikan user hanya bisa melihat hasil quiz miliknya
    if result.user_id != current_user.id:
        flash('Anda tidak memiliki akses ke halaman ini', 'danger')
        return redirect(url_for('learning.index'))
    
    quiz = Quiz.query.get(result.quiz_id)
    lesson = Lesson.query.get(quiz.lesson_id)
    course = Course.query.get(lesson.course_id)
    
    return render_template('learning/quiz_result.html', 
                          result=result,
                          quiz=quiz,
                          lesson=lesson,
                          course=course)
