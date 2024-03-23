import ast
import sys
import types


def run_code(code, input_dict):
    # Create a new module to execute the code safely
    module_name = "__temp_module__"
    module = types.ModuleType(module_name)
    sys.modules[module_name] = module

    # Add the input_dict variable to the temporary module
    module.input_dict = input_dict

    # Analyze the code to make sure it doesn't contain any dangerous statements
    ast_node = ast.parse(code)
    for node in ast.walk(ast_node):
        if isinstance(
            node, ast.Global | ast.Import | ast.ImportFrom | ast.Nonlocal
        ):
            raise ValueError(
                "The code must not contain any import, global or nonlocal statements."
            )

    # Execute the code in the new module and store the result in a variable
    output_dict = None
    try:
        exec(code, module.__dict__)
        if hasattr(module, "output_dict"):
            output_dict = module.output_dict
        else:
            raise ValueError("The code must define an output_dict variable.")
    except Exception as e:
        raise RuntimeError(f"Error while executing the code: {e}")

    # Delete the temporary module
    del sys.modules[module_name]

    return output_dict
