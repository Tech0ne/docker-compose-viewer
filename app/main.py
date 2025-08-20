from flask import Blueprint, redirect, render_template, request, url_for

from .api import get_nodes_and_links

main = Blueprint("main", __name__)


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/")
def home():
    return render_template("main.html")


@main.errorhandler(Exception)
def error():
    return redirect(url_for("fail"))


@main.route("/fail")
def fail():
    return render_template("fail.html")


@main.route("/view", methods=["POST"])
def view_file():
    file = request.files.get("file")
    if not file:
        return redirect(url_for("fail"))

    output, nodes, links = get_nodes_and_links(file)
    if not output:
        return redirect(url_for("fail"))

    return render_template("view.html", nodes=nodes, links=links)
