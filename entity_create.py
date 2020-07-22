import dialogflow_v2 as dialogflow
# documentation: https://googleapis.dev/python/dialogflow/latest/gapic/v2/api.html
# https://googleapis.dev/python/dialogflow/latest/gapic/v2/types.html

AUTHENTICATION = "C:/Users/Sibat/df/entitypy-hclqpr-fda9848cedf9.json"
'''
Info on authentication: https://cloud.google.com/dialogflow/docs/quick/setup (go to "About Service Accounts" section and get a private key)
'''

def startup(project_id, filename):

    '''
     create "Attributes" entity type
     get "Attributes" entity ID
     parse list
     add all attributes to Attributes as entities
     create new entity types from entity list
     add values to new entity types
     good source: https://blog.dialogflow.com/post/create-and-manage-entities-with-api/
    '''

    # Create target_metrics entity type
    DISPLAY_NAME = "Attributes"
    create_entity_type(project_id, DISPLAY_NAME, "KIND_MAP")


    # GET ENTITY ID
    entity_id = get_entity_id(project_id, DISPLAY_NAME)

    # Parse List
    attributes, entities = list_parser(filename)

    # Add attributes to "target metrics (attributes)" entity type
    entity_types_client = dialogflow.EntityTypesClient.from_service_account_json(AUTHENTICATION)
    parent = entity_types_client.entity_type_path(project_id, entity_id)
    response = entity_types_client.batch_create_entities(parent, attributes)

    # Create new entity types, and add values to them
    for e in entities:
        create_entity_type(project_id, e[0], 'KIND_MAP')
        # get new entity type ID

        entity_id = get_entity_id(project_id, e[0])
        parent = entity_types_client.entity_type_path(project_id, entity_id)
        response = entity_types_client.batch_create_entities(parent, e[1])

    return 0

# Reads attribute and entity list, returns list of entities and list of attributes
def list_parser(file):
    ''' Reads attribute and entity list, returns list of entities and list of attributes '''
    f = open(file, "r")
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
                    attribute_string_list.append((x[0],x[2]))
                if 'Entities' in line:
                    break
        if 'Entities' in line:
            for line in f:
                if '------' in line:
                    continue
                x = line.split("|")
                temp = x[0]
                if ' ' in x[0]:
                    temp = x[0].replace(' ','')
                entity_string_list.append((temp,x[1]))

    attribute_list = []
    entity_list = []

    # in the following loop, we split the synonyms into a list of synonyms, and create entity objects as according to the API guidelines.
    for a in attribute_string_list:
        synonyms = a[1].split(',')
        synonyms.append(a[0])
        synonyms.extend(a[1].split())
        temp = {"value": a[0],
                'synonyms': synonyms}

        attribute_list.append(temp)
        '''
            # Creates a list of tuples,
            # the first value is the name of the entity TYPE to be created
            # the second value is a list of entities that belong to the given entity type
            # For now, synonyms are empty for these entities.
        '''

    for e in entity_string_list:
        display_name = e[0]
        values = e[1].split(',')
        values.append(e[1])
        values.extend(e[1].split())
        value_list = []
        for v in values:
            temp = {"value": v,
                    "synonyms": ''}
            value_list.append(temp)

        entity_list.append((display_name, value_list))

    return attribute_list, entity_list

def get_entity_id(project_id, display_name):
    entities_client = dialogflow.EntityTypesClient.from_service_account_json(AUTHENTICATION)
    agent_path = entities_client.project_agent_path(project_id)
    iterator = entities_client.list_entity_types(parent=agent_path)
    # iterator explanation^ https://googleapis.dev/python/google-api-core/latest/page_iterator.html
    entity_list = list(iterator)
    for e in entity_list:
        if (e.display_name == display_name):
            name = e.name.split('/')
            id = name[len(name)-1]
            return id
    return 0

def create_entity_type(project_id, display_name, kind):
    """Create an entity type with the given display name."""
    entity_types_client = dialogflow.EntityTypesClient.from_service_account_json(AUTHENTICATION)
    parent = entity_types_client.project_agent_path(project_id)
    entity_type = dialogflow.types.EntityType(
        display_name=display_name, kind=kind)
    response = entity_types_client.create_entity_type(parent, entity_type)
    print('Entity type created: \n{}'.format(response))


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient.from_service_account_json(AUTHENTICATION)

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)

    print('Intent created: {}'.format(response))

def list_intents(project_id):

    intents_client = dialogflow.IntentsClient.from_service_account_json(
        AUTHENTICATION)


    parent = intents_client.project_agent_path(project_id)

    intents = intents_client.list_intents(parent)

    for intent in intents:
        print('=' * 20)
        print('Intent name: {}'.format(intent.name))
        print('Intent display_name: {}'.format(intent.display_name))
        print('Action: {}\n'.format(intent.action))
        print('Root followup intent: {}'.format(
            intent.root_followup_intent_name))
        print('Parent followup intent: {}\n'.format(
            intent.parent_followup_intent_name))

        print('Input contexts:')
        for input_context_name in intent.input_context_names:
            print('\tName: {}'.format(input_context_name))

        print('Output contexts:')
        for output_context in intent.output_contexts:
            print('\tName: {}'.format(output_context.name))


# list_intents('api-agent-frktdb')
startup('entitypy-hclqpr', 'FlightDelay.attributes.mapping')
