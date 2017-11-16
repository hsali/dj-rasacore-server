from rest_framework.decorators import api_view
from rest_framework.response import Response

# from .chat import Chat

@api_view(http_method_names=['post', ])
def chatView(request):
    pass
    # CHAT_AGENT = Chat()

    # message = request.data.get('message')
    # user_id = request.data.get('user_id', 'default')
    # state = request.data.get('state', 'start')
    # executed_action = request.data.get('executed_action')
    # events = request.data.get('events', [])

    # if message and state == 'start':
    #     res = CHAT_AGENT.agent.start_message_handling(message, user_id=user_id)
    #     return Response(res)
    # if message and state == 'parse':
    #     res = CHAT_AGENT.agent.handle_message(message, user_id)
    #     return Response(res)
    # if message and state == 'continue':
    #     res = CHAT_AGENT.agent.continue_message_handling(user_id, executed_action, events)
    #     return Response(res)
    # else:
    #     return Response({'status': 'error', 'detail': 'message is required'}, 400)
