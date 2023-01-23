from ..parsers.javafileparser import JavaFile

if __name__ == "__main__":
    file = JavaFile("commint/tests/Box.java")

    print(file.getClassName())

