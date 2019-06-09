# Create your views here.
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AppSerializer
from src.two_relay.give_answer import answer_question
from .models import Action, App

from src.deprecated_demos.listen import listen_async, end_listening_for_generic
from src.main import listen_for_keyword_async, end_listening_for_keyword
from src.one_start.actions.text import actions

generic_thread = None
keyword_thread = None
keyword_terminate = False


def stop_generic():
    print("1")
    global generic_thread
    if generic_thread and generic_thread.is_alive():
        generic_thread.join()


def stop_keyword():
    print("2")
    global keyword_thread, keyword_terminate
    if keyword_thread and keyword_thread.is_alive():
        keyword_terminate = True
        keyword_thread.join()
        keyword_terminate = False


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
                response = None
                try:
                    response = answer_question(message)
                except Exception as e:
                    print(e)
                    return Response(data={
                        'message': "I did not understand that. Please retry"},
                                    status=status.HTTP_404_NOT_FOUND)
                print(response)
                if response:
                    next_step_number = 1
                    return Response(data={'activeActionId': 0,
                                          'message': response,
                                          'nextStepNumber': next_step_number})
                else:
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
        stop_generic()
        stop_keyword()
        keyword_thread = listen_for_keyword_async()
        return Response(
            data={'message': "Listening for keyword..."},
            status=status.HTTP_200_OK)


class ListenForGenericView(APIView):
    def post(self, request):
        global generic_thread, keyword_thread
        # end_listening_for_generic()
        stop_keyword()
        stop_generic()
        generic_thread = listen_async()
        return Response(
            data={'message': "Listening for generic..."},
            status=status.HTTP_200_OK)


# do not call in self
def set_keyword_thread(new_keyword_thread):
    global keyword_thread
    keyword_thread = new_keyword_thread


def set_generic_thread(new_generic_thread):
    global generic_thread
    stop_generic()
    generic_thread = new_generic_thread


def get_keyword_terminate():
    return keyword_terminate


class AppsView(ListCreateAPIView):
    serializer_class = AppSerializer
    queryset = App.objects.all()
