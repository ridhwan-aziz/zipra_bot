import sys, io, traceback, logging
from telethon.tl.custom.message import Message
from utils.helper import get_length
from utils.init import owner

async def main(*args):
    logging.debug("[EvalHandler] Setting up variables")
    event: Message = args[0]
    parser = args[1]

    code = await parser.get_args()


    if (await event.get_sender()).id != owner:
        logging.info("[EvalHandler] The sender is my owner. Aborting")
        return None
    elif code == None:
        logging.debug("[EvalHandler] Code not found. Aborting")
        return await event.respond("No code...")

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    re_out = sys.stdout = io.StringIO()
    re_err = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    logging.debug("[EvalHandler] Executing code")
    try:
        await aexec(code, event, event.client)
    except:
        exc = traceback.format_exc()

    logging.debug("[EvalHandler] Parsing output")
    stdout = re_out.getvalue()
    stderr = re_err.getvalue()
    sys.stderr = old_stderr
    sys.stdout = old_stdout

    result = None
    if exc:
        result = exc
    elif stderr:
        result = stderr
    elif stdout:
        result = stdout
    
    if result != None:
        if get_length(result) > 4096:
            logging.debug(f"[EvalHandler] Message length is {get_length(result)}. Sending as file instead.")
            with io.BytesIO(str.encode(result)) as out:
                out.name = "eval.txt"
                return await event.respond(file=out)
        else:
            logging.debug("[EvalHandler] Message length is less than 4096. Sending as message")
            return await event.respond(result, parse_mode=None)

async def aexec(code: str, event, client):
    exec(
        "async def __aexec(event, client): "
        + "".join(f"\n {c}" for c in code.split("\n"))
    )
    return await locals()['__aexec'](event, client)