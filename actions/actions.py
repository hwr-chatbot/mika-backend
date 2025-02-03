from typing import Any, List, Dict, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionSetTopic(Action):
    def name(self) -> Text:
        return "action_set_topic"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Mapping von Intent-Namen zu Themen
        intent_to_topic = {
            "study_without_a_level": "a-level",
            "guest_auditor": "guest auditor",
            "english_certificate": "english certificate",
            "cv": "cv",
            "motivational_letter": "motivational letter",
            "admission_requirement": "admission",
            "prerequisite_admission": "admission",
            "admission_documents": "admission",
            "application_from_international_university": "application",
            "aps_needed": "aps",
            "whats_aps": "aps",
            "aps_hand_in_late": "aps",
            "missed_deadline": "deadline",
            "application_deadline": "deadline",
            "where_to_apply": "application",
            "application_many_programs_possible": "application",
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

        # Sicherer Zugriff auf den erkannten Intent
        current_intent = tracker.latest_message.get("intent", {}).get("name")
        topic = intent_to_topic.get(current_intent)

        print("Latest message:", tracker.latest_message)
        print("Erkannter Intent:", recognized_intent, "mit Konfidenz:", confidence)
        print("Topic Slot:", topic)


        if topic:
            dispatcher.utter_message(text=f"I will remember that your topic is {topic}.")
            return [SlotSet("topic", topic)]
        else:
            # Falls kein passendes Thema gefunden wurde, fragen wir nach.
            dispatcher.utter_message(
                text="I could not determine the topic from your input. Could you please clarify?"
            )
            return [SlotSet("topic", None)]


class ActionRespondBasedOnTopic(Action):
    def name(self) -> Text:
        return "action_respond_based_on_topic"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Gespeichertes Thema aus dem Slot abrufen
        topic = tracker.get_slot("topic")
        if not topic:
            dispatcher.utter_message(
                text="I need more context. What topic are we discussing?"
            )
            return []

        # Erkannten Intent und dessen Konfidenz aus der neuesten Nachricht abrufen
        intent_info = tracker.latest_message.get("intent", {})
        recognized_intent = intent_info.get("name")
        confidence = intent_info.get("confidence", 0)

        # Mindestkonfidenz für eine sichere Erkennung
        if recognized_intent and confidence > 0.7:
            # Hier wird versucht, die Antwort aus den domain-Templates zu ziehen.
            # In aktuellen Rasa-Versionen kann dispatcher.utter_message(template=...) genutzt werden.
            dispatcher.utter_message(template=f"utter_{recognized_intent}")
        else:
            dispatcher.utter_message(
                text=f"I'm not sure about that. Could you clarify your question regarding {topic}?"
            )

        return []


class HandleMultipleIntents(Action):
    def name(self) -> Text:
        return "action_handle_multiple_intents"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Abrufen der Liste der erkannten Intents (Intent-Ranking)
        intents = tracker.latest_message.get("intent_ranking", [])
        max_intents = 3

        # Sicherstellen, dass im Domain-Dictionary Antworten hinterlegt sind
        domain_responses = domain.get("responses", {})

        responses = []
        for intent in intents[:max_intents]:
            intent_name = intent.get("name")
            response_key = f"utter_{intent_name}"
            # Überprüfen, ob ein entsprechender Antwort-Template vorhanden ist
            if response_key in domain_responses and domain_responses[response_key]:
                # Hier nehmen wir den ersten Eintrag aus der Liste der Antworten
                response_text = domain_responses[response_key][0].get("text", "")
                if response_text:
                    responses.append(response_text)

        if responses:
            # Die gesammelten Antworten werden kombiniert und ausgegeben.
            dispatcher.utter_message(text=" ".join(responses))
        else:
            dispatcher.utter_message(
                text="I don't know if I got that right. Please try to ask one question at a time."
            )
        return []
