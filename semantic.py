def analyze_semantics(parsed_code):
    if 'error' in parsed_code:
        return parsed_code
    
    result = parsed_code.get('result', None)
    if result is None:
        return {'error': 'No se proporcionó código analizado'}
    
    try:
        main_method = result[2]
        block = main_method[1]
        statements = block[1]
    except IndexError:
        return {'error': 'La estructura del código analizado no es la esperada'}
    
    declared_vars = set()
    errors = []

    def check_statements(statements):
        if isinstance(statements, tuple) and statements[0] == 'statements':
            statement = statements[1]
            if statement[0] == 'statement' and statement[1] == 'SYSOUT':
                expression = statement[2]
                check_expression(expression)
            if len(statements) > 2:
                check_statements(statements[2])

    def check_expression(expression):
        if isinstance(expression, tuple) and expression[0] == 'binary_op':
            left = expression[2]
            right = expression[3]
            op = expression[1]
            left_type = get_expression_type(left)
            right_type = get_expression_type(right)
            if left_type != right_type:
                errors.append(f"Type mismatch in expression: {left_type} {op} {right_type}")
        else:
            get_expression_type(expression)

    def get_expression_type(expression):
        if isinstance(expression, tuple):
            if expression[0] == 'term':
                if expression[1].startswith('"'):
                    return 'string'
                elif expression[1].isdigit():
                    return 'int'
                else:
                    return 'variable'
        elif isinstance(expression, str):
            if expression.isdigit():
                return 'int'
            else:
                return 'variable'
        return 'unknown'

    check_statements(statements)

    if errors:
        return {'error': 'Se encontraron errores semánticos', 'details': errors}
    
    return {'success': 'Análisis semántico completado con éxito', 'result': result}
