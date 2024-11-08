import datetime

import exifread
from PIL import Image, ImageDraw, ImageFont


class JpegAnalyzer(object):
    def __init__(self, path, exif_source_path=None):
        self.path = path
        self.exif_source_path = exif_source_path
        if exif_source_path is None:
            with open(self.path, 'rb') as f:
                self.tags = exifread.process_file(f)
        else:
            with open(self.exif_source_path, 'rb') as f:
                self.tags = exifread.process_file(f)

    def get_camera_model(self) -> str:
        """
        获取相机型号
        """
        return str(self.tags['Image Model'])

    def get_camera_iso(self) -> str:
        """
        获取照片的ISO
        """
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return str("" if "EXIF ISOSpeedRatings" not in self.tags else tags['EXIF ISOSpeedRatings'])

    def get_camera_aperture(self) -> str:
        """
        获取照片的光圈
        """
        aperture = str("" if "EXIF FNumber" not in self.tags else self.tags['EXIF FNumber'])
        if aperture == "":
            return ""
        if aperture.isdigit():
            return aperture
        else:
            aperture_array = aperture.split("/")
            return str(int(aperture_array[0]) / int(aperture_array[1]))

    def get_camera_exposure_time(self) -> str:
        return str("" if "EXIF ExposureTime" not in self.tags else self.tags['EXIF ExposureTime'])

    def get_camera_lens_model(self) -> str:
        return str("" if "EXIF LensModel" not in self.tags else self.tags['EXIF LensModel'])

    def get_width(self) -> int:
        image = Image.open(self.path)
        width = image.width
        if self.get_image_orientation()[0] == 'Rotated':
            width = image.height
        image.close()
        """
        tags = self.tags
        ## 拦截hook
        if self.exif_source_path != None:
            image = Image.open(self.path)
            width = image.width
            image.close()
            return width
        orientation = self.get_image_orientation()
        if orientation[0] == 'Horizontal':
            return int(str(tags['EXIF ExifImageWidth']))
        else:
            return int(str(tags['EXIF ExifImageLength']))
        """
        return width

    def get_height(self) -> int:
        image = Image.open(self.path)
        height = image.height
        if self.get_image_orientation()[0] == 'Rotated':
            height = image.width
        image.close()
        '''
        tags = self.tags
        ## 拦截hook
        if self.exif_source_path != None:
            image = Image.open(self.path)
            height = image.height
            image.close()
            return height
        orientation = self.get_image_orientation()
        print(tags.keys())
        if orientation[0] == 'Horizontal':
            return int(str(tags['EXIF ExifImageLength']))
        else:
            return int(str(tags['EXIF ExifImageWidth']))
        '''
        return height

    def get_original_datetime(self):
        return str(
            datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S') if "EXIF DateTimeOriginal" not in self.tags else
            self.tags['EXIF DateTimeOriginal'])

    def get_camera_focal_length(self) -> int | str:
        focal_length = str("" if "EXIF FocalLength" not in self.tags else self.tags['EXIF FocalLength'])
        if focal_length == "":
            return ""
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
        # 拦截hook
        # if self.exif_source_path != None:
        #    with open(self.path, 'rb') as f:
        #        tags = exifread.process_file(f)
        if 'Image Orientation' not in tags:
            return ('Horizontal', 'normal')
        orientation = str(tags['Image Orientation']).strip().split(" ")
        if len(orientation) == 2:
            return (orientation[0], orientation[1])
        else:
            return (orientation[0], int(orientation[1]), orientation[2])

    def get_camera_company(self) -> str:
        if 'Image Make' not in self.tags:
            return None
        return str(self.tags['Image Make'])


def test():
    # test_jpeg_path = '../test/DSC00524.JPG'
    # test_jpeg_path = "../test/test_photo.jpg"
    # test_jpeg_path = "../output/output.jpg"
    test_jpeg_path = "../../p/IMG_0757_1.jpg"

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
