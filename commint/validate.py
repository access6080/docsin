import sys
from parsers.javafileparser import JavaFile
from model.validate import validate

if __name__ == "__main__":
    # Get and loop comments and methods from file
    file = JavaFile("commint/tests/Box.java")

    response = {}

    for method in file.getMethods():
        method_name = method.getName()
        comment = method.getComments()
        code = method.getCode()

        response[method_name] = validate(comment, code)

    for res in response:
        print(res,"---",response.get(res))
        print()