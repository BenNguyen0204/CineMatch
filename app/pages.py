from flask import Blueprint, jsonify, render_template
from flask_login import login_required

blueprint = Blueprint("pages", __name__)

@blueprint.route("/")
@login_required
def index():
    return render_template("index.html")

@blueprint.get("/healthz")
def healthz():
    return jsonify(status = "ok")