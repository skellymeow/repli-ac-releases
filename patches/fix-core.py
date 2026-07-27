from pathlib import Path

path = Path("app/src/core.ts")
text = path.read_text(encoding="utf-8")

text = text.replace(
    'export function settingsOpen(model: Model): boolean { return model.settingsOpen; }\n',
    '',
)
text = text.replace(
    'export function modelPickerOpen(model: Model): boolean { return model.modelPickerOpen; }\n',
    '',
)

start = text.index('function chatCommand(model: Model, turns: readonly Turn[]): Cmd<Msg> {')
end = text.index('\n\nexport function update', start)
text = text[:start] + text[end + 2:]

text = text.replace(
    '        chatCommand(model, turns),\n',
    '''        Cmd.fetch(\n          {\n            url: model.endpoint,\n            method: "POST",\n            headers: { authorization: bearerToken(model.apiKey), "content-type": "application/json", "x-stitch-token": model.bridgeToken },\n            body: encodeChatRequest(model.modelName, model.autoMode ? AUTO_SYSTEM_PROMPT : SYSTEM_PROMPT, turns),\n            timeoutMs: 600000,\n          },\n          { key: "chat", ok: "chat_response", err: "chat_failed" },\n        ),\n''',
    1,
)
text = text.replace(
    '      return [{ ...model, phase: "sending", failReason: new Uint8Array(0) }, chatCommand(model, model.turns)];\n',
    '''      return [\n        { ...model, phase: "sending", failReason: new Uint8Array(0) },\n        Cmd.fetch(\n          {\n            url: model.endpoint,\n            method: "POST",\n            headers: { authorization: bearerToken(model.apiKey), "content-type": "application/json", "x-stitch-token": model.bridgeToken },\n            body: encodeChatRequest(model.modelName, model.autoMode ? AUTO_SYSTEM_PROMPT : SYSTEM_PROMPT, model.turns),\n            timeoutMs: 600000,\n          },\n          { key: "chat", ok: "chat_response", err: "chat_failed" },\n        ),\n      ];\n''',
    1,
)

path.write_text(text, encoding="utf-8")
