import os
from imaging_interview import compare_frames_change_detection, preprocess_image_change_detection

class duplicateDeleter:
  def __init__(self, folder=r"/content/dataset", max_score=1000, min_contour_area=100):
    self.folder = folder
    self.min_contour_area = min_contour_area
    self.max_score = max_score
    self.files_to_delete = []
    self.height = 480
    self.width = 640
    self.dim = (self.width, self.height)

  def compare(self, img_i, img_j):
    img_i = cv2.resize(img_i, self.dim)
    img_j = cv2.resize(img_j, self.dim)

    # preprocess the image and get the grayscaled image
    gray_img_i = preprocess_image_change_detection(img_i)
    gray_img_j = preprocess_image_change_detection(img_j)

    # compare two image files
    score, res_cnts, thresh = compare_frames_change_detection(gray_img_i, gray_img_j, self.min_contour_area)

    # if score is below max_score, return True
    if(score < self.max_score):
      return True
    else:
      return False

  def findDuplicate(self):
    # Get a list of files in the folder
    file_list = os.listdir(self.folder)
    for i in range(len(file_list)):
      for j in range(i+1, len(file_list)):
        # Get path to files
        path_i = os.path.join(self.folder, file_list[i])
        path_j = os.path.join(self.folder, file_list[j])

        # check if the file that we are comparing is already in a list of files to be deleted
        if(path_j in self.files_to_delete or path_i in self.files_to_delete):
          continue

        # read and resize the image to same size to compare
        img_i = cv2.imread(path_i, flags=cv2.IMREAD_COLOR)
        img_j = cv2.imread(path_j, flags=cv2.IMREAD_COLOR)

        comparion = False
        # If image cannot be opened continue to next
        if(img_i is None or img_j is None):
          print("Error while opening one of the image!")
          continue
        else:
          comparison = self.compare(img_i, img_j)

        # if files are similar, then add the file to the list to delete
        if(comparison):
          self.files_to_delete.append(path_j)

  def delete(self):
    # delete all duplicate images
    for file in self.files_to_delete:
      # if file exists, delete them
      if(os.path.exists(file)):
        print("deleting:", file)
        os.remove(file)

  def process(self):
    self.findDuplicate()
    self.delete()

if __name__ == '__main__':
  duplicate_deleter = duplicateDeleter()
  duplicate_deleter.process()