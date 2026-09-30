#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Vision & Motion Engine
Performs real-time face detection, user presence tracking, and hand gesture recognition using OpenCV.
Compatible with OpenCV 4.x and 5.x.
"""

import cv2
import numpy as np
import time
import sys

class JarvisVisionEngine:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        
        # Safe initialization for OpenCV CascadeClassifier (CV 4.x vs 5.x)
        self.face_cascade = None
        if hasattr(cv2, 'CascadeClassifier'):
            try:
                cascade_path = getattr(cv2, 'data', None)
                if cascade_path and hasattr(cascade_path, 'haarcascades'):
                    xml_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                    self.face_cascade = cv2.CascadeClassifier(xml_path)
            except Exception as e:
                print(f"[Vision Engine Warning] CascadeClassifier init skipped: {e}", file=sys.stderr)
        
        self.prev_frame = None
        self.user_present = False
        self.last_presence_change = 0
        self.gesture_cooldown = 0
        
    def start_camera(self):
        """웹캠 카메라 스트림 초기화"""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print(f"[Vision Engine Error] Cannot open camera device {self.camera_index}", file=sys.stderr)
            return False
        print(f"[Vision Engine] Camera index {self.camera_index} initialized successfully.")
        return True

    def stop_camera(self):
        """웹캠 카메라 닫기"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("[Vision Engine] Camera closed.")

    def detect_face_presence(self, frame_gray):
        """얼굴 탐지 및 움직임을 통한 사용자 착석/부재 판정"""
        if self.face_cascade is not None and not self.face_cascade.empty():
            try:
                faces = self.face_cascade.detectMultiScale(
                    frame_gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(60, 60)
                )
                return len(faces) > 0, faces
            except Exception:
                pass
        
        # Fallback to motion-based presence detection
        motion_score = self.detect_motion(frame_gray)
        return motion_score > 0.02, []

    def detect_motion(self, frame_gray):
        """프레임 차분법을 통한 움직임(Motion) 크기 계산"""
        if self.prev_frame is None:
            self.prev_frame = frame_gray
            return 0.0
            
        frame_delta = cv2.absdiff(self.prev_frame, frame_gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        motion_score = np.sum(thresh) / (thresh.shape[0] * thresh.shape[1])
        self.prev_frame = frame_gray
        return motion_score

    def classify_gesture(self, frame):
        """손 윤곽선 및 움직임 영역 기반 제스처 판정"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        mask = cv2.blur(mask, (3, 3))
        
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
            
        max_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(max_contour)
        
        if area > 10000:
            hull = cv2.convexHull(max_contour, returnPoints=False)
            if len(hull) > 3 and len(max_contour) > 3:
                defects = cv2.convexityDefects(max_contour, hull)
                finger_count = 0
                if defects is not None:
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(max_contour[s][0])
                        end = tuple(max_contour[e][0])
                        far = tuple(max_contour[f][0])
                        a = np.linalg.norm(np.array(end) - np.array(start))
                        b = np.linalg.norm(np.array(far) - np.array(start))
                        c = np.linalg.norm(np.array(end) - np.array(far))
                        angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c + 1e-5))
                        if angle <= np.pi / 2 and d > 1000:
                            finger_count += 1
                
                if finger_count >= 4:
                    return "OPEN_PALM"  # 손바닥 펼치기 (정지/일시정지)
                elif finger_count == 2:
                    return "VICTORY"    # V 포즈 (1분 브리핑 시작)
                elif finger_count == 0:
                    return "THUMBS_UP"  # 주먹/엄지 척 (확인/승인)
        return None

    def run_detection_loop(self, callback=None, show_window=False):
        """비전 인식 메인 루프"""
        if not self.start_camera():
            return
            
        print("[Vision Engine] 🎥 실시간 웹캠 감지 루프 가동 중...")
        
        try:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    time.sleep(0.1)
                    continue
                    
                frame = cv2.flip(frame, 1)  # 좌우 반전
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR_GRAY)
                gray_blurred = cv2.GaussianBlur(gray, (21, 21), 0)
                
                now = time.time()
                is_present, faces = self.detect_face_presence(gray)
                
                # Draw faces if present
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Presence state change
                if is_present != self.user_present and (now - self.last_presence_change > 3.0):
                    self.user_present = is_present
                    self.last_presence_change = now
                    event_type = "USER_ARRIVED" if is_present else "USER_DEPARTED"
                    print(f"[Vision Event] {event_type}")
                    if callback:
                        callback(event_type, {"present": is_present})
                
                # Gesture classification
                if now - self.gesture_cooldown > 2.5:
                    gesture = self.classify_gesture(frame)
                    if gesture:
                        self.gesture_cooldown = now
                        print(f"[Vision Event] GESTURE_DETECTED: {gesture}")
                        if callback:
                            callback("GESTURE_DETECTED", {"gesture": gesture})
                
                if show_window:
                    cv2.imshow("Jarvis Vision Engine", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                        
                time.sleep(0.05)  # 20 FPS Cap
                        
        finally:
            self.stop_camera()

if __name__ == "__main__":
    def print_event(event_type, details):
        print(f">> [EVENT TRIGGERED] Type: {event_type}, Details: {details}")

    engine = JarvisVisionEngine()
    engine.run_detection_loop(callback=print_event, show_window=False)
