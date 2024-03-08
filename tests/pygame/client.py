from pymultiplayer import MultiplayerClient
from json import dumps
from player import Player
import pygame as p

self = None
other_players = []
velocity = 5
running = True


async def send_update():
    msg = {"type": "update", "content": {"x": self.x, "y": self.y}, "id": self.id}
    print(msg)
    await client.send(dumps(msg))


async def main():
    for event in p.event.get():
        if event.type == p.QUIT:
            global running
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

    print("a")
    screen.fill((0, 0, 0))
    print("0")
    for player in other_players:
        p.draw.rect(screen, player.colour, (player.x, player.y, player.width, player.height))
    print("1")
    p.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
    print("2")
    p.display.update()
    print("3")


async def msg_handler(msg):
    if msg["type"] == "client_joined":
        print("Client joined")
        global other_players
        other_players.append(Player(msg["content"]))

    elif msg["type"] == "client_left":
        print("Client left")
        for player in other_players:
            if player.id == msg["content"]:
                other_players.remove(player)
                break


async def proxy(websocket):
    global self
    self = Player(client.id + 1)
    while running:
        await client.handle_msgs()
        await main()

    p.quit()
    client.disconnect()


if __name__ == "__main__":
    p.init()
    p.display.set_caption("Multiplayer Test")
    screen = p.display.set_mode((500, 500))
    clock = p.time.Clock()
    running = True

    client = MultiplayerClient(msg_handler)
    client.run(proxy)
