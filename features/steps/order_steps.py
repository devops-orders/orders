from behave import *
from service import service
import requests
from compare import expect, ensure
import json


@given(u'the server is started')
def step_impl(context):
    context.app = service.app.test_client()
    context.server = service


@when(u'I visit the "home page"')
def step_impl(context):
    context.resp = context.app.get('/')


@then('I should see "{message}"')
def step_impl(context, message):
    message = bytes(message, 'ascii')
    assert message in context.resp.data


@then(u'I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.data)
    message = bytes(message, 'ascii')
    ensure(message in context.resp.data, False, error_msg)