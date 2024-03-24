from jsonschema import Draft7Validator


def infer_json_schema(data: dict) -> Draft7Validator:
    validator = Draft7Validator.check_schema({})
    schema = validator.infer_schema(data)
    return schema


def validate_json(data: dict, json_schema: Draft7Validator):
    validator = Draft7Validator(json_schema)
    errors = list(validator.iter_errors(data))
    return errors
