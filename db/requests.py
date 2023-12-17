import json
from pydantic import BaseModel, types, ConfigDict, validator, Field, conlist, field_validator, ValidationInfo
from pprint import pprint


file_characters = './db/characters.json'
file_dialogs = './db/dialogs.json'
# file_dialogs = './db/dialogs_test.json'
file_quests = './db/quests.json'


class Dialog(BaseModel):
    ident: str
    user: str
    npc: str
    responses: list[str]


class DB:
    def __init__(self):
        self.dialog_messages = {}
        self._init_dialogs()

    def get_characters(self):
        with open(file_characters) as fp:
            data = json.load(fp)
            return data

    def get_dialogs(self):
        return self.dialog_messages

    def get_quests(self):
        with open(file_quests) as fp:
            data = json.load(fp)
            return data

    def _init_dialogs(self):
        with open(file_dialogs) as fp:
            data = json.load(fp)
            self._convert_dialogs(data)

    def _convert_dialogs(self, dialogs_lst, prefix=''):
        messages_ids = []
        for dialog in dialogs_lst:
            answers = dialog['next']
            answers_ids = []
            if 'id' in dialog:
                prefix = dialog['id']
            if answers:
                answers_ids = self._convert_dialogs(answers, prefix)
            ident = dialog.get('id') or f'{prefix}_{len(self.dialog_messages)}'
            self.dialog_messages[ident] = Dialog(
                ident=ident,
                user=dialog['user'],
                npc=dialog['npc'],
                responses=answers_ids
            )
            messages_ids.append(ident)

        return messages_ids


if __name__ == "__main__":
    db = DB()
    pprint(db.get_characters())
    # pprint(db.get_dialogs())
    # pprint(db.get_quests())
