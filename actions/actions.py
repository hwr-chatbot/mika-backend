from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from rasa_sdk.interpreter import RasaNLUInterpreter

class ActionSetTopic(Action):
    def name(self):
        return "action_set_topic"

    def run(self, dispatcher, tracker, domain):
        intent_to_topic = {
            "study_without_a-level": "a-level",
            "guest_auditor": "guest auditor",
            "english_certificate": "english certificate",
            "cv": "cv",
            "motivational_letter": "motivational letter"
            "admission_requirement": "admission",
            "prerequisite_admission": "admission",
            "admission_documents": "admission"
            "application_from_international_university": "application",
            "aps_needed": "aps",
            "whats_aps": "aps",
            "aps_hand_in_late": "aps",
            "missed_deadline": "deadline",
            "application_deadline", "deadline",
            "where_to_apply": "application",
            "application_many_programs_possible", "application",
            "application_many_programs_needed": "application",
            "application_many_programs_chance_increase": "application",
            "application_status": "application",
            "application_status_uni_assist": "application",
            "eligibility": "eligibility",
            "eligibility_check": "eligibility",
            "eligibility_master": "eligibility",
            "eligibility_check_who": "eligibility",
            "whats_gmat": "gmat",
            "gmat_needed": "gmat",
            "hwr_gmat_test": "gmat",
            "gre_instead_gmat": "gmat",
            "semester_start": "semester",
            "time_span_semester": "semester",
            "work_experience_accepted": "work experience",
            "swap_work_experience": "work experience",
        }
        
        current_intent = tracker.latest_message['intent'].get('name')
        topic = intent_to_topic.get(current_intent, None)
        
        if topic:
            dispatcher.utter_message(text=f"I will remember that your topic is {topic}.")
            return [SlotSet("topic", topic)]
        return []

class ActionRespondBasedOnTopic(Action):
    def name(self):
        return "action_respond_based_on_topic"

    def run(self, dispatcher, tracker, domain):
        # Gespeichertes Thema aus dem Slot abrufen
        topic = tracker.get_slot("topic")
        user_message = tracker.latest_message.get("text", "").strip().lower()

        # Falls kein Thema gespeichert ist, nachfragen
        if not topic:
            dispatcher.utter_message(text="I need more context. What topic are we discussing?")
            return []

        # Nutzerfrage mit dem Thema kombinieren
        combined_query = f"{topic} - {user_message}"

        # NLU-Modell zur Intent-Erkennung verwenden
        interpreter = RasaNLUInterpreter("models/nlu")  # Lade das trainierte NLU-Modell
        parsed_result = interpreter.parse(combined_query)  # Analysiere die neue kombinierte Eingabe

        # Intent und Konfidenz abrufen
        recognized_intent = parsed_result.get("intent", {}).get("name", None)
        confidence = parsed_result.get("intent", {}).get("confidence", 0)

        # Mindestkonfidenz für gültige Erkennung setzen
        if recognized_intent and confidence > 0.7:
            dispatcher.utter_message(response=f"utter_{recognized_intent}")
        else:
            dispatcher.utter_message(text=f"I'm not sure about that. Could you clarify your question regarding {topic}?")

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