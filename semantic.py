def analyze_semantics(parsed_code):
    if 'error' in parsed_code:
        return parsed_code
    
    result = parsed_code.get('result', None)
    if result is None:
        return {'error': 'No se proporcionó código analizado'}
    
    declarations = result[1]
    statements = result[2]
    
    declared_vars = set()
    errors = []

    if declarations[0] == 'declarations':
        current = declarations
        while current:
            if current[0] == 'declarations':
                declaration = current[1]
                if declaration[0] == 'declaration':
                    var_name = declaration[1]
                    declared_vars.add(var_name)
                if len(current) > 2:
                    current = current[2]
                else:
                    current = None
            else:
                break

    def check_statements(statements):
        current = statements
        while current:
            if current[0] == 'statements':
                statement = current[1]
                if statement[0] == 'statement' and statement[1] == 'if':
                    condition = statement[2]
                    if condition[0] == 'condition':
                        var_name = condition[1]
                        if var_name not in declared_vars:
                            errors.append(f'Variable no declarada usada en condición: {var_name}')
                    block = statement[3]
                    if block[0] == 'block':
                        check_statements(block[1])
                elif statement[0] == 'assignment':
                    var_name = statement[1]
                    if var_name not in declared_vars and var_name != 'ver':
                        errors.append(f'Variable no declarada usada en asignación: {var_name}')
                if len(current) > 2:
                    current = current[2]
                else:
                    current = None
            else:
                break

    check_statements(statements)

    if errors:
        return {'error': 'Se encontraron errores semánticos', 'details': errors}
    
    return {'success': 'Análisis semántico completado con éxito', 'result': result}