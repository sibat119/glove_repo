import intent_create

def main():
    attr_entity_tuple = intent_create.get_entity_attr_list()
    attribute_list = attr_entity_tuple[0]
    entity_list = attr_entity_tuple[1]
    detected_entity = 'AIRLINE'
    detected_attribute = 'WEATHER_DELAY'
    while(1):
        data = input()
        fields = intent_create.detect_intent_texts('entitypy-hclqpr', '123456789', [data] , 'en-US')
        for entity in entity_list:
            if (len(fields[entity[0]].list_value.values) > 0) :
                detected_entity = entity[0]
        print('Detected Entity: {}. Is it correct? type yes for correct and no for incorrect'.format(detected_entity))
        data = input()
        if(data == 'yes'):
            for attr in attribute_list:
                if (len(fields[attr[0]].list_value.values) > 0):
                    detected_attribute = attr[0]
            print('Detected Aggregation Attribute: {}. Is it correct? type yes for correct and no for incorrect'.format(detected_attribute))
            data = input()
            if (data == 'yes'):
                break



main()