import re

def tokenize(expression):
  """
  Splits the expression string into tokens (numbers, operators, parentheses).
  """
  token_pattern = r"(\d+|[()+\-*/])"
  return re.findall(token_pattern, expression)

def parse_factor(tokens, path):
  """
  Parses a factor (number or parenthesized expression), updating the path.
  """
  token = tokens.pop(0)
  path.append("Factor")
  if token.isdigit():
    path.append(int(token))
    print(f"Factor: {token} = {int(token)}")  # Print intermediate value
    return int(token)
  elif token == "(":
    path.append("(")
    result = parse_expression(tokens, path.copy())  # Copy path to avoid modification
    path.append(")")
    if tokens.pop(0) != ")":
      raise SyntaxError("Missing closing parenthesis")
    print(f"Factor (sub-expression): {path}")  # Print intermediate path
    return result
  else:
    raise SyntaxError("Unexpected token: " + token)

def parse_term(tokens, path):
  """
  Parses a term (factors multiplied or divided), updating the path.
  """
  result = parse_factor(tokens, path.copy())
  path.append("Term")
  while True:
    token = tokens.pop(0) if tokens else None
    if not token in ("*", "/"):
      tokens.insert(0, token)  # Push back the token if not used
      break
    path.append(token)
    print(f"Term: {result} {token}")  # Print intermediate calculation
    result = result * parse_factor(tokens, path.copy()) if token == "*" else result / parse_factor(tokens, path.copy())
  print(f"Final Term: {result}")  # Print final term value
  return result

def parse_expression(tokens, path):
  """
  Parses the entire expression (terms added or subtracted), updating the path.
  """
  result = parse_term(tokens, path.copy())
  path.append("Expression")
  while True:
    token = tokens.pop(0) if tokens else None
    if not token in ("+", "-"):
      tokens.insert(0, token)  # Push back the token if not used
      break
    path.append(token)
    print(f"Expression: {result} {token}")  # Print intermediate calculation
    result = result + parse_term(tokens, path.copy()) if token == "+" else result - parse_term(tokens, path.copy())
  print(f"Final Expression: {result}")  # Print final expression value
  return result

def evaluate(expression):
  """
  Evaluates the parsed expression and prints the path.
  """
  tokens = tokenize(expression)
  path = []
  result = parse_expression(tokens, path)
  print(f"Result: {result}")
  print(f"Recursive Path: {path}")
  return result

# Example usage
expression = "(2 + 3) * 4 + 1"
result = evaluate(expression)
