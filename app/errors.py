from flask import render_template
from app import app,db

@app.errorhandler(500)
def internal_server_error(e):
    db.session.rollback()
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404

