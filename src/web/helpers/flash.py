from flask import flash


def flash_validation_errors(errors):
    """Helper function to flash validation errors"""
    for error in errors:
        flash(f"{error.field}: {error.message}", "error")
