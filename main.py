import cv2
import numpy as np
import random

WIDTH, HEIGHT = 640, 480
cap = cv2.VideoCapture(0)

score = 0
enemy_radius = 25
garis_batas = int(HEIGHT * 0.4) 
enemy = [random.randint(100, WIDTH-100), 0, 8]

def apply_morphology(mask_img):
    kernel = np.ones((7, 7), np.uint8)
    cleaned = cv2.erode(mask_img, kernel, iterations=1)
    cleaned = cv2.dilate(cleaned, kernel, iterations=2)
    return cleaned

def draw_dashed_line(img, y_pos):
    dist = 20 
    for i in range(0, WIDTH, dist*2):
        cv2.line(img, (i, y_pos), (i + dist, y_pos), (255, 255, 255), 1)
    cv2.putText(img, "Batas Tangan", (10, y_pos - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

while True:
    ret, frame = cap.read()
    if not ret: break
    
    frame = cv2.flip(frame, 1)
    focus_frame = frame[0:HEIGHT, 80:WIDTH-80] 
    display_f = focus_frame.copy()
    h, w, _ = display_f.shape

    hsv = cv2.cvtColor(display_f, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 20, 60], dtype=np.uint8)
    upper_skin = np.array([25, 255, 255], dtype=np.uint8)
    
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    mask_cleaned = apply_morphology(mask)
    
    draw_dashed_line(display_f, garis_batas)

    contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    palm_center = None
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) > 3000:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                if cy > garis_batas:
                    palm_center = (cx, cy)
                    w_w, w_h = 20, 150
                    p1 = (cx - w_w//2, cy - w_h)
                    p2 = (cx + w_w//2, cy)
                    cv2.rectangle(display_f, p1, p2, (0, 255, 255), -1)
                    cv2.rectangle(display_f, p1, p2, (255, 255, 255), 2)
                    sword_rect = (p1, p2)

    enemy[1] += enemy[2]
    cv2.circle(display_f, (enemy[0]-80, enemy[1]), enemy_radius, (0, 0, 255), -1)
    
    if palm_center:
        s_p1, s_p2 = sword_rect
        ex, ey = enemy[0]-80, enemy[1]
        if (s_p1[0] < ex < s_p2[0]) and (s_p1[1] < ey < s_p2[1]):
            score += 1
            enemy = [random.randint(100, WIDTH-100), 0, random.randint(8, 15)]

    if enemy[1] > HEIGHT:
        enemy = [random.randint(100, WIDTH-100), 0, 8]
        score = max(0, score - 1)

    cv2.putText(display_f, f"SCORE: {score}", (20, 40), 
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)
    
    cv2.imshow("Game PCV", display_f)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
