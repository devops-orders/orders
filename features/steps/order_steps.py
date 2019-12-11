from behave import *
from service import service
import requests
from compare import expect, ensure
import json
from os import getenv
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))

@given(u'the server is started')
def step_impl(context):
    context.app = service.app.test_client()
    context.server = service

@given(u'the following orders')
def step_impl(context):
    """ Delete all Orders and load new ones """
    headers = {'Content-Type': 'application/json'}
    print(context.base_url)
    context.resp = requests.delete(context.base_url + '/orders/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/orders'
    for row in context.table:
        data = {
            "uuid": row['uuid'],
            "price": row['price'],
            "quantity": row['quantity'],
            "customer_id": row['customer_id'],
            "product_id": row['product_id'],
            "status": row['Status']
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)


@when(u'I visit the "home page"')
def step_impl(context):
    context.driver.get(context.base_url)


@then('I should see "{message}"')
def step_impl(context, message):
    expect(context.driver.title).to_contain(message)


@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@when(u'I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'order_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)


@when(u'I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()


@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = 'order_' + element_name.lower()
    print(element_id)
    element = context.driver.find_element_by_id(element_id)
    print("*****")
    print(element.get_attribute('value'))
    print("*****")
    expect(element.get_attribute('value')).to_equal(text_string)
    #found = WebDriverWait(context.driver, WAIT_SECONDS).until(
    #    expected_conditions.text_to_be_present_in_element_value(
    #        (By.ID, element_id),
    #        text_string
    #    )
    #)
    #expect(found).to_be(True)


@when(u'I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'order_' + element_name.lower()
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)

@then(u'I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)


@when(u'I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = 'order_' + element_name.lower()
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)


@when(u'I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = 'order_' + element_name.lower()
    # element = context.driver.find_element_by_id(element_id)
    element = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

@then(u'I should see "{text}" in the results')
def step_impl(context, text):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            text
        )
    )
    expect(found).to_be(True)


@then(u'I should not see "{text}" in the results')
def step_impl(context, text):
    element = context.driver.find_element_by_id('search_results')
    error_msg = "I should not see '%s' in '%s'" % (text, element.text)
    ensure(text in element.text, False, error_msg)


@when(u'I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = 'order_' + element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    element.select_by_visible_text(text)


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = 'order_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    expect(element.get_attribute('value')).to_be(u'')


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = 'order_' + element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    expect(element.first_selected_option.text).to_equal(text)
