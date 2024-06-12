def analyze_semantics(parsed_code):
    if 'error' in parsed_code:
        return parsed_code
    
    result = parsed_code.get('result', None)
    if result is None:
        return {'error': 'No se proporcionó código analizado'}
    
    loop_type, declaration, condition, iteration, block = result
    
    if loop_type != 'for_loop':
        return {'error': 'No es un bucle for'}

    errors = []
    
    if declaration[0] != 'declaration' or declaration[1] != 'int':
        errors.append('La declaración de la variable debe ser de tipo int')
    declared_var = declaration[2]
    
    if condition[0] != 'condition' or condition[1] != declared_var:
        errors.append('La variable de la condición debe coincidir con la variable declarada')
    if condition[2] not in ('<=', '<', '>=', '>'):
        errors.append('El operador en la condición debe ser una comparación')
    
    if iteration[0] != 'iteration' or iteration[1] != declared_var:
        errors.append('La variable de iteración debe coincidir con la variable declarada')
    if iteration[2] not in ('++', '--', '+=', '-='):
        errors.append('La operación de iteración no es válida')
    
    block_statements = block[1]
    if isinstance(block_statements, list):
        for statement in block_statements:
            if statement[0] == 'statement' and statement[1] == 'System.out.println':
                if declared_var in statement[2]:
                    errors.append('La variable de iteración se usa dentro de una declaración de impresión')
    
    if errors:
        return {'error': 'Se encontraron errores semánticos', 'details': errors}
    
    return {'success': 'Análisis semántico completado con éxito', 'result': result}
