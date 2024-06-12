def analyze_semantics(parsed_code):
    if 'error' in parsed_code:
        return parsed_code
    
    result = parsed_code.get('result', None)
    if result is None:
        return {'error': 'No parsed code provided'}
    
    loop_type, declaration, condition, iteration, block = result
    
    if loop_type != 'for_loop':
        return {'error': 'Not a for loop'}

    errors = []
    
    if declaration[0] != 'declaration' or declaration[1] != 'int':
        errors.append('Variable declaration must be of type int')
    
    if condition[0] != 'condition' or condition[1] != declaration[2]:
        errors.append('Condition variable must match the declared variable')
    
    if iteration[0] != 'iteration' or iteration[1] != declaration[2]:
        errors.append('Iteration variable must match the declared variable')
    
    if errors:
        return {'error': 'Semantic errors found', 'details': errors}
    
    return {'success': 'Semantic analysis completed successfully', 'result': result}
