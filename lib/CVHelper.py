from ultralytics import YOLO
from PIL import Image, ImageDraw
import numpy as np
import cv2
import os

class CVHelper:
    
    def __init__(self) ->None:
        self.model = YOLO("./lib/cv_models/icon-detector.pt")
    
    def preprocess_image(self, image_path, input_size=(640, 480)):
        """Görüntüyü modele uygun şekilde hazırlar."""
        image = cv2.imread(image_path)
        original_shape = image.shape[:2]  # (height, width)
        image_resized = cv2.resize(image, input_size)
        return image, image_resized, original_shape

    def postprocess(self, predictions, original_shape, conf_threshold=0.2, iou_threshold=0.5):
        """Tahminleri işler ve NMS uygular."""
        boxes = []
        scores = []
        class_ids = []
        coordinates_info = []  # Koordinat bilgilerini tutacak liste
        
        # YOLO sonuçlarını işle
        for box in predictions.boxes:
            conf = float(box.conf[0])
            if conf > conf_threshold:
                # Koordinatları al ve orijinal boyuta göre ayarla
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                
                boxes.append([x1, y1, x2, y2])
                scores.append(conf)
                class_id = int(box.cls[0])
                class_ids.append(class_id)
                
                # Her tespit için detaylı bilgileri sakla
                detection_info = {
                    'class_id': class_id,
                    'confidence': conf,
                    'bbox': {
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2,
                        'center_x': (x1 + x2) // 2,
                        'center_y': (y1 + y2) // 2,
                        'width': x2 - x1,
                        'height': y2 - y1
                    }
                }
                coordinates_info.append(detection_info)

        # NMS uygula
        indices = cv2.dnn.NMSBoxes(boxes, scores, conf_threshold, iou_threshold)
        
        if len(indices) > 0:
            filtered_boxes = [boxes[i] for i in indices.flatten()]
            filtered_scores = [scores[i] for i in indices.flatten()]
            filtered_class_ids = [class_ids[i] for i in indices.flatten()]
            filtered_coordinates = [coordinates_info[i] for i in indices.flatten()]
        else:
            filtered_boxes = []
            filtered_scores = []
            filtered_class_ids = []
            filtered_coordinates = []
            
        return filtered_boxes, filtered_scores, filtered_class_ids, filtered_coordinates
    
    def draw_boxes(self, image, boxes, scores, class_ids):
        """Bounding box'ları çiz."""
        for box, score, class_id in zip(boxes, scores, class_ids):
            x1, y1, x2, y2 = box
            color = (0, 255, 0)  # BGR formatta yeşil
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            label = f"Class {class_id}: {score:.2f}"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return image
    
    def run_inference(self):
        """YOLO modelini kullanarak tahmin yapar ve sonucu kaydeder."""
        image_path = "./lib/images/temp.png"
        
        # Görüntüyü hazırla
        image = cv2.imread(image_path)
        # original_image, resized_image, original_shape = self.preprocess_image(image_path)
        
        # YOLO ile tahmin yap
        results = self.model(image)
        
        # Tahminleri işle
        boxes, scores, class_ids, coordinates_info = self.postprocess(results[0], image.shape[:2])
        
        # Sonuçları görselleştir
        result_image = self.draw_boxes(image, boxes, scores, class_ids)
        
        # Sonucu kaydet
        output_path = "./lib/images/temp_procceeded.png"
        cv2.imwrite(output_path, result_image)
        print(f"Tahmin yapılan görüntü kaydedildi: {'temp_procceeded.png'}")
        
        # Koordinat bilgilerini döndür
        return coordinates_info