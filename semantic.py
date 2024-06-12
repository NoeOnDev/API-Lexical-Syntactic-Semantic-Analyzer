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
    
    if condition[0] != 'condition' or condition[1] != declaration[2]:
        errors.append('La variable de la condición debe coincidir con la variable declarada')
    
    if iteration[0] != 'iteration' or iteration[1] != declaration[2]:
        errors.append('La variable de iteración debe coincidir con la variable declarada')
    
    if errors:
        return {'error': 'Se encontraron errores semánticos', 'details': errors}
    
    return {'success': 'Análisis semántico completado con éxito', 'result': result}