import base64

# EXIT SIGN IMAGE (base64 encoded)
data = b'''
iVBORw0KGgoAAAANSUhEUgAAAZAAAADICAYAAADQfF33AAAACXBIWXMAAAsSAAALEgHS3X78AAAg
AElEQVR4nOydd5Acx3nHf7O7szuzs9kxjzSkFBTwkN... (TRUNCATED)
'''

with open("exit.jpg", "wb") as f:
    f.write(base64.b64decode(data))

print("exit.jpg created!")
