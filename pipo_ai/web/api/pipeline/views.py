from fastapi import APIRouter

from pipo_ai.web.api.pipeline.schema import Message

router = APIRouter()


@router.post("/{slug}", response_model=Message)
async def send_echo_message(
    slug: str,
    incoming_message: Message,
) -> Message:
    """
    Sends echo back to user.

    :param incoming_message: incoming message.
    :returns: message same as the incoming.
    """
    return incoming_message
