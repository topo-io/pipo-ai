import ast
import sys
import types


def run_code(code, input_dict):
    # Check code safety
    check_code(code)

    # Create a new module to execute the code safely
    module_name = "__temp_module__"
    module = types.ModuleType(module_name)
    sys.modules[module_name] = module

    # Add the input_dict variable to the temporary module
    module.input_dict = input_dict

    # Execute the code in the new module and store the result in a variable
    output_dict = None
    try:
        exec(code, module.__dict__)  # noqa: S102
        if hasattr(module, "output_dict"):
            output_dict = module.output_dict
        else:
            raise ValueError("The code must define an output_dict variable.")
    except Exception as e:
        raise RuntimeError(f"Error while executing the code: {e}")

    # Delete the temporary module
    del sys.modules[module_name]

    return output_dict


def check_code(code):
    # Analyze the code to make sure it doesn't contain any dangerous statements
    ast_node = ast.parse(code)
    for node in ast.walk(ast_node):
        if isinstance(
            node, ast.Global | ast.Import | ast.ImportFrom | ast.Nonlocal
        ):
            raise ValueError(
                "The code must not contain any import, global or nonlocal statements."
            )


def sanitize_code(code: str) -> str:
    # Parse the code into an AST
    tree = ast.parse(code)

    # Remove all import statements from the code
    for node in ast.walk(tree):
        if isinstance(node, ast.Import | ast.ImportFrom):
            # Find the parent node of the import statement
            parent_node = node
            while isinstance(parent_node, ast.AST):
                parent_node = getattr(parent_node, "parent", None)
                if parent_node is None:
                    break
            if parent_node is not None:
                parent_node.body.remove(node)

    # Remove all return statements and their values from the code
    for node in ast.walk(tree):
        if isinstance(node, ast.Return):
            # Find the parent node of the return statement
            parent_node = node
            while isinstance(parent_node, ast.AST):
                parent_node = getattr(parent_node, "parent", None)
                if parent_node is None:
                    break
            if parent_node is not None:
                parent_node.body.remove(node)

    # Generate the sanitized code from the modified AST
    sanitized_code = ast.unparse(tree)

    return sanitized_code
