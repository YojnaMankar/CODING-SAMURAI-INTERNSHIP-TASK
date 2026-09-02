import os
import sqlite3
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import generate_password_hash, check_password_hash

from database import init_db, get_db, close_db


app = Flask(__name__)

# Use an environment variable in production.
app.secret_key = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-before-deployment"
)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# -----------------------------------
# Database
# -----------------------------------

app.teardown_appcontext(close_db)


# -----------------------------------
# Authentication
# -----------------------------------

def login_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped


# -----------------------------------
# Home / Blog
# -----------------------------------

@app.route("/")
def index():

    db = get_db()

    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()


    query = """
        SELECT
            posts.*,
            users.username,

            (
                SELECT COUNT(*)
                FROM likes
                WHERE likes.post_id = posts.id
            ) AS like_count,

            (
                SELECT COUNT(*)
                FROM comments
                WHERE comments.post_id = posts.id
            ) AS comment_count

        FROM posts

        JOIN users
            ON posts.user_id = users.id

        WHERE 1=1
    """


    params = []


    # SEARCH

    if search:

        query += """
            AND (
                posts.title LIKE ?
                OR posts.content LIKE ?
                OR users.username LIKE ?
                OR posts.category LIKE ?
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value,
            search_value,
            search_value
        ])


    # CATEGORY FILTER

    if category:

        query += """
            AND posts.category = ?
        """

        params.append(category)


    # SORT

    query += """
        ORDER BY posts.created_at DESC
    """


    posts = db.execute(
        query,
        params
    ).fetchall()


    # CATEGORIES

    categories = db.execute("""
        SELECT DISTINCT category

        FROM posts

        WHERE category IS NOT NULL
        AND category != ''

        ORDER BY category
    """).fetchall()


    return render_template(
        "index.html",

        posts=posts,

        categories=categories,

        search=search,

        selected_category=category
    )




# -----------------------------------
# Register
# -----------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username:
            flash("Username is required.")
            return redirect(url_for("register"))

        if len(username) < 3:
            flash("Username must be at least 3 characters.")
            return redirect(url_for("register"))

        if len(password) < 4:
            flash("Password must be at least 4 characters.")
            return redirect(url_for("register"))

        db = get_db()

        try:

            db.execute(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?)
                """,
                (
                    username,
                    generate_password_hash(password)
                )
            )

            db.commit()

            flash("Registration successful. Please log in.")

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            flash("Username already exists. Please choose another.")

            return redirect(url_for("register"))

    return render_template("register.html")


# -----------------------------------
# Login
# -----------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        db = get_db()

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash("Welcome back!")

            return redirect(url_for("index"))

        flash("Invalid username or password.")

    return render_template("login.html")

# -----------------------------------
# Create New Post
# -----------------------------------

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    db = get_db()

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        category = request.form.get("category", "General").strip()

        if not title or not content:
            flash("Title and content are required.")
            return render_template("create.html")

        if not category:
            category = "General"

        db.execute(
            """
            INSERT INTO posts
            (title, content, user_id, category)
            VALUES (?, ?, ?, ?)
            """,
            (
                title,
                content,
                session["user_id"],
                category
            )
        )

        db.commit()

        flash("Post created successfully!")

        return redirect(url_for("dashboard"))

    return render_template("create.html")


# -----------------------------------
# dashboard
# -----------------------------------

