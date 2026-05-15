import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import init_db

app = Flask(__name__)

app.secret_key = '5d1883eba628fd1ed2824748fd9229307b713ed77e34d51c'

# ─── Prevent caching on admin pages ───────────────────────
@app.after_request
def prevent_caching(response):
    if request.path.startswith('/admin'):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

init_db()

# ─── Helpers ──────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

def public_route(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' in session:
            session.clear()
            return redirect(url_for(f.__name__, **request.args))
        return f(*args, **kwargs)
    return decorated

# ─── Public routes ────────────────────────────────────────
@app.route('/')
@public_route
def index():
    db = get_db()
    solutions = db.execute(
        'SELECT * FROM solution ORDER BY display_order'
    ).fetchall()
    testimonials = db.execute(
        'SELECT * FROM testimonial WHERE approved = 1 ORDER BY created_at DESC'
    ).fetchall()
    db.close()
    return render_template('public/index.html',
                           solutions=solutions,
                           testimonials=testimonials)

@app.route('/solutions')
@public_route
def solutions():
    db = get_db()
    solutions = db.execute(
        'SELECT * FROM solution ORDER BY display_order'
    ).fetchall()
    db.close()
    return render_template('public/solutions.html', solutions=solutions)

@app.route('/case-studies')
@public_route
def case_studies():
    db = get_db()
    case_studies = db.execute(
        'SELECT * FROM case_study ORDER BY created_at DESC'
    ).fetchall()
    db.close()
    return render_template('public/case_studies.html', case_studies=case_studies)

@app.route('/blog')
@public_route
def blog():
    db = get_db()
    posts = db.execute(
        'SELECT * FROM blog_post WHERE status = ? ORDER BY published_at DESC',
        ('published',)
    ).fetchall()
    db.close()
    return render_template('public/blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
@public_route
def blog_post(post_id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM blog_post WHERE id = ? AND status = ?',
        (post_id, 'published')
    ).fetchone()
    db.close()
    if post is None:
        return redirect(url_for('blog'))
    return render_template('public/blog_post.html', post=post)

@app.route('/testimonials', methods=['GET', 'POST'])
@public_route
def testimonials():
    db = get_db()
    if request.method == 'POST':
        client_name = request.form.get('client_name', '').strip()
        company     = request.form.get('company', '').strip()
        rating      = request.form.get('rating', '').strip()
        content     = request.form.get('content', '').strip()

        errors = []
        if not client_name:
            errors.append('Name is required.')
        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
            errors.append('A valid star rating between 1 and 5 is required.')
        if not content:
            errors.append('Testimonial message is required.')

        if errors:
            testimonials = db.execute(
                'SELECT * FROM testimonial WHERE approved = 1 ORDER BY created_at DESC'
            ).fetchall()
            db.close()
            return render_template('public/testimonials.html',
                                   testimonials=testimonials,
                                   errors=errors,
                                   form_data=request.form)

        db.execute(
            '''INSERT INTO testimonial (client_name, company, rating, content)
               VALUES (?, ?, ?, ?)''',
            (client_name, company or None, int(rating), content)
        )
        db.commit()
        db.close()
        return redirect(url_for('testimonials', submitted=1))

    submitted = request.args.get('submitted')
    testimonials = db.execute(
        'SELECT * FROM testimonial WHERE approved = 1 ORDER BY created_at DESC'
    ).fetchall()
    db.close()
    return render_template('public/testimonials.html',
                           testimonials=testimonials,
                           submitted=submitted)

@app.route('/gallery')
@public_route
def gallery():
    db = get_db()
    images = db.execute(
        'SELECT * FROM gallery_image ORDER BY updated_at DESC'
    ).fetchall()
    db.close()
    return render_template('public/gallery.html', images=images)

@app.route('/contact', methods=['GET', 'POST'])
@public_route
def contact():
    if request.method == 'POST':
        name         = request.form.get('name', '').strip()
        email        = request.form.get('email', '').strip()
        phone        = request.form.get('phone', '').strip()
        company      = request.form.get('company', '').strip()
        service_type = request.form.get('service_type', '').strip()
        region       = request.form.get('region', '').strip()
        message      = request.form.get('message', '').strip()

        errors = []
        if not name:
            errors.append('Full name is required.')
        if not email:
            errors.append('Email address is required.')
        if not message:
            errors.append('Message is required.')

        if errors:
            return render_template('public/contact.html',
                                   errors=errors,
                                   form_data=request.form)

        db = get_db()
        db.execute(
            '''INSERT INTO inquiry (name, email, phone, company, service_type, region, message)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (name, email, phone or None, company or None,
             service_type or None, region or None, message)
        )
        db.commit()
        db.close()
        return render_template('public/contact.html', submitted=True)

    return render_template('public/contact.html')

# ─── Admin routes ─────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        db = get_db()
        admin = db.execute(
            'SELECT * FROM admin WHERE username = ?', (username,)
        ).fetchone()
        db.close()

        if admin is None:
            error = 'Invalid username or password.'
        elif not check_password_hash(admin['password_hash'], password):
            error = 'Invalid username or password.'
        else:
            session['admin_id']   = admin['id']
            session['admin_name'] = admin['first_name']
            return redirect(url_for('admin_dashboard'))

    return render_template('admin/login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    db = get_db()
    service_filter = request.args.get('service_type', '')

    if service_filter:
        inquiries = db.execute(
            'SELECT * FROM inquiry WHERE service_type = ? ORDER BY submitted_at DESC LIMIT 5',
            (service_filter,)
        ).fetchall()
    else:
        inquiries = db.execute(
            'SELECT * FROM inquiry ORDER BY submitted_at DESC LIMIT 5'
        ).fetchall()

    service_counts = db.execute(
        '''SELECT service_type, COUNT(*) as count
           FROM inquiry
           WHERE service_type IS NOT NULL
           GROUP BY service_type
           ORDER BY count DESC'''
    ).fetchall()

    region_counts = db.execute(
        '''SELECT region, COUNT(*) as count
           FROM inquiry
           WHERE region IS NOT NULL
           GROUP BY region
           ORDER BY count DESC'''
    ).fetchall()

    testimonials = db.execute(
        'SELECT * FROM testimonial ORDER BY created_at DESC'
    ).fetchall()

    service_types = db.execute(
        'SELECT DISTINCT service_type FROM inquiry WHERE service_type IS NOT NULL'
    ).fetchall()

    db.close()
    return render_template('admin/dashboard.html',
                           inquiries=inquiries,
                           service_counts=service_counts,
                           region_counts=region_counts,
                           testimonials=testimonials,
                           service_types=service_types,
                           service_filter=service_filter)

@app.route('/admin/testimonials')
@login_required
def admin_testimonials():
    db = get_db()
    testimonials = db.execute(
        'SELECT * FROM testimonial ORDER BY created_at DESC'
    ).fetchall()
    db.close()
    return render_template('admin/testimonials.html', testimonials=testimonials)

@app.route('/admin/testimonials/<int:testimonial_id>/approve', methods=['POST'])
@login_required
def approve_testimonial(testimonial_id):
    db = get_db()
    db.execute(
        'UPDATE testimonial SET approved = 1, admin_id = ? WHERE id = ?',
        (session['admin_id'], testimonial_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('admin_testimonials'))

@app.route('/admin/testimonials/<int:testimonial_id>/reject', methods=['POST'])
@login_required
def reject_testimonial(testimonial_id):
    db = get_db()
    db.execute(
        'DELETE FROM testimonial WHERE id = ?', (testimonial_id,)
    )
    db.commit()
    db.close()
    return redirect(url_for('admin_testimonials'))

@app.route('/admin/testimonials/<int:testimonial_id>/unpublish', methods=['POST'])
@login_required
def unpublish_testimonial(testimonial_id):
    db = get_db()
    db.execute(
        'UPDATE testimonial SET approved = 0, admin_id = ? WHERE id = ?',
        (session['admin_id'], testimonial_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('admin_testimonials'))

@app.route('/admin/blog')
@login_required
def admin_blog():
    db = get_db()
    category = request.args.get('category', '')
    if category:
        posts = db.execute(
            'SELECT * FROM blog_post WHERE category = ? ORDER BY published_at DESC',
            (category,)
        ).fetchall()
    else:
        posts = db.execute(
            'SELECT * FROM blog_post ORDER BY published_at DESC'
        ).fetchall()
    db.close()
    return render_template('admin/blog.html', posts=posts)

@app.route('/admin/blog/new', methods=['POST'])
@login_required
def admin_blog_new():
    title    = request.form.get('title', '').strip()
    content  = request.form.get('content', '').strip()
    status   = request.form.get('status', 'draft').strip()
    category = request.form.get('category', '').strip()

    if title and content:
        db = get_db()
        db.execute(
            '''INSERT INTO blog_post (admin_id, title, content, category, status, published_at)
               VALUES (?, ?, ?, ?, ?, CASE WHEN ? = 'published'
               THEN CURRENT_TIMESTAMP ELSE NULL END)''',
            (session['admin_id'], title, content, category or None, status, status)
        )
        db.commit()
        db.close()

    return redirect(url_for('admin_blog'))

@app.route('/admin/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_blog_edit(post_id):
    db = get_db()
    post = db.execute(
        'SELECT * FROM blog_post WHERE id = ?', (post_id,)
    ).fetchone()

    if request.method == 'POST':
        title    = request.form.get('title', '').strip()
        content  = request.form.get('content', '').strip()
        status   = request.form.get('status', 'draft').strip()
        category = request.form.get('category', '').strip()

        db.execute(
            '''UPDATE blog_post
               SET title = ?, content = ?, category = ?, status = ?,
                   published_at = CASE WHEN ? = 'published' AND published_at IS NULL
                   THEN CURRENT_TIMESTAMP ELSE published_at END
               WHERE id = ?''',
            (title, content, category or None, status, status, post_id)
        )
        db.commit()
        db.close()
        return redirect(url_for('admin_blog'))

    db.close()
    return render_template('admin/blog.html', post=post)

@app.route('/admin/blog/<int:post_id>/delete', methods=['POST'])
@login_required
def admin_blog_delete(post_id):
    db = get_db()
    db.execute('DELETE FROM blog_post WHERE id = ?', (post_id,))
    db.commit()
    db.close()
    return redirect(url_for('admin_blog'))

@app.route('/admin/gallery')
@login_required
def admin_gallery():
    db = get_db()
    category = request.args.get('category', '')
    if category:
        images = db.execute(
            'SELECT * FROM gallery_image WHERE category = ? ORDER BY updated_at DESC',
            (category,)
        ).fetchall()
    else:
        images = db.execute(
            'SELECT * FROM gallery_image ORDER BY updated_at DESC'
        ).fetchall()
    db.close()
    return render_template('admin/gallery.html', images=images)

@app.route('/admin/gallery/upload', methods=['POST'])
@login_required
def admin_gallery_upload():
    import os
    from werkzeug.utils import secure_filename
    file     = request.files.get('image')
    caption  = request.form.get('caption', '').strip()
    category = request.form.get('category', '').strip()

    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(app.static_folder, 'images', 'gallery')
        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, filename))

        db = get_db()
        db.execute(
            'INSERT INTO gallery_image (admin_id, filename, caption, category) VALUES (?, ?, ?, ?)',
            (session['admin_id'], filename, caption or None, category or None)
        )
        db.commit()
        db.close()

    return redirect(url_for('admin_gallery'))

@app.route('/admin/gallery/<int:image_id>/delete', methods=['POST'])
@login_required
def admin_gallery_delete(image_id):
    db = get_db()
    db.execute('DELETE FROM gallery_image WHERE id = ?', (image_id,))
    db.commit()
    db.close()
    return redirect(url_for('admin_gallery'))

@app.route('/admin/content')
@login_required
def admin_content():
    db = get_db()
    solutions = db.execute(
        'SELECT * FROM solution ORDER BY display_order'
    ).fetchall()
    case_studies = db.execute(
        'SELECT * FROM case_study ORDER BY created_at DESC'
    ).fetchall()
    db.close()
    return render_template('admin/content.html',
                           solutions=solutions,
                           case_studies=case_studies)

# ─── Admin: Solutions CRUD ────────────────────────────────
@app.route('/admin/solutions/new', methods=['POST'])
@login_required
def admin_solution_new():
    title         = request.form.get('title', '').strip()
    description   = request.form.get('description', '').strip()
    icon          = request.form.get('icon', '').strip()
    display_order = request.form.get('display_order', '0').strip()

    if title and description:
        db = get_db()
        db.execute(
            '''INSERT INTO solution (admin_id, title, description, icon, display_order)
               VALUES (?, ?, ?, ?, ?)''',
            (session['admin_id'], title, description,
             icon or None, int(display_order) if display_order.isdigit() else 0)
        )
        db.commit()
        db.close()
        flash('Solution added successfully.', 'success')
    else:
        flash('Title and description are required.', 'danger')

    return redirect(url_for('admin_content'))

@app.route('/admin/solutions/<int:solution_id>/edit', methods=['POST'])
@login_required
def admin_solution_edit(solution_id):
    title         = request.form.get('title', '').strip()
    description   = request.form.get('description', '').strip()
    icon          = request.form.get('icon', '').strip()
    display_order = request.form.get('display_order', '0').strip()

    if title and description:
        db = get_db()
        db.execute(
            '''UPDATE solution
               SET title = ?, description = ?, icon = ?, display_order = ?
               WHERE id = ?''',
            (title, description, icon or None,
             int(display_order) if display_order.isdigit() else 0,
             solution_id)
        )
        db.commit()
        db.close()
        flash('Solution updated successfully.', 'success')
    else:
        flash('Title and description are required.', 'danger')

    return redirect(url_for('admin_content'))

@app.route('/admin/solutions/<int:solution_id>/delete', methods=['POST'])
@login_required
def admin_solution_delete(solution_id):
    db = get_db()
    db.execute('DELETE FROM solution WHERE id = ?', (solution_id,))
    db.commit()
    db.close()
    flash('Solution deleted.', 'success')
    return redirect(url_for('admin_content'))

# ─── Admin: Case Studies CRUD ─────────────────────────────
@app.route('/admin/case-studies/new', methods=['POST'])
@login_required
def admin_case_new():
    title    = request.form.get('title', '').strip()
    client   = request.form.get('client', '').strip()
    industry = request.form.get('industry', '').strip()
    summary  = request.form.get('summary', '').strip()
    content  = request.form.get('content', '').strip()

    if title and client and content:
        db = get_db()
        db.execute(
            '''INSERT INTO case_study (admin_id, title, client, industry, summary, content)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (session['admin_id'], title, client,
             industry or None, summary or None, content)
        )
        db.commit()
        db.close()
        flash('Case study added successfully.', 'success')
    else:
        flash('Title, client, and content are required.', 'danger')

    return redirect(url_for('admin_content'))

@app.route('/admin/case-studies/<int:case_id>/edit', methods=['POST'])
@login_required
def admin_case_edit(case_id):
    title    = request.form.get('title', '').strip()
    client   = request.form.get('client', '').strip()
    industry = request.form.get('industry', '').strip()
    summary  = request.form.get('summary', '').strip()
    content  = request.form.get('content', '').strip()

    if title and client and content:
        db = get_db()
        db.execute(
            '''UPDATE case_study
               SET title = ?, client = ?, industry = ?, summary = ?, content = ?
               WHERE id = ?''',
            (title, client, industry or None, summary or None, content, case_id)
        )
        db.commit()
        db.close()
        flash('Case study updated successfully.', 'success')
    else:
        flash('Title, client, and content are required.', 'danger')

    return redirect(url_for('admin_content'))

@app.route('/admin/case-studies/<int:case_id>/delete', methods=['POST'])
@login_required
def admin_case_delete(case_id):
    db = get_db()
    db.execute('DELETE FROM case_study WHERE id = ?', (case_id,))
    db.commit()
    db.close()
    flash('Case study deleted.', 'success')
    return redirect(url_for('admin_content'))

# ─── Admin: Inquiries ─────────────────────────────────────
@app.route('/admin/inquiries')
@login_required
def admin_inquiries():
    db = get_db()
    service_filter = request.args.get('service_type', '')

    if service_filter:
        inquiries = db.execute(
            'SELECT * FROM inquiry WHERE service_type = ? ORDER BY submitted_at DESC',
            (service_filter,)
        ).fetchall()
    else:
        inquiries = db.execute(
            'SELECT * FROM inquiry ORDER BY submitted_at DESC'
        ).fetchall()

    service_types = db.execute(
        'SELECT DISTINCT service_type FROM inquiry WHERE service_type IS NOT NULL'
    ).fetchall()
    db.close()
    return render_template('admin/inquiries.html',
                           inquiries=inquiries,
                           service_types=service_types,
                           service_filter=service_filter)

@app.route('/admin/inquiries/<int:inquiry_id>/status', methods=['POST'])
@login_required
def admin_inquiry_status(inquiry_id):
    status = request.form.get('status', 'new')
    db = get_db()
    db.execute('UPDATE inquiry SET status = ? WHERE id = ?', (status, inquiry_id))
    db.commit()
    db.close()
    return redirect(url_for('admin_inquiries'))

@app.route('/admin/inquiries/<int:inquiry_id>/delete', methods=['POST'])
@login_required
def admin_inquiry_delete(inquiry_id):
    db = get_db()
    db.execute('DELETE FROM inquiry WHERE id = ?', (inquiry_id,))
    db.commit()
    db.close()
    return redirect(url_for('admin_inquiries'))

# ─── Run ──────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)