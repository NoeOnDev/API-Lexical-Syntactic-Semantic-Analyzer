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
    
    declared_vars = {}
    errors = []

    def check_statements(statements):
        if isinstance(statements, tuple) and statements[0] == 'statements':
            statement = statements[1]
            if statement[0] == 'statement':
                if statement[1][0] == 'SYSOUT':
                    expression = statement[1][2]
                    check_expression(expression)
                elif statement[1][0] == 'declaration':
                    var_name = statement[1][1]
                    var_type = 'int'
                    declared_vars[var_name] = var_type
                    check_expression(statement[1][2])
                elif statement[1][0] == 'assignment':
                    var_name = statement[1][1]
                    if var_name not in declared_vars:
                        errors.append(f'Variable no declarada usada en asignación: {var_name}')
                    check_expression(statement[1][2])
                elif statement[1][0] == 'for_loop':
                    check_for_loop(statement[1])
            if len(statements) > 2:
                check_statements(statements[2])

    def check_for_loop(for_loop):
        declaration = for_loop[1]
        condition = for_loop[2]
        assignment = for_loop[3]
        block = for_loop[4]

        var_name = declaration[1]
        declared_vars[var_name] = 'int'

        check_expression(declaration[2])
        check_expression(condition)
        
        if assignment[0] == 'increment':
            if assignment[1] not in declared_vars:
                errors.append(f'Variable no declarada usada en incremento: {assignment[1]}')
        else:
            check_expression(assignment[2])
        
        check_statements(block[1])


    def check_expression(expression):
        if isinstance(expression, tuple) and expression[0] == 'binary_op':
            left = expression[2]
            right = expression[3]
            op = expression[1]
            left_type = get_expression_type(left)
            right_type = get_expression_type(right)
            if left_type != right_type:
                errors.append(f"No coinciden los tipos en la expresión: {left_type} {op} {right_type}")
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
                    return declared_vars.get(expression[1], 'unknown')
        elif isinstance(expression, str):
            if expression.isdigit():
                return 'int'
            else:
                return declared_vars.get(expression, 'unknown')
        return 'unknown'

    check_statements(statements)

    if errors:
        return {'error': 'Se encontraron errores semánticos', 'details': errors}
    
    return {'success': 'Análisis semántico completado con éxito', 'result': result}
