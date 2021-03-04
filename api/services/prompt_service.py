from api import models, db, helpers

class PromptService(object):
    def __init__(self):
        self.user_phone = None

    def add_prompt_response(self, jsonData):
        data = jsonData['results']
        user_phone = helpers.fetch_by_key('urn', jsonData['contact'])
        self.user_phone = helpers.sanitize_phone_string(user_phone)
        for key in data:
            if key != 'result' and 'category' in data[key]:
                prompt_name = helpers.remove_last_string_separated_by(data[key]['category'])
                ivr_prompt_details = models.IvrPrompt.query.get_by_name(prompt_name)
                if ivr_prompt_details:
                    if "TIME-OPTIN" in ivr_prompt_details.prompt_name:
                        self.selected_time_slot = self.fetch_prompt_response(data[key]['category'])

                    ivr_prompt_response = models.IvrPromptResponse(
                        prompt_name = ivr_prompt_details.prompt_name,
                        prompt_question = ivr_prompt_details.prompt_question,
                        user_phone = self.user_phone,
                        response = data[key]['category'],
                        content_id = ivr_prompt_details.content_id
                    )
                    db.session.add(ivr_prompt_response)
                    db.session.commit()

    def fetch_prompt_response(self, prompt):
        split_prompt_by_hyphen = helpers.split_prompt_by_hyphen(prompt)
        split_prompt_by_underscore = helpers.split_prompt_by_underscore(split_prompt_by_hyphen[-1])
        return split_prompt_by_underscore[1] if len(split_prompt_by_underscore) > 1 else None
