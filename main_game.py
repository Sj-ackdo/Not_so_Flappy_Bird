import cv2
import pygame
import landmark_setup as setup
import landmarking as landmark
import threading

DEVICE = "/dev/video0"

pygame.init()
clock = pygame.time.Clock()
screen_size = (640, 480)
screen_size = (1280, 720)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Not so Flappy Bird")

cap = cv2.VideoCapture(DEVICE, cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)


thread = threading.Thread(target=landmark.hand_landmarker, args=(cap,), daemon=True)

try:
    thread.start()
    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        frame = setup.latest_frame
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.transpose(frame)
            surface = pygame.surfarray.make_surface(frame)
            screen.blit(surface, (0, 0))
        
        
        

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
