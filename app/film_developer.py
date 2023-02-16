import io
import os
from datetime import datetime

from PIL import Image, ImageOps, ImageCms, ImageEnhance

def convert_to_profile(img: Image, profile_name: str):
    icc = img.info.get('icc_profile', '')
    if icc:
        io_handle = io.BytesIO(icc)
        src_profile = ImageCms.ImageCmsProfile(io_handle)
        dst_profile = ImageCms.createProfile(profile_name)
        img = ImageCms.profileToProfile(img, src_profile, dst_profile)
    return img


# decorators
def black_and_white(method):
    def wrapper(self):
        grayscaled_image    = ImageOps.grayscale(method(self))
        result_image        = ImageOps.invert(grayscaled_image)
        return result_image
    return wrapper


def color(method):
    def wrapper(self):
        image            = method(self)
        
        enhancer         = ImageEnhance.Contrast(image)
        image            = enhancer.enhance(1.25)

        enhancer         = ImageEnhance.Brightness(image)
        image            = enhancer.enhance(0.95)

        result_image  = ImageOps.invert(image)

        return result_image
    return wrapper


class FilmDeveloper:
    def __init__(  
            self,
            filename,
            format,
            upload_folder,
            result_folder,
            *args,
            **kwargs):
        self.filename         = filename
        self.format           = format
        self.upload_folder    = upload_folder
        self.result_folder    = result_folder
        self.result_filename  = self._get_result_filename()

    def _name_generator(self) -> str:
        time = datetime.now()
        time_str = datetime.strftime(time, '%Y%m%d%H%M%S')

        return time_str


    def _get_result_filename(self) -> str:
        filename  = self._name_generator()
        return f'{filename}.{self.format}'


    def get_result_image(self) -> Image:
        path  = f'./{self.upload_folder}/{self.filename}'
        image = Image.open(path)

        os.remove(path)

        return image


    def execute(self) -> None:
        result_image = self.get_result_image()
        result_filename = self.result_filename

        result_image.save(f'./{self.result_folder}/{result_filename}')



class FilmDeveloperBW(FilmDeveloper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @black_and_white
    def get_result_image(self) -> Image:
        path  = f'./{self.upload_folder}/{self.filename}'
        image = Image.open(path)

        os.remove(path)

        return image



class FilmDeveloperColor(FilmDeveloper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @color
    def get_result_image(self) -> Image:
        path  = f'./{self.upload_folder}/{self.filename}'
        image = Image.open(path)

        os.remove(path)

        return image
