# utils/response_handler.py
from flask import jsonify
from constants.status_codes import StatusCode
from constants.messages import AuthMessages

class ResponseHandler:
    """
    Har API response same format mein aayega:

    Success:
    {
        "success": true,
        "message": "Login successful!",
        "data": { ... }         ← optional
    }

    Error:
    {
        "success": false,
        "message": "Email is required",
        "errors": [ ... ]       ← optional (multiple errors)
    }
    """

    @staticmethod
    def success(message, data=None, status_code=StatusCode.OK):
        response = {
            'success': True,
            'message': message
        }
        if data is not None:
            response['data'] = data

        return jsonify(response), status_code


    @staticmethod
    def error(message, status_code=StatusCode.BAD_REQUEST, errors=None):
        response = {
            'success': False,
            'message': message
        }
        if errors is not None:
            response['errors'] = errors     # multiple validation errors

        return jsonify(response), status_code


    @staticmethod
    def validation_error(errors: list):
        """
        Multiple field errors ek saath return karo
        errors = ['Name is required', 'Email is invalid']
        """
        return jsonify({
            'success': False,
            'message': 'Validation failed',
            'errors' : errors
        }), StatusCode.BAD_REQUEST


    @staticmethod
    def not_found(message):
        return jsonify({
            'success': False,
            'message': message
        }), StatusCode.NOT_FOUND


    @staticmethod
    def unauthorized(message):
        return jsonify({
            'success': False,
            'message': message
        }), StatusCode.UNAUTHORIZED


    @staticmethod
    def server_error(message=None):
        return jsonify({
            'success': False,
            'message': message or AuthMessages.SERVER_ERROR
        }), StatusCode.SERVER_ERROR