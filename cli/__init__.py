import context # Context can be though of as the current session


def interpret(parser, context, code):
    root =  parser.parse(code)
    parser.print_tree(root)
    context.eval(root, context)
    


def interpret_source_file(parser, context, file_path):
    source = open(file_path)
    code = source.read()
    print code[:-1]
    interpret(parser, context, code)