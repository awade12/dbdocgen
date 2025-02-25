from click import command, option, pass_context

@command()
@option('--help', is_flag=True, help='Show this message and exit.')
@pass_context
def help(ctx, help):
    if help:
        ctx.ensure_object(dict)
        ctx.obj['help'] = True
        return
    ctx.ensure_object(dict)
    ctx.obj['help'] = False
