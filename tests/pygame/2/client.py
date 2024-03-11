from pymultiplayer import MultiplayerClient
from player import Player
from json import dumps
import pygame as p

self = None
other_players = []
running = True
velocity = 5


async def send_update():
    msg = {"type": "update", "content": {"x": self.x, "y": self.y}, "id": self.id}
    await client.send(dumps(msg))
    print("Sent update")


def msg_handler(msg):
    print(msg)
    if msg["type"] == "client_joined":
        other_players.append(Player(msg["content"]))

    elif msg["type"] == "client_left":
        for player in other_players:
            if player.id == msg["content"]:
                other_players.remove(player)

    elif msg["type"] == "update":
        for player in other_players:
            if player.id == msg["id"]:
                player.x = msg["content"]["x"]
                player.y = msg["content"]["y"]


async def proxy(websocket):
    global self, running
    self = Player(client.id + 1)

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            elif event.type == p.KEYDOWN:
                if event.key == p.K_UP:
                    self.y -= velocity

                elif event.key == p.K_DOWN:
                    self.y += velocity

                elif event.key == p.K_LEFT:
                    self.x -= velocity

                elif event.key == p.K_RIGHT:
                    self.x += velocity

                await send_update()

        screen.fill((0, 0, 0))

        p.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        for player in other_players:
            p.draw.rect(screen, player.colour, (player.x, player.y, player.width, player.height))

        clock.tick(60)
        p.display.update()

if __name__ == "__main__":
    p.init()
    screen = p.display.set_mode((500, 500))
    p.display.set_caption("Client")
    clock = p.time.Clock()

    client = MultiplayerClient(msg_handler)
    client.run(proxy)
