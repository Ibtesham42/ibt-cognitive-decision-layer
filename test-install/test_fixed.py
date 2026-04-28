from ibtcode import IbtcodeSystem

engine = IbtcodeSystem()
response, state, decision = engine.process("My payment failed!")

print("Response:", response)
print("Emotion:", state.emotion)
print("Strategy:", decision.strategy)
print("Decision confidence:", decision.confidence)
