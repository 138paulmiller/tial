import context


def interpret(parser, context, code):
    root =  parser.parse(code)
    parser.print_tree(root)
    context.eval(root, context)
    print 'CONTEXT:'
    context.print_vars()


def interpret_source_file(parser, context, file_path):
    source = open(file_path)
    code = source.read()
    interpret(parser, context, code)