@app.route("/dashboard")
@login_required
def dashboard():

    db = get_db()

    # Total posts
    total_posts = db.execute(
        """
        SELECT COUNT(*)
        FROM posts
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]

    # Categories
    category_count = db.execute(
        """
        SELECT COUNT(DISTINCT category)
        FROM posts
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]

    # Recent posts with Like + Comment counts
    recent_posts = db.execute(
        """
        SELECT
            posts.*,

            (
                SELECT COUNT(*)
                FROM likes
                WHERE likes.post_id = posts.id
            ) AS like_count,

            (
                SELECT COUNT(*)
                FROM comments
                WHERE comments.post_id = posts.id
            ) AS comment_count

        FROM posts

        WHERE posts.user_id = ?

        ORDER BY posts.created_at DESC

        LIMIT 5
        """,
        (session["user_id"],)
    ).fetchall()

    return render_template(
        "dashboard.html",
        total_posts=total_posts,
        category_count=category_count,
        recent_posts=recent_posts
    )


    # -----------------------------------
    # Comments for dashboard posts
    # -----------------------------------

    dashboard_comments = {}

    for post in recent_posts:

        comments = db.execute(
            """
            SELECT
                comments.*,
                users.username
            FROM comments
            JOIN users
                ON comments.user_id = users.id
            WHERE comments.post_id = ?
            ORDER BY comments.created_at DESC
            """,
            (post["id"],)
        ).fetchall()

        dashboard_comments[post["id"]] = comments


    return render_template(
        "dashboard.html",

        total_posts=total_posts,

        category_count=category_count,

        recent_posts=recent_posts,

        dashboard_comments=dashboard_comments
    )


# -----------------------------------
# Logout
# -----------------------------------

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.")

    return redirect(url_for("index"))


# -----------------------------------
# Edit Post
# -----------------------------------

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit(post_id):

    db = get_db()

    post = db.execute(
        """
        SELECT *
        FROM posts
        WHERE id = ?
        """,
        (post_id,)
    ).fetchone()

    if not post:

        flash("Post not found.")

        return redirect(url_for("index"))

    # Only owner can edit
    if post["user_id"] != session["user_id"]:

        flash("You cannot edit this post.")

        return redirect(url_for("index"))

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        category = request.form.get(
            "category",
            "General"
        ).strip()

        if not category:
            category = "General"

        if not title or not content:

            flash("Title and content are required.")

            return redirect(
                url_for(
                    "edit",
                    post_id=post_id
                )
            )

        db.execute(
            """
            UPDATE posts
            SET title = ?,
                content = ?,
                category = ?
            WHERE id = ?
            """,
            (
                title,
                content,
                category,
                post_id
            )
        )

        db.commit()

        flash("Post updated successfully!")

        return redirect(url_for("index"))

    return render_template(
        "edit.html",
        post=post
    )

# -----------------------------------
# Like / Unlike Post
# -----------------------------------

@app.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):

    db = get_db()

    # Check that the post exists
    post = db.execute(
        "SELECT id FROM posts WHERE id = ?",
        (post_id,)
    ).fetchone()

    if not post:
        flash("Post not found.")
        return redirect(url_for("index"))

    # Check whether this user already liked the post
    existing_like = db.execute(
        """
        SELECT id
        FROM likes
        WHERE user_id = ? AND post_id = ?
        """,
        (
            session["user_id"],
            post_id
        )
    ).fetchone()

    if existing_like:

        # Unlike
        db.execute(
            "DELETE FROM likes WHERE id = ?",
            (existing_like["id"],)
        )

    else:

        # Like
        db.execute(
            """
            INSERT INTO likes (user_id, post_id)
            VALUES (?, ?)
            """,
            (
                session["user_id"],
                post_id
            )
        )

    db.commit()

    return redirect(request.referrer or url_for("index"))


# -----------------------------------
# Add Comment
# -----------------------------------

@app.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def add_comment(post_id):

    db = get_db()

    # Check if post exists
    post = db.execute(
        """
        SELECT id
        FROM posts
        WHERE id = ?
        """,
        (post_id,)
    ).fetchone()

    if not post:
        flash("Post not found.")
        return redirect(url_for("index"))

    comment = request.form.get("comment", "").strip()

    if not comment:
        flash("Comment cannot be empty.")
        return redirect(
            url_for(
                "post_detail",
                post_id=post_id
            )
        )

    if len(comment) > 500:
        flash("Comment must be 500 characters or less.")
        return redirect(
            url_for(
                "post_detail",
                post_id=post_id
            )
        )

    db.execute(
        """
        INSERT INTO comments
        (content, user_id, post_id)
        VALUES (?, ?, ?)
        """,
        (
            comment,
            session["user_id"],
            post_id
        )
    )

    db.commit()

    flash("Comment added successfully!")

    return redirect(
        url_for(
            "post_detail",
            post_id=post_id
        )
    )


# -----------------------------------
# Delete Comment
# -----------------------------------

