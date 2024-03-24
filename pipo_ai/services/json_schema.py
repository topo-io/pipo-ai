from genson import SchemaBuilder
from jsonschema import Draft7Validator


def infer_json_schema(data: dict) -> dict:
    builder = SchemaBuilder()
    builder.add_object(data)
    return builder.to_schema()


def validate_json(data: dict, json_schema: Draft7Validator):
    validator = Draft7Validator(json_schema)
    errors = list(validator.iter_errors(data))
    return errors
