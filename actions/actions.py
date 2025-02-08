from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted

# class ActionSetTopic(Action):
#     def name(self) -> Text:
#         return "action_set_topic"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # Mapping von Intent-Namen zu Themen
#         intent_to_topic = {
#             "study_without_a-level": "a-level",
#             "guest_auditor": "guest auditor",
#             "english_certificate": "english certificate",
#             "cv": "cv",
#             "motivational_letter": "motivational letter",
#             "admission_requirement": "admission",
#             "prerequisite_admission": "admission",
#             "admission_documents": "admission",
#             "application_from_international_university": "application",
#             "aps_needed": "aps",
#             "whats_aps": "aps",
#             "aps_hand_in_late": "aps",
#             "missed_deadline": "deadline",
#             "application_deadline": "deadline",
#             "where_to_apply": "application",
#             "application_many_programs_possible": "application",
#             "application_many_programs_needed": "application",
#             "application_many_programs_chance_increase": "application",
#             "application_status": "application",
#             "application_status_uni_assist": "application",
#             "eligibility": "eligibility",
#             "eligibility_check": "eligibility",
#             "eligibility_master": "eligibility",
#             "eligibility_check_who": "eligibility",
#             "whats_gmat": "gmat",
#             "gmat_needed": "gmat",
#             "hwr_gmat_test": "gmat",
#             "gre_instead_gmat": "gmat",
#             "semester_start": "semester",
#             "time_span_semester": "semester",
#             "work_experience_accepted": "work experience",
#             "swap_work_experience": "work experience",
#         }

#         recognized_intent = tracker.latest_message.get("intent", {}).get("name", "unknown")
#         confidence = tracker.latest_message.get("intent", {}).get("confidence", 0.0)
#         topic = intent_to_topic.get(recognized_intent, None)

#         if topic:
#             dispatcher.utter_message(text=f"I will remember that your topic is {topic}.")
#             return [SlotSet("topic", topic), SlotSet("last_intent", recognized_intent)]
#         else:
#             dispatcher.utter_message(text="I could not determine the topic from your input. Could you please clarify?")
#             return [SlotSet("topic", None), SlotSet("last_intent", None)]

class ActionHandleUnknownIntent(Action):
    def name(self) -> Text:
        return "action_handle_unknown_intent"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_topic = tracker.get_slot("topic")
        last_message = tracker.latest_message.get("text", "")

        print(f"🔍 DEBUG: Action aufgerufen!")
        print(f"🔍 DEBUG: Last Topic = {last_topic}")
        print(f"🔍 DEBUG: Last Message = {last_message}")

        if last_topic:
            combined_message = f"{last_topic} {last_message}"
            print(f"🔍 DEBUG: Kombinierte Nachricht = {combined_message}")

            # Ersetze die letzte Nutzereingabe mit der kombinierten Nachricht
            return [
                SlotSet("combined_message", combined_message),
                UserUtteranceReverted()  # Erzwingt eine erneute Intent-Klassifikation
            ]
        else:
            print("🔍 DEBUG: Kein Topic-Slot gefunden, normale Fallback-Antwort wird verwendet.")
            dispatcher.utter_message(response="Ich bin mir nicht sicher, was du meinst. Kannst du es anders formulieren?")
            return [UserUtteranceReverted()]

