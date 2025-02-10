from typing import Any, List, Dict, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import re

RASA_NLU_URL = "http://localhost:5005/model/parse"

class ActionHandleUnknownIntent(Action):
    def name(self) -> Text:
        return "action_handle_unknown_intent"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_topic = tracker.get_slot("topic")
        last_message = tracker.latest_message.get("text", "")

        # Falls ein Topic existiert, kombiniere es mit der letzten Nachricht
        if last_topic:
            combined_message = f"{last_topic} {last_message}"

            # Schicke die neue Nachricht zur Intent-Klassifikation an Rasa NLU
            response = requests.post(RASA_NLU_URL, json={"text": combined_message}).json()

            # Falls ein Intent erkannt wurde, extrahiere ihn
            recognized_intent = response.get("intent", {}).get("name")
            confidence = response.get("intent", {}).get("confidence", 0.0)

            if recognized_intent and confidence > 0.6:
                dispatcher.utter_message(template=f"utter_{recognized_intent}")  # Antwort aus domain.yml senden
                
                # **Thema nur für die aktuelle Anfrage verwenden, danach zurücksetzen**
                return [SlotSet("topic", None)]
            else:
                dispatcher.utter_message(text="I'm sorry, I didn't understand that. Can you clarify?")

                return [SlotSet("topic", None)]  
        else:
            dispatcher.utter_message(template="utter_please_rephrase")

            return [SlotSet("topic", None)]
        
        return []

class ActionHandleMultipleQuestions(Action):
    def name(self) -> Text:
        return "action_handle_multiple_questions"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_message = tracker.latest_message.get("text", "")

        sentences = re.split(r'[.!?Y]\s*', last_message.strip())

        detected_intents = set()
        responses = []
        treshold = 0.6

        for sentence in sentences:
            if not sentence.strip():
                continue
            response = requests.post(RASA_NLU_URL, json={"text": sentence}).json()
            recognized_intents = response.get("intent_ranking", [])

            for intent in recognized_intents:
                if intent["confidence"] > treshold:
                    intent_name = intent["name"]
                    intent_found = True
                    if intent_name not in detected_intents:
                        detected_intents.add(intent_name)
                        utter_action = f"utter_{intent_name}"
                        responses.append(domain.get("responses", {}).get(utter_action, [{"text": f""}])[0]["text"])
    
        if responses:
            dispatcher.utter_message(text=" ".join(responses))
        if not intent_found:
            dispatcher.utter_message(template="utter_please_rephrase")
        
        return []