import psutil, os, numpy
from icecream import ic
from DICOMReader import DICOMReader
import vtkmodules.all as vtk

# invald path
# absolute_path = "C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data\\Case005\\Case005\\NRRDS\\001_LOCALIZER_3_PLANE_"

# # valid path
absolute_path = "C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data\\enc_files"

## mixed invalid path
# absolute_path = 'C:\\Users\\vardo\\OneDrive\\Documents\\Github\\ImageUntangler\\internal_data\\MRI_Data\\Filename_test'

test_dicom_reader = DICOMReader(absolute_path)

print(test_dicom_reader.get_sequence_list())
print(len(test_dicom_reader))

zcoords = []
for i in test_dicom_reader['cor  2D FIESTA']:
    zcoords.append(i[0])

print(len(zcoords))

dz = []
for i in range(1, len(zcoords)-1):
    dz.append(zcoords[i-1] - zcoords[i])
# TODO: ask moti about the unevenly spaced SliceLocations

print((zcoords[0] - zcoords[-1])/(len(zcoords) - 1))


def test_class_method():
    if DICOMReader.test_folder(absolute_path):
        ic(DICOMReader.test_folder(absolute_path))
        ic(len(DICOMReader.test_folder(absolute_path)))
    else:
        print("not dicom")

def test_caching():
    print("initial memory used")
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("loading '3 plane Loc SSFSE BH'")
    test_dicom_reader['3 plane Loc SSFSE BH']
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("reloading '3 plane Loc SSFSE BH' from cache, should be minimal change from above")
    test_dicom_reader['3 plane Loc SSFSE BH']
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("loading 'Ax 2D FIESTA'")
    test_dicom_reader['Ax 2D FIESTA']
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

    print("reloading '3 plane Loc SSFSE BH' from cache, should be minimal change from above")
    test_dicom_reader['3 plane Loc SSFSE BH']
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

def vtk_out():
    reader = vtk.vtkDICOMImageReader()
    reader.SetDirectoryName(absolute_path)
    reader.Update()

    # Visualize
    imageViewer = vtk.vtkImageViewer2()
    imageViewer.SetInputConnection(reader.GetOutputPort())




    # initialize rendering and interaction
    imageViewer.GetRenderWindow().SetSize(400, 300)
    imageViewer.GetRenderer().SetBackground(0.2, 0.3, 0.4)
    imageViewer.Render()
    imageViewer.GetRenderer().ResetCamera()
    imageViewer.Render()

    window = vtk.vtkRenderWindow()
    window.AddRenderer(imageViewer.GetRenderer())

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.Start()

# if __name__ == "__main__":
#     vtk_out()