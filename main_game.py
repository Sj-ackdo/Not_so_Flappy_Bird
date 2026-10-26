import cv2
import pygame
import landmark_setup as setup
import landmarking as landmark
import threading
import pipe as pp
import player
import random

DEVICE = "/dev/video0"

pygame.init()
clock = pygame.time.Clock()
screen_size = (640, 480)
#screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Not so Flappy Bird")

cap = cv2.VideoCapture(DEVICE, cv2.CAP_V4L2)

#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#cap.set(cv2.CAP_PROP_FPS, 30)



pipe = pygame.image.load("pipe_image.png").convert_alpha()
flip_pipe = pygame.transform.flip(pipe, False, True)

player_image = pygame.image.load("chimken.png").convert_alpha()
player = player.Sprite(player_image, screen)

thread = threading.Thread(target=landmark.hand_landmarker, args=(cap,), daemon=True)
pipe_spawner = pp.PipeSpawner(screen_size[0], screen_size[1],
                              3, pipe, flip_pipe, player, screen)

try:
    thread.start()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                pp.stop = False
                player.reset_position()
                pipe_spawner = pp.PipeSpawner(screen_size[0], screen_size[1], 
                                              3, pipe, flip_pipe, player, screen)

        frame = setup.latest_frame
        mid_hand = setup.mid_hand
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.transpose(frame)
            surface = pygame.surfarray.make_surface(frame)
            screen.blit(surface, (0, 0))
            if not pp.stop:
                if mid_hand is None:
                    player.draw_player((screen_size[0]//2, screen_size[1]//2))
                    player.reset_position()
                    pipe_spawner.update(player.player_rect)
                else:
                    player.draw_player(mid_hand)
                    pipe_spawner.update(player.player_rect)
                pipe_spawner.draw()
             

        pygame.display.flip()
        clock.tick(30)

except KeyboardInterrupt:
    print("\n Graceful shutdown...")
finally:
    thread.join(timeout=3)
    cap.release()
    pygame.quit()
    cv2.destroyAllWindows()
    print("Cleanup finsished")