@app.route("/comment/delete/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):

    db = get_db()

    comment = db.execute(
        """
        SELECT *
        FROM comments
        WHERE id = ?
        """,
        (comment_id,)
    ).fetchone()

    if not comment:
        flash("Comment not found.")
        return redirect(url_for("index"))

    # Only comment owner can delete it
    if comment["user_id"] != session["user_id"]:
        flash("You cannot delete this comment.")
        return redirect(
            url_for(
                "post_detail",
                post_id=comment["post_id"]
            )
        )

    post_id = comment["post_id"]

    db.execute(
        """
        DELETE FROM comments
        WHERE id = ?
        """,
        (comment_id,)
    )

    db.commit()

    flash("Comment deleted successfully!")

    return redirect(
        url_for(
            "post_detail",
            post_id=post_id
        )
    )
    
# -----------------------------------
# Delete Post
# -----------------------------------

@app.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete(post_id):

    db = get_db()

    post = db.execute(
        """
        SELECT *
        FROM posts
        WHERE id = ?
        """,
        (post_id,)
    ).fetchone()

    if post and post["user_id"] == session["user_id"]:

        db.execute(
            """
            DELETE FROM posts
            WHERE id = ?
            """,
            (post_id,)
        )

        db.commit()

        flash("Post deleted successfully.")

    else:

        flash("You cannot delete this post.")

    return redirect(url_for("index"))

@app.route("/post/<int:post_id>")
def post_detail(post_id):

    db = get_db()

    # Get post
    post = db.execute(
        """
        SELECT posts.*, users.username
        FROM posts
        JOIN users
            ON posts.user_id = users.id
        WHERE posts.id = ?
        """,
        (post_id,)
    ).fetchone()

    if not post:
        flash("Post not found.")
        return redirect(url_for("index"))

    # Get comments
    comments = db.execute(
        """
        SELECT
            comments.*,
            users.username
        FROM comments
        JOIN users
            ON comments.user_id = users.id
        WHERE comments.post_id = ?
        ORDER BY comments.created_at DESC
        """,
        (post_id,)
    ).fetchall()

    # Get total likes
    like_count = db.execute(
        """
        SELECT COUNT(*)
        FROM likes
        WHERE post_id = ?
        """,
        (post_id,)
    ).fetchone()[0]

    return render_template(
        "post_detail.html",
        post=post,
        comments=comments,
        like_count=like_count
    )

# -----------------------------------
# User Profile
# -----------------------------------

@app.route("/profile")
@login_required
def profile():

    db = get_db()

    # Current user
    user = db.execute(
        """
        SELECT id, username
        FROM users
        WHERE id = ?
        """,
        (session["user_id"],)
    ).fetchone()

    if not user:
        session.clear()
        flash("User account not found.")
        return redirect(url_for("login"))


    # User's posts
    posts = db.execute(
        """
        SELECT
            posts.*,
            (
                SELECT COUNT(*)
                FROM likes
                WHERE likes.post_id = posts.id
            ) AS like_count,
            (
                SELECT COUNT(*)
                FROM comments
                WHERE comments.post_id = posts.id
            ) AS comment_count
        FROM posts
        WHERE posts.user_id = ?
        ORDER BY posts.created_at DESC
        """,
        (session["user_id"],)
    ).fetchall()


    # Total posts
    total_posts = db.execute(
        """
        SELECT COUNT(*)
        FROM posts
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]


    # Total likes received
    total_likes = db.execute(
        """
        SELECT COUNT(*)
        FROM likes
        JOIN posts
            ON likes.post_id = posts.id
        WHERE posts.user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]


    # Total comments written
    total_comments = db.execute(
        """
        SELECT COUNT(*)
        FROM comments
        WHERE user_id = ?
        """,
        (session["user_id"],)
    ).fetchone()[0]


    return render_template(
        "profile.html",
        user=user,
        posts=posts,
        total_posts=total_posts,
        total_likes=total_likes,
        total_comments=total_comments
    )


# -----------------------------------
# Run Application
# -----------------------------------

if __name__ == "__main__":

    with app.app_context():
        init_db()

    app.run(debug=True)