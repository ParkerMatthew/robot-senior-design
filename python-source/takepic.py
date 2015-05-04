import cv2

cap = cv2.VideoCapture(0)
cap.set(3,352)
cap.set(4,288)
cap.set(12,.190)
ret, im = cap.read()

del(cap)

cv2.imwrite(r'/root/temp.png', im)
