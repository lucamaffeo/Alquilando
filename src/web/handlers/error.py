from dataclasses import dataclass
from flask import render_template


@dataclass
class Error:
    code: int
    message: str
    description: str


def error_not_found(e):
    error = Error(404, "Not Found",
                  "The Requested URL was not found on the server.")

    return render_template('error.html', error=error), 404


def forbidden(e):
    error = Error(403, "Forbidden", "You shouldn't be here!")

    return render_template('error.html', error=error), 403


def error_unauthorized(e):
    error = Error(401, "Unauthorized",
                  "You are not authorized to view this page.")

    return render_template('error.html', error=error), 401
