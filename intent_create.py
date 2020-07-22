import dialogflow_v2 as dialogflow
AUTHENTICATION = "C:/Users/Sibat/df/entitypy-hclqpr-fda9848cedf9.json"
def create_intent(project_id, display_name, training_phrases_parts_list,
                  message_texts):
    """Create an intent of the given intent type."""
    #entity_types_client = dialogflow.EntityTypesClient.from_service_account_json(AUTHENTICATION)
    intents_client = dialogflow.IntentsClient.from_service_account_json(AUTHENTICATION)

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []

    for training_phrases_parts in training_phrases_parts_list:
        parts = []
        for training_phrases_part in training_phrases_parts:
            part = dialogflow.types.Intent.TrainingPhrase.Part(
                text=training_phrases_part['text'],
                entity_type=training_phrases_part['entity_type'],
                alias=training_phrases_part['alias'],
                user_defined=training_phrases_part['user_defined'],
            )
            parts.append(part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=parts)
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    # intent = {
    #     "display_name": display_name,
    #     "webhook_state": True,
    #     "training_phrases": training_phrases_parts,
    #     "parameters": [{"display_name": "weather delay", "entity_type_display_name": "@Attributes", "value": "$Attributes"},
    #                    {"display_name": "origin airport", "entity_type_display_name": "@ORIGIN_AIRPORT", "value": "$ORIGIN_AIRPORT"}]
    # }

    response = intents_client.create_intent(parent, intent)

    print('Intent created: {}'.format(response))

def get_response_messages():
    attr_entity_tuple = get_entity_attr_list()
    attribute_list = attr_entity_tuple[0]
    entity_list = attr_entity_tuple[1]
    msg_list = []
    for entity in entity_list:
        for attribute in attribute_list:
            msg_list.append('you have entered $' + entity[0] + ' as your entity and $' + attribute[0] + ' as aggregation attribute')

    return msg_list

def get_training_phrases():
    prefix_file = open('prefix_text.txt', "r")
    root_file = open('root_text.txt', "r")
    suffix_file = open('suffix_text.txt', "r")
    attr_entity_tuple = get_entity_attr_list()
    attribute_list = attr_entity_tuple[0]
    entity_list = attr_entity_tuple[1]
    phrase_list = []
    for prefix in prefix_file:
        for root_word in root_file:
            for suffix in suffix_file:
                for attribute_pre in attribute_list:
                    for entity in entity_list:

                        prefix_dict = {}
                        prefix_dict['text'] = prefix
                        prefix_dict['entity_type'] = ''
                        prefix_dict['alias'] = ''
                        prefix_dict['user_defined'] = 0

                        attribute_pre_dict = {}
                        attribute_pre_dict['text'] = attribute_pre[0].lower().replace('_', ' ')
                        attribute_pre_dict['entity_type'] = '@Attributes'
                        attribute_pre_dict['alias'] = attribute_pre[0]
                        attribute_pre_dict['user_defined'] = 1

                        root_dict = {}
                        root_dict['text'] = root_word
                        root_dict['entity_type'] = ''
                        root_dict['alias'] = ''
                        root_dict['user_defined'] = 0

                        entity_dict = {}
                        entity_dict['text'] = entity[0].lower().replace('_', ' ')
                        entity_dict['entity_type'] = '@' + entity[0]
                        entity_dict['alias'] = entity[0]
                        entity_dict['user_defined'] = 1

                        suffix_dict = {}
                        suffix_dict['text'] = suffix
                        suffix_dict['entity_type'] = ''
                        suffix_dict['alias'] = ''
                        suffix_dict['user_defined'] = 0

                        phrase = []
                        phrase.append(prefix_dict)
                        phrase.append(attribute_pre_dict)
                        phrase.append(root_dict)
                        phrase.append(entity_dict)
                        phrase.append(suffix_dict)
                        phrase_list.append(phrase)

    # phrase_list = [{'text': 'weather delay ', 'entity_type': '@Attributes', 'alias': 'Attributes', 'user_defined': 1},
    #         {'text': 'for all ', 'entity_type': '', 'alias': '', 'user_defined': 0},
    #         {'text': 'origin airport.', 'entity_type': '@ORIGIN_AIRPORT', 'alias': 'origin_airport', 'user_defined': 1}]
    # for line in f:
    #     query = line.split('|')[0]
    #     phrase_list.append(query)
    return phrase_list

def get_entity_attr_list():
    f = open('FlightDelay.attributes.mapping', "r")
    attribute_string_list = []
    entity_string_list = []

    # creates 2 lists of tuples. Tuples are formatted as (attribute, string of synonyms)

    for line in f:
        if 'Attributes' in line:
            for line in f:
                if '------' in line:
                    continue
                if "|" in line:
                    x = line.split("|")
                    attribute_string_list.append((x[0], x[2]))
                if 'Entities' in line:
                    break
        if 'Entities' in line:
            for line in f:
                if '------' in line:
                    continue
                x = line.split("|")
                temp = x[0]
                if ' ' in x[0]:
                    temp = x[0].replace(' ', '')
                entity_string_list.append((temp, x[1]))
    return (attribute_string_list, entity_string_list)

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient.from_service_account_json(AUTHENTICATION)

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        # print(response.query_result.parameters.fields.split(','))
        # print('=' * 20)
        # print('Query text: {}'.format(response.query_result.query_text))
        # print('Detected intent: {} (confidence: {})\n'.format(
        #     response.query_result.intent.display_name,
        #     response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

        return response.query_result.parameters.fields


#create_intent('entitypy-hclqpr', 'entity_extraction', get_training_phrases(), get_response_messages())
# detect_intent_texts('entitypy-hclqpr', '123456789', ['Predict average elapsed time for each origin airports with delay caused by weather is more than five minutes for next week'], 'en-US')