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
