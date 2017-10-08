"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function

from mappings import name_to_ticker
from nasdaq import *


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "StockPriceIntent":
        return get_stock_price_in_session(intent, session)
    elif intent_name == "StockHighIntent":
        return get_stock_high_in_session(intent, session)
    elif intent_name == "StockLowIntent":
        return get_stock_low_in_session(intent, session)
    elif intent_name == "PortfolioUpdateIntent":
        return get_portfolio_update(intent, session)
    elif intent_name == "StockRecommendationIntent":
        return get_stock_recommendation_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_end_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Nasdaq Stock Skill. " \
                    "Please ask for a stock price by saying, " \
                    "what is the stock price of Nasdaq"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask for a stock price by saying, " \
                    "what is the stock price of Nasdaq"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_end_response():
    card_title = 'Goodbye'
    session_attributes = {}
    reprompt_text = None

    speech_output = "Thank you for using the Nasdaq API!"
    should_end_session = True

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_stock_price_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    reprompt_text = None
    should_end_session = False

    if 'Company' in intent['slots']:
        company = intent['slots']['Company']['value']
        if company.upper() in name_to_ticker:
            stock_price = get_close_price(name_to_ticker[company.upper()])
            speech_output = "The stock price of " + company + " is " + str(stock_price) + " dollars."
        else:
            speech_output = "I'm not sure what that company is. Please try again."
    else:
        speech_output = "I'm not sure what that company is. Please try again."

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_stock_high_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    reprompt_text = None
    should_end_session = False

    if 'Company' in intent['slots']:
        company = intent['slots']['Company']['value']
        if company.upper() in name_to_ticker:
            high_price = get_high_price(name_to_ticker[company.upper()])
            speech_output = "The high price of " + company + " is " + str(high_price) + " dollars."
        else:
            speech_output = "I'm not sure what that company is. Please try again."
    else:
        speech_output = "I'm not sure what that company is. Please try again."

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_stock_low_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    reprompt_text = None
    should_end_session = False

    if 'Company' in intent['slots']:
        company = intent['slots']['Company']['value']
        if company.upper() in name_to_ticker:
            low_price = get_low_price(name_to_ticker[company.upper()])
            speech_output = "The low price of " + company + " is " + str(low_price) + " dollars."
        else:
            speech_output = "I'm not sure what that company is. Please try again."
    else:
        speech_output = "I'm not sure what that company is. Please try again."

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_portfolio_update(intent, session):
    card_title = intent['name']
    session_attributes = {}
    reprompt_text = None
    should_end_session = False

    # Demo purposes using mock portfolio
    speech_output = 'Here is your portfolio. Nasdaq increased by 0.66 percentage points and closed at 71.49 dollars. ' \
                    'Microsoft increased by 0.73 percentage points and closed at 73.35 dollars. ' \
                    'Amazon increased by 0.5 percentage points and closed at 1010.04 dollars.'

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def get_stock_recommendation_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    reprompt_text = None
    should_end_session = False

    # Demo purposes using mock portfolio
    speech_output = 'Based on your portfolio and current market performance, we recommend' \
                    'investing in Tesla, Nvidia, and CA Technologies.'

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }