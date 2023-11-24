import os

from initialsolution import initial_solution
from readProblemInstances import readProblemInstances

def process_file(file_path):
    # Belirli bir kodu çağırın veya dosya üzerinde istediğiniz işlemleri gerçekleştirin
    # Örnek olarak, dosyanın içeriğini ekrana yazdıralım
    with open(file_path, 'r') as file:
        content = file.read()
        print("file name : ",file_path)
        
def test_files_in_directory(directory):
    # Dizin içindeki tüm dosya adlarını al
    file_list = os.listdir(directory)

    # Dosya adlarını tam dosya yollarına dönüştür
    file_paths = [os.path.join(directory, file) for file in file_list]
    print(file_paths)
    return file_paths

            


