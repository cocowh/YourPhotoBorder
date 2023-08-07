import exifread
from PIL import Image, ImageDraw, ImageFont

class JpegAnalyzer(object):
    def __init__(self,path,exif_source_path=None):
        self.path = path
        self.exif_source_path = exif_source_path
        if exif_source_path == None:
            with open(self.path, 'rb') as f:
                self.tags = exifread.process_file(f)
        else:
            with open(self.exif_source_path, 'rb') as f:
                self.tags = exifread.process_file(f)

    def get_camera_model(self) -> str:
        '''
        获取相机型号
        '''
        return str(self.tags['Image Model'])
    
    def get_camera_iso(self) -> str:
        '''
        获取照片的ISO
        '''
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return str(self.tags['EXIF ISOSpeedRatings'])
    
    def get_camera_aperture(self) -> str:
        '''
        获取照片的光圈
        '''
        aperture = str(self.tags['EXIF FNumber'])
        if aperture.isdigit():
            return aperture
        else:
            aperture_array = aperture.split("/")
            return str(int(aperture_array[0]) / int(aperture_array[1]))
    
    def get_camera_exposure_time(self) -> str:
        return str(self.tags['EXIF ExposureTime'])
    
    def get_camera_lens_model(self) -> str:
        return str(self.tags['EXIF LensModel'])
    
    def get_width(self) -> int:
        image = Image.open(self.path)
        width = image.width
        image.close()
        return width
        
    def get_height(self) -> int:
        image = Image.open(self.path)
        height = image.height
        image.close()
        return height
        
    def get_original_datetime(self):
        return str(self.tags['EXIF DateTimeOriginal'])
    
    def get_camera_focal_length(self) -> str:
        focal_length = str(self.tags['EXIF FocalLength'])
        if focal_length.isdigit():
            
            return int(focal_length)
        else:
            focal_length_array = focal_length.split("/")
            return str(int(focal_length_array[0]) / int(focal_length_array[1]))
        
    def get_image_format(self) -> str:
        image = Image.open(self.path)
        image_format = str(image.format)
        image.close()
        return image_format
        
    def get_image_orientation(self) -> tuple:
        # Rotated 90 CCW
        # Horizontal normal
        # CCW 逆时针旋转
        # CW  顺时针
        
        
        tags = self.tags
        ## 拦截hook
        if self.exif_source_path != None:
            with open(self.path, 'rb') as f:
                tags = exifread.process_file(f)
        if 'Image Orientation' not in tags:
            return ('Horizontal','normal')
        orientation = str(tags['Image Orientation']).strip().split(" ")
        if len(orientation) == 2:
            return (orientation[0],orientation[1])
        else:
            return (orientation[0],int(orientation[1]),orientation[2])
    def get_camera_company(self) -> str:
        if 'Image Make' not in self.tags:
            return None
        return str(self.tags['Image Make'])
    
def test():
    test_jpeg_path = "../test/0711_1.jpg"
    
    analyzer = JpegAnalyzer(test_jpeg_path)
    print(f"Image Format: {analyzer.get_image_format()}")
    print(f"Camera Model: {analyzer.get_camera_model()}")
    print(f"Lens Camera Model: {analyzer.get_camera_lens_model()}")
    print(f"ISO: {analyzer.get_camera_iso()}")
    print(f"Exposure Time: {analyzer.get_camera_exposure_time()}")
    print(f"Aperture: {analyzer.get_camera_aperture()}")
    print(f"Width: {analyzer.get_width()}")
    print(f"Height: {analyzer.get_height()}")
    print(f"Time: {analyzer.get_original_datetime()}")
    print(f"Orientation: {analyzer.get_image_orientation()}")
    print(f"Camera Company: {analyzer.get_camera_company()}")
    
    
def main():
    test()
if __name__ == '__main__':
    main()
