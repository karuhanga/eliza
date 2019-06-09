# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Action

from src.deprecated_demos.listen import listen_async, end_listening_for_generic
from src.main import listen_for_keyword_async, end_listening_for_keyword
from src.one_start.actions.text import actions

generic_thread = None
keyword_thread = None


class ActionView(APIView):
    def post(self, request, step_number):
        data = request.data
        try:
            message = data['message']['body'].lower()
        except KeyError:
            return Response(
                data={'message': "A message is required"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if step_number is 1:
            try:
                resolved_action = actions[message]
            except KeyError:
                # todo do some fancy speech analysis here
                return Response(data={
                    'message': "I did not understand that. Please retry"},
                                status=status.HTTP_404_NOT_FOUND)

            action = Action(name=message, completed_step_number=step_number)
            action.save()

            if step_number < resolved_action['steps']:
                next_step_number = step_number + 1
                return Response(data={'activeActionId': action.pk,
                                      'message':
                                          resolved_action['last_n_prompts'][
                                              step_number - 1],
                                      'nextStepNumber': next_step_number})
            else:
                response = resolved_action['action']()
                next_step_number = 1
                return Response(data={'activeActionId': action.pk,
                                      'message': response if response else
                                      resolved_action['last_n_prompts'][step_number - 1],
                                      'nextStepNumber': next_step_number})
        else:
            try:
                active_action_id = data['activeActionId']
            except KeyError:
                return Response(
                    data={
                        'message': "An activeActionId is required"},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            try:
                resolved_action = actions[
                    Action.objects.get(pk=active_action_id).name]
            except AttributeError:
                return Response(data={
                    'message': "I did not understand that. Please retry"},
                    status=status.HTTP_404_NOT_FOUND)

            if step_number < resolved_action['steps']:
                next_step_number = step_number + 1
                return Response(data={'activeActionId': active_action_id,
                                      'message':
                                          resolved_action['last_n_prompts'][
                                              step_number - 1],
                                      'nextStepNumber': next_step_number})
            else:
                response = resolved_action['action'](message)
                next_step_number = 1
                return Response(data={'activeActionId': active_action_id,
                                      'message': response if response else
                                          resolved_action['last_n_prompts'][step_number - 1] + message + '...',
                                      'nextStepNumber': next_step_number})


class ListenForKeywordView(APIView):
    def post(self, request):
        global generic_thread, keyword_thread
        # end_listening_for_keyword()
        if generic_thread: generic_thread._stop()
        if keyword_thread: keyword_thread._stop()
        keyword_thread = listen_for_keyword_async()
        return Response(
            data={'message': "Listening for keyword..."},
            status=status.HTTP_200_OK)


class ListenForGenericView(APIView):
    def post(self, request):
        global generic_thread, keyword_thread
        # end_listening_for_generic()
        if generic_thread: generic_thread._stop()
        if keyword_thread: keyword_thread._stop()
        generic_thread = listen_async()
        return Response(
            data={'message': "Listening for generic..."},
            status=status.HTTP_200_OK)
