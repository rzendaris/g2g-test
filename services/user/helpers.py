from rest_framework.response import Response


def generate_response(data, success=True):
    http_code = 200
    if success:
        base_response = {
            "message": "Success",
            "data": data
        }
    else:
        base_response = {
            "message": "Error",
            "error": {
                "message": data,
            }
        }
        http_code = 400

    return Response(base_response, status=http_code)


def form_error_response(form):
    message = ['{0}'.format(form[item].errors[0]) for item in form.errors][0]
    field = ['{0}'.format(form[item].name) for item in form.errors][0]
    message = "{0} > {1}".format(field, message)

    return generate_response(data=message, success=False)
