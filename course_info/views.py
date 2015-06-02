import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.core.urlresolvers import reverse
from django.conf import settings
from dce_lti_py.tool_config import ToolConfig

from icommons import ICommonsApi

log = logging.getLogger(__name__)

@require_GET
def tool_config(request):

    app_config = settings.LTI_APPS['course_info']

    launch_url = request.build_absolute_uri(reverse('lti_launch'))

    editor_settings = {
        'enabled': 'true',
        'text': app_config['menu_title'],
        'width': app_config['selection_width'],
        'height': app_config['selection_height'],
        'icon_url': request.build_absolute_uri(app_config['icon_url']),
        'url': launch_url
    }

    extensions = {
        app_config['extensions_provider']: {
            'editor_button': editor_settings,
            'tool_id': app_config['id'],
            'privacy_level': app_config['privacy_level']
        }
    }

    lti_tool_config = ToolConfig(
        title=app_config['name'],
        launch_url=launch_url,
        secure_launch_url=launch_url,
        extensions=extensions,
        description = app_config['description']
    )

    return HttpResponse(lti_tool_config.to_xml(), content_type='text/xml')

@login_required
@require_POST
@csrf_exempt
def lti_launch(request):
    return editor(request)


def __course_context(request,course_instance_id,keys):
    course_info = ICommonsApi.from_request(request).get_course_info(course_instance_id)
    context = { 'fields':[], 'course_instance_id': course_instance_id}
    for key in keys :
        if '.' in key:
            keyparts = key.split('.')
            field  = { 'key': key, 'value': course_info[keyparts[0]][keyparts[1]]}
        else :
            field  = { 'key': key, 'value': course_info[key]}
        context['fields'].append(field)
    return context

@require_GET
def widget(request):
    course_instance_id = request.GET.get('course_instance_id')
    return render(request, 'course_info/widget.html',
                  __course_context(request,course_instance_id,
                    request.GET.getlist('key')))


def editor(request):
    # hard code while developing locally
    course_instance_id = "312976"
    keys = ['title','description']
    course_context = __course_context(request,course_instance_id,keys)
    print(request.GET)
    print(request.POST)
    print("Why isn't it here?")
    print(request.POST.get('launch_presentation_return_url'))
    course_context['launch_presentation_return_url'] = request.POST.get('launch_presentation_return_url')
    return render(request, 'course_info/editor.html',course_context)

