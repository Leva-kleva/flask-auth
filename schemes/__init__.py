from jsonschema import validate
import schemes.signup
import schemes.login


def check(request, schema):
    try:
        validate(instance=request.json, schema=schema)
        return True
    except:
        return False
