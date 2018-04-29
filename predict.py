import pygame
import random
import numpy as np


class Box:
    def __init__(self, x, y, sizes):
        self.x = x
        self.y = y
        self.size = sizes


class NN:
    def __init__(self):
        self.X = np.array([[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]])
        self.weights = [np.random.randn(3, 3), np.random.randn(3, 2)]
        self.hidden_layer = sigmoid(np.dot(self.X, self.weights[0]))
        self.output = sigmoid(np.dot(self.hidden_layer, self.weights[1]))

    def train(self, x, target):
        # FeedForward
        self.hidden_layer = sigmoid(np.dot(x, self.weights[0]))
        self.output = sigmoid(np.dot(self.hidden_layer, self.weights[1]))

        # BackPropagation
        output_delta = (target - self.output)*(self.output*(1-self.output))
        hidden_layer_delta = output_delta.dot(self.weights[1].T)*(self.hidden_layer*(1-self.hidden_layer))
        self.weights[1] += self.hidden_layer.T.dot(output_delta)
        self.weights[0] += self.X.T.dot(hidden_layer_delta)


def sigmoid(z):
    """The sigmoid function."""
    return 1/(1+np.exp(-z))


pygame.init()

display_width = 400
display_height = 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)
rect_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# Box objects
box1 = Box(30, 80, 120)
box2 = Box(250, 80, 120)

# Text
smallText = pygame.font.Font("freesansbold.ttf", 20)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Color Predictor')

clock = pygame.time.Clock()

# Setting parameter for when to end game. That is when crashed is True game ends.
crashed = False

# NeuralNet
nn = NN()


def check():
    """ This function is called after mouse button is pressed."""
    mouse = pygame.mouse.get_pos()

    # mouse[0] = x-coordinate of mouse position.
    # mouse[1] = y-coordinate of mouse position.
    if box1.x + box1.size > mouse[0] > box1.x and box1.y + box1.size > mouse[1] > box1.y:
        return True
    elif box2.x + box2.size > mouse[0] > box2.x and box2.y + box2.size > mouse[1] > box2.y:
        return False
    return None


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def change_color():
    """This function returns random color."""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            # choice is the selected box. True if left box, false if right.
            choice = check()
            if choice is not None:
                if choice:
                    target_output = np.array([[1, 0]])
                else:
                    target_output = np.array([[0, 1]])
                nn.train(np.array([np.asarray(list(rect_color))]), target_output)
                # Change color every time a box is selected.
                rect_color = change_color()

    # Box-1
    pygame.draw.rect(gameDisplay, rect_color, (box1.x, box1.y, box1.size, box1.size))
    pygame.draw.rect(gameDisplay, white, (box1.x, box1.y, box1.size, box1.size), 1)
    # Box-2
    pygame.draw.rect(gameDisplay, rect_color, (box2.x, box2.y, box2.size, box2.size))
    pygame.draw.rect(gameDisplay, white, (box2.x, box2.y, box2.size, box2.size), 1)

    # Text in box 1
    textSurf, textRect = text_objects("BLACK", smallText, black)
    textRect.center = ((box1.x + (box1.size / 2)), (box1.y + (box1.size / 2)))
    gameDisplay.blit(textSurf, textRect)

    # Text in box 2
    textSurf, textRect = text_objects("WHITE", smallText, white)
    textRect.center = ((box2.x + (box2.size / 2)), (box2.y + (box2.size / 2)))
    gameDisplay.blit(textSurf, textRect)

    # Displaying predicted output using circle
    output = nn.output.flatten()

    if output[0] > output[1]:
        pygame.draw.circle(gameDisplay, white, (box1.x + box1.size // 2, box1.y + box1.size + 10), 5)
        pygame.draw.circle(gameDisplay, black, (box2.x + box2.size // 2, box2.y + box2.size + 10), 5)

    else:
        pygame.draw.circle(gameDisplay, white, (box2.x + box2.size // 2, box2.y + box2.size + 10), 5)
        pygame.draw.circle(gameDisplay, black, (box1.x + box1.size // 2, box1.y + box1.size + 10), 5)

    # Update pygame display
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
