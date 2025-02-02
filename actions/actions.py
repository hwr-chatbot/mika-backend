from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionSetTopic(Action):
    def name(self):
        return "action_set_topic"

    def run(self, dispatcher, tracker, domain):
        intent_to_topic = {
            "a_level": "a-level",
            "guest_auditor": "guest auditor",
            "cv": "cv",
            "admission": "admission",
            "application": "application",
            "aps": "aps",
            "eligibility": "eligibility",
            "gmat": "gmat",
            "semester": "semester",
        }
        
        current_intent = tracker.latest_message['intent'].get('name')
        topic = intent_to_topic.get(current_intent, None)
        
        if topic:
            dispatcher.utter_message(text=f"I will remember that your topic is {topic}.")
            return [SlotSet("topic", topic)]
        return []

class HandleMultipleIntents(Action):
    def name(self):
        return "action_handle_multiple_intents"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Liste der besten Intents aus der Nachricht
        intents = tracker.latest_message["intent_ranking"]
        
        # Maximale Anzahl an Intents, die verarbeitet werden sollen
        max_intents = 3

        # Antworten aus der `domain.yml` generieren
        responses = []
        for intent in intents[:max_intents]:
            response_key = f"utter_{intent['name']}"  # Antwort-Schlüssel aus domain.yml
            if response_key in domain["responses"]:
                responses.append(domain["responses"][response_key][0]["text"])  # Antwort abrufen
        
        # Antworten an den Benutzer senden
        if responses:
            dispatcher.utter_message(text=" ".join(responses))
        else:
            dispatcher.utter_message(text="I don't know, if I got that right. Please try to ask question by question.")
        
        return []