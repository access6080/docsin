import javalang

class JavaFile:
    class JavaMethod:
        def __init__(self, name, comments: str, code: str, start: int, end: int) -> None:
            self.name = name
            self.comments = comments
            self.code = code
            self.start = start
            self.end = end
        
        def getName(self):
            return self.name
        
        def getComments(self):
            return self.comments
        
        def getCode(self):
            return self.code

    def __init__(self, path: str) -> None:
        self.path = path
        self.tree = None
        self.class_name = ""
        self.codelines = ""
        self.methods = []

        self.parse_file()

    def parse_file(self):
        with open(self.path, 'r') as r:
            self.codelines = r.readlines()
            code_text = ''.join(self.codelines)

        lex = None
        self.tree = javalang.parse.parse(code_text)
        methods = {}
        for _, class_node in self.tree.filter(javalang.tree.TypeDeclaration):
            self.class_name = class_node.name

        for _, method_node in self.tree.filter(javalang.tree.MethodDeclaration):
            startpos, endpos, startline, endline = self._get_method_start_end(
                method_node)
            method_text, startline, endline, lex = self._get_method_text(
                startpos, endpos, startline, endline, lex)
            methods[method_node.name] = method_text

            self.methods.append(self.JavaMethod(method_node.name,
                method_node.documentation, method_text, startline, endline))
            

    def _get_method_start_end(self, method_node):
        startpos = None
        endpos = None
        startline = None
        endline = None
        for path, node in self.tree:
            if startpos is not None and method_node not in path:
                endpos = node.position
                endline = node.position.line if node.position is not None else None
                break
            if startpos is None and node == method_node:
                startpos = node.position
                startline = node.position.line if node.position is not None else None
        return startpos, endpos, startline, endline
    
    def _get_method_text(self, startpos, endpos, startline, endline, last_endline_index):
        if startpos is None:
            return "", None, None, None
        else:
            startline_index = startline - 1
            endline_index = endline - 1 if endpos is not None else None

            # 1. check for and fetch annotations
            if last_endline_index is not None:
                for line in self.codelines[(last_endline_index + 1):(startline_index)]:
                    if "@" in line:
                        startline_index = startline_index - 1
            meth_text = "<ST>".join(self.codelines[startline_index:endline_index])
            meth_text = meth_text[:meth_text.rfind("}") + 1]

            # 2. remove trailing rbrace for last methods & any external content/comments
            # if endpos is None and
            if not abs(meth_text.count("}") - meth_text.count("{")) == 0:
                # imbalanced braces
                brace_diff = abs(meth_text.count("}") - meth_text.count("{"))

                for _ in range(brace_diff):
                    meth_text = meth_text[:meth_text.rfind("}")]
                    meth_text = meth_text[:meth_text.rfind("}") + 1]

            meth_lines = meth_text.split("<ST>")
            meth_text = "".join(meth_lines)
            last_endline_index = startline_index + (len(meth_lines) - 1)

            return meth_text, (startline_index + 1), (last_endline_index + 1), last_endline_index
        

    def getMethods(self):
        return self.methods
    
    def getClassName(self):
        return self.class_name
