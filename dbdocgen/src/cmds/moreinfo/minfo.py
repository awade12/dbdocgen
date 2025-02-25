from click import command, option, pass_context

@command()
@option('--info', is_flag=True, help='Show this message and exit.')
@pass_context
def info(ctx, info):
    if info:
        ctx.ensure_object(dict)
        ctx.obj['info'] = True
        return
    ctx.ensure_object(dict)
    ctx.obj['info'] = False
