import js
import random


CHAR_WIDTH = 10
CHAR_HEIGHT = 10
CHANGE_PROB = 0.1
WORD_PROB = 0.05
REFRESH_RENDER = 1000 // 10


class TextLetter:
    def __init__(self, element):
        self.img = js.Image.new()
        self.img.onload = lambda event: self.render(element, self.img, {})
        self.img.src = '/assets/logo.png'

        self.words = ['dev', 'python', 'django', 'docker', 'backend', 'frontend', 'pyscript', 'micropython']
        self.letters = '01234567890!@#$%^&*()'
 
    def get_canvas(self, w, h):
        canvas = js.document.createElement('canvas')
        canvas.width, canvas.height = w // CHAR_WIDTH, h // CHAR_HEIGHT
        ctx = canvas.getContext('2d')
        ctx.drawImage(self.img, 0, 0, canvas.width, canvas.height)
        return ctx.getImageData(0, 0, canvas.width, canvas.height)

    def generate_text(self, width, height, text):
        text = text.replace('\n', '') if text else ''
        canvas = self.get_canvas(width, height)
        chars = []
        sequence = None

        for i in range(canvas.height * canvas.width):
            if canvas.data[i * 4] < 120 and not canvas.data[i * 4 + 3] < 50:
                if sequence is None: sequence = i
                if not text or random.random() < CHANGE_PROB:
                    word = random.choice(self.words)
                    if len(self.words) > 0 and random.random() < WORD_PROB and i + 1 - sequence >= len(word):
                        chars = chars[:-len(word)] + list(word)
                    chars.append(random.choice(self.letters))
                else:
                    chars.append(text[i])
            else:
                chars.append(' ')
                sequence = None
            if (i + 1) % canvas.width == 0:
                chars.append('\n')
                sequence = None
        return ''.join(chars)

    def render(self, element, image, previous):
        element.style.height = f"{element.clientWidth * 0.5}px"

        text = self.generate_text(
            element.clientWidth,
            element.clientHeight,
            previous.get('text') if previous.get('w') == element.clientWidth and previous.get('h') == element.clientHeight else None,
        )
        element.textContent = text
        js.setTimeout(lambda: self.render(element, image, {'w': element.clientWidth, 'h': element.clientHeight, 'text': text}), REFRESH_RENDER)
