import face_recognition
import os
import pickle
import cv2
from PIL import Image
from alive_progress import alive_bar
import time 

class model:
    def name_to_color(self,name):
        color = [(ord(c.lower())-97)*8 for c in name[:3]]
        return color
    def resize(self,image):
        (h,w) = image.shape[:2]
        width=500
        ratio= width/float(w)
        height=int(h*ratio)
        image=cv2.resize(image,(width,height))
        return image
    
    def train(self):
        KNOWN_FACES_DIR =  'data/' 
        n=0

        FRAME_THICKNESS = 3
        FONT_THICKNESS = 2
        TOLERANCE = 0.435
        MODEL = 'hog'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model
        known_faces = []
        known_names = []
        Names = os.listdir(KNOWN_FACES_DIR)
        print('Variables_initialized')
        for name in os.listdir(KNOWN_FACES_DIR) :
            print('Training ',name,'s data ',sep='')
            for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
                if('.jpg' not in filename):
                    continue
                try:
                    image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
                    image= self.resize(image)
                    encoding = face_recognition.face_encodings(image)[0]
                except:
                    n=n+1
                    print('err for',name,n)
                    pass
                known_faces.append(encoding)
                known_names.append(name)
        with open('known_faces.pkl', 'wb') as f:
            pickle.dump(known_faces, f)
        with open('known_names.pkl', 'wb') as f:
            pickle.dump(known_names, f)
        print( 'files loaded')
    def predict(self):
        MODEL = 'hog'
        FRAME_THICKNESS = 3
        FONT_THICKNESS = 2
        TOLERANCE = 0.435
        Attendance = []
        with open('known_faces.pkl', 'rb') as f:
            known_faces= pickle.load(f)
        with open('known_names.pkl', 'rb') as f:
            known_names= pickle.load(f)
        print('Processing unknown faces...')

        cap=cv2.VideoCapture(0)
        while(True):
            ret,image=cap.read()
            # image= resize(image1)
    
            locations = face_recognition.face_locations(image, model=MODEL)
            encodings = face_recognition.face_encodings(image, locations)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            print(f', found {len(encodings)} face(s)')
            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
                match = None
                if True in results:  
                    match = known_names[results.index(True)] 
                    print(f' - {match} from {results}')
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])
                
                    color = self.name_to_color(match)
                    cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 15)
                    cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
                    cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
                    Attendance.append(match)
            cv2.imshow('Screen', image)              
            if cv2.waitKey(1) == 13 : #13 is the Enter Key
                  break
        cap.release()
        cv2.destroyAllWindows()
    
        return Attendance